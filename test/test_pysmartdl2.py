import os
import sys
import random
import time
import string
import json
import math
import unittest
import warnings
import tempfile
import socket

from pysmartdl2 import SmartDL, HashFailedException, CanceledException, utils

class TestSmartDL(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=ResourceWarning, message="unclosed.*<ssl.SSLSocket.*>")
        self.dl_dir = os.path.join(tempfile.gettempdir(), "".join([random.choice(string.ascii_letters+string.digits) for i in range(8)]), '')
        while os.path.exists(self.dl_dir):
            self.dl_dir = os.path.join(tempfile.gettempdir(), "".join([random.choice(string.ascii_letters+string.digits) for i in range(8)]), '')
            
        self.res_7za920_mirrors = [
            "https://raw.githubusercontent.com/amkrajewski/pysmartdl2/refs/heads/main/test/7za920.zip",
            "http://www.bevc.net/dl/7za920.zip"
        ]
        self.res_7za920_hash = '2a3afe19c180f8373fa02ff00254d5394fec0349f5804e0ad2f6067854ff28ac'
        self.res_testfile_1gb = 'https://proof.ovh.net/files/1Gb.dat'
        self.res_testfile_100mb = 'https://proof.ovh.net/files/100Mb.dat'
        self.enable_logging = "-vvv" in sys.argv
    
    def test_download(self):
        """-->Testing the ability to download a file:"""
        obj = SmartDL(
            self.res_7za920_mirrors, 
            dest=self.dl_dir, 
            progress_bar=False, 
            connect_default_logger=self.enable_logging)
        obj.start()
        self.assertEqual(obj.get_progress_bar(), '[##################]')

        data = obj.get_data(binary=True, bytes=2)
        
        self.assertEqual(data, b'PK')

        # attempt to start a completed task
        with self.assertRaises(RuntimeError) as ctx:
            obj.start()
    
    def test_mirrors(self):
        """-->Testing the ability to download from multiple mirrors, where the first one is a fake one:"""
        urls = ["http://totally_fake_website/7za.zip", "https://raw.githubusercontent.com/amkrajewski/pysmartdl2/refs/heads/main/test/7za920.zip"]
        obj = SmartDL(urls, dest=self.dl_dir, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.start()
        
        self.assertTrue(obj.isSuccessful())
        
    def test_hash(self):
        """-->Testing hash verification in case of positive and negative results:"""
        obj = SmartDL(
            self.res_7za920_mirrors, 
            progress_bar=False, 
            connect_default_logger=self.enable_logging)
        obj.add_hash_verification('sha256' , self.res_7za920_hash)  # good hash
        obj.start(blocking=False)  # no exceptions
        obj.wait()
        
        self.assertTrue(obj.isSuccessful())

        obj = SmartDL(
            self.res_7za920_mirrors, 
            progress_bar=False, 
            connect_default_logger=self.enable_logging)
        obj.add_hash_verification('sha256' ,'a'*64)  # bad hash
        obj.start(blocking=False)  # no exceptions
        obj.wait()
        
        self.assertFalse(obj.isSuccessful())
        errorList = obj.get_errors()
        self.assertTrue(len(errorList) > 0)
        self.assertTrue(HashFailedException in [type(e) for e in errorList])
        
    def test_pause_unpause(self, testfile=None):
        """-->Testing the ability to pause and unpause a download:"""
        obj = SmartDL(
            testfile if testfile else self.res_7za920_mirrors, 
            dest=self.dl_dir, 
            progress_bar=False, 
            connect_default_logger=self.enable_logging)
        obj.start(blocking=False)

        while not obj.get_dl_size():
            time.sleep(0.1)

        # pause
        obj.pause()
        time.sleep(0.5)
        if obj.get_status() == "finished":
            print("\nThe test file downloaded too fast, trying a bigger file: ...")
            if self.res_testfile_100mb == testfile:
                self.fail("The download got completed before we could stop it, even though we've used a big file. Are we on a 100GB/s internet connection or somethin'?")
            return self.test_pause_unpause(testfile=self.res_testfile_100mb)
        
        dl_size = obj.get_dl_size()

        # verify download has really stopped
        time.sleep(1.5)
        self.assertEqual(dl_size, obj.get_dl_size())
        
        # continue
        obj.unpause()
        time.sleep(3)
        self.assertNotEqual(dl_size, obj.get_dl_size())
        
        obj.wait()
        self.assertTrue(obj.isSuccessful())

    def test_stop(self):
        """-->Testing the ability to stop a download:"""
        obj = SmartDL(self.res_testfile_100mb, dest=self.dl_dir, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.start(blocking=False)

        while not obj.get_dl_size():
            time.sleep(0.1)

        obj.stop()
        obj.wait()
        self.assertFalse(obj.isSuccessful())

    def test_speed_limiting(self):
        """-->Testing the ability to limit the download speed to 1MB/s. Takes 30 seconds and should be around 30MB:"""
        obj = SmartDL(self.res_testfile_1gb, dest=self.dl_dir, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.limit_speed(1024**2)  # 1MB per sec
        obj.start(blocking=False)

        while not obj.get_dl_size():
            time.sleep(0.1)
        time.sleep(30)

        expected_dl_size = 30 * 1024**2
        allowed_delta = 0.7  # because we took only 30sec, the delta needs to be quite big, it we were to test 60sec the delta would probably be much smaller
        diff = math.fabs(expected_dl_size - obj.get_dl_size()) / expected_dl_size

        obj.stop()
        obj.wait()

        self.assertLessEqual(diff, allowed_delta)
    
    def test_basic_auth(self):
        """-->Authentification testing:"""
        basic_auth_test_url = "https://httpbin.org/basic-auth/user/passwd"
        obj = SmartDL(basic_auth_test_url, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.add_basic_authentication('user', 'passwd')
        obj.start()
        data = obj.get_data()
        self.assertTrue(json.loads(data)['authenticated'])
        
    def test_unicode(self):
        """-->Handling of unicode URLs:"""
        url = "https://he.wikipedia.org/wiki/ג'חנון"
        obj = SmartDL(url, progress_bar=False, connect_default_logger=self.enable_logging)
        obj.start()

    def test_timeout(self):
        """-->Test that long delay triggers short timeout and short delay triggers no timeout:"""
        self.assertRaises(
            socket.timeout, 
            SmartDL, 
            "https://httpbin.org/delay/10", 
            progress_bar=False, 
            timeout=3, 
            connect_default_logger=self.enable_logging)

        obj = SmartDL(
            "https://httpbin.org/delay/3", 
            progress_bar=False, 
            timeout=15, 
            connect_default_logger=self.enable_logging)
        obj.start(blocking=False)
        obj.wait()
        self.assertTrue(obj.isSuccessful())

    def test_custom_headers(self):
        """-->Testing the ability to send custom headers:"""
        ua = "pySmartDL/1.3.2"
       	request_args = {"headers": {"User-Agent": ua}}
        obj = SmartDL("http://httpbin.org/headers", request_args=request_args, progress_bar=False)
        obj.start()
        data = obj.get_json()
        self.assertTrue(data['headers']['User-Agent'] == ua)

        # passing empty request_args
        obj = SmartDL("http://httpbin.org/headers", request_args={}, progress_bar=False)
        obj.start()
        self.assertTrue(obj.isSuccessful())

    def test_utils(self):
        """-->Testing the utility functions:"""
        with self.subTest("Progress bar rendering"):
            self.assertEqual(utils.progress_bar(0.6, length=42), '[########################----------------]')
        with self.subTest("Size formatting"):
            self.assertEqual(utils.sizeof_human(175799789), '167.7 MB')
            self.assertEqual(utils.sizeof_human(0), '0 bytes')
        with self.subTest("Time formatting"):
            self.assertEqual(utils.time_human(50), '50 seconds')
            self.assertEqual(utils.time_human(50, fmt_short=True), '50s')
            self.assertEqual(utils.time_human(0, fmt_short=True), '0s')
        with self.subTest("Chunk size calculation"):
            self._test_calc_chunk_size(10000, 10, 20)
            self._test_calc_chunk_size(1906023034, 20, 20)
            self._test_calc_chunk_size(261969919, 20, 32)

    def _test_calc_chunk_size(self, filesize, threads, minChunkFile):
        """-->Testing the calc_chunk_size function: """
        chunks = utils.calc_chunk_size(filesize, threads, 20)
        self.assertEqual(chunks[0][0], 0)
        self.assertIsInstance(chunks[0][0], int)
        self.assertIsInstance(chunks[0][1], int)

        for i in range(1, len(chunks)):
            self.assertIsInstance(chunks[i][0], int)
            self.assertIsInstance(chunks[i][1], int)
            self.assertTrue(chunks[i][0] <= chunks[i][1])
            self.assertEqual(chunks[i-1][1] + 1, chunks[i][0])
            
        self.assertEqual(chunks[-1][1], filesize-1)

if __name__ == '__main__':
    unittest.main(verbosity=3)
