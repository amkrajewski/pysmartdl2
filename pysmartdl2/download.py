import os
import urllib.request, urllib.error, urllib.parse
import time
import socket
import http.client
from . import utils

class CanceledException(Exception):
    "Raised when the job is canceled."
    def __init__(self):
        pass
    def __str__(self):
        return 'CanceledException'
    def __repr__(self):
        return "<CanceledException>"

def _interruptible_sleep(duration, thread_shared_cmds, logger):
    remaining = float(duration)
    while remaining > 0:
        if thread_shared_cmds and 'stop' in thread_shared_cmds:
            logger.info('stop command received. Stopping.')
            raise CanceledException()
        step = min(0.2, remaining)
        time.sleep(step)
        remaining -= step

def download(url, 
             dest, 
             requestArgs=None, 
             context=None, 
             startByte=0, 
             endByte=None, 
             timeout=4, 
             shared_var=None, 
             thread_shared_cmds=None, 
             logger=None, 
             retries=3) -> None:
    "The basic download function that runs at each thread."
    logger = logger or utils.DummyLogger()
    if thread_shared_cmds and 'stop' in thread_shared_cmds:
        logger.info('stop command received. Stopping.')
        raise CanceledException()

    req = urllib.request.Request(url, **requestArgs)
    if endByte:
        req.add_header('Range', 'bytes={:.0f}-{:.0f}'.format(startByte, endByte))
    logger.info("Downloading '{}' to '{}'...".format(url, dest))
    try:
        # Context is used to skip ssl validation if verify is False.
        urlObj = urllib.request.urlopen(req, timeout=timeout, context=context)
    except (urllib.error.HTTPError, urllib.error.URLError, socket.timeout, http.client.HTTPException, ConnectionError) as e:
        is_retryable = not isinstance(e, urllib.error.HTTPError) or e.code in (416, 429, 500, 502, 503, 504)
        if is_retryable and retries > 0:
            '''
            HTTP 416 / 429 or transient network error: Happens when we open
            too many concurrent connections to the server or hit rate limits.
            Wait for other threads / rate-limit window and try again.
            '''
            retry_after = e.headers.get("Retry-After") if isinstance(e, urllib.error.HTTPError) else None
            wait_time = int(retry_after) if (retry_after and retry_after.isdigit()) else 5 * (4 - retries)
            wait_time = min(wait_time, 60)
            logger.warning("Thread encountered {}. Retrying in {}s ({} times left)...".format(e, wait_time, retries-1))
            _interruptible_sleep(wait_time, thread_shared_cmds, logger)
            return download(url, dest, requestArgs, context, startByte, endByte, timeout, shared_var, thread_shared_cmds, logger, retries-1)
        else:
            raise
    
    try:
        with open(dest, 'wb') as f:
            if endByte:
                filesize = endByte - startByte + 1
            else:
                filesize = 0
                try:
                    meta = urlObj.info()
                    filesize = int(urlObj.headers["Content-Length"])
                    logger.info("Content-Length is {}.".format(filesize))
                except (IndexError, KeyError, TypeError):
                    logger.warning("Server did not send Content-Length. Filesize is unknown.")
            
            filesize_dl = 0  # total downloaded size
            limitspeed_timestamp = time.time()
            limitspeed_filesize = 0
            block_sz = 8192
            while True:
                if thread_shared_cmds:
                    if 'stop' in thread_shared_cmds:
                        logger.info('stop command received. Stopping.')
                        raise CanceledException()
                    if 'pause' in thread_shared_cmds:
                        time.sleep(0.2)
                        limitspeed_timestamp = time.time()
                        limitspeed_filesize = filesize_dl
                        continue
                    if 'limit' in thread_shared_cmds and thread_shared_cmds['limit'] > 0:
                        now = time.time()
                        time_passed = now - limitspeed_timestamp
                        expected_time = (filesize_dl - limitspeed_filesize) / thread_shared_cmds['limit']
                        time_to_sleep = expected_time - time_passed
                        if time_to_sleep >= 0.05:
                            logger.debug('Thread has downloaded {} in {}. Limit is {}/s. Slowing down...'.format(utils.sizeof_human(filesize_dl-limitspeed_filesize), utils.time_human(time_passed, fmt_short=True, show_ms=True), utils.sizeof_human(thread_shared_cmds['limit'])))
                            _interruptible_sleep(time_to_sleep, thread_shared_cmds, logger)
                            limitspeed_timestamp += expected_time
                            limitspeed_filesize = filesize_dl
                        elif time_to_sleep < -1.0:
                            limitspeed_timestamp = now
                            limitspeed_filesize = filesize_dl
                    
                try:
                    buff = urlObj.read(block_sz)
                except Exception as e:
                    logger.error(str(e))
                    if shared_var:
                        shared_var.value -= filesize_dl
                    if retries > 0 and not (thread_shared_cmds and 'stop' in thread_shared_cmds):
                        urlObj.close()
                        _interruptible_sleep(5, thread_shared_cmds, logger)
                        return download(url, dest, requestArgs, context, startByte, endByte, timeout, shared_var, thread_shared_cmds, logger, retries-1)
                    raise
                    
                if not buff:
                    break

                filesize_dl += len(buff)
                if shared_var:
                    shared_var.value += len(buff)
                f.write(buff)
                if filesize and filesize_dl >= filesize:
                    break
    finally:
        urlObj.close()
