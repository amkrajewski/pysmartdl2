# pysmartdl2

[![GitHub top language](https://img.shields.io/github/languages/top/amkrajewski/pysmartdl2)](https://github.com/amkrajewski/pysmartdl2)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysmartdl2)](https://pypi.org/project/pysmartdl2)
![GitHub License](https://img.shields.io/github/license/amkrajewski/pysmartdl2)
[![PyPI - Version](https://img.shields.io/pypi/v/pysmartdl2?label=PyPI&color=green)](https://pypi.org/project/pysmartdl2)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pysmartdl2)](https://pypi.org/project/pysmartdl2)

This software is a fork of the `pySmartDL` or **Python Smart Download Manager** by iTaybb which appears to not be maintained anymore. I (1) went through its codebase to check if things work as expected in modern (Python 3.8-12+) versions of Python, (2) did some modernizing fixes here and there, (3) fixed broken test suites, (4) implemented automated testing workflows, and (4) restructured the package to modern standards (e.g., `pyproject.toml`). New features were added and bugs have been fixed, but original API is and _will_ be retained, so that you can treat it as a **drop-in replacement**. Enjoy!

Test suites go over all popular Python versions (Python 3.8 - 3.14) on all four platforms enabled by GitHub Action Runners: Linux (Ubuntu), MacOS (M1 CPU), and Windows. Live status is shown below.

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_Linux.yaml/badge.svg)](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_Linux.yaml)
[![Multi-OS Multi-Python Build2](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_MacM1.yaml/badge.svg)](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_MacM1.yaml)
[![Multi-OS Multi-Python Build4](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_Windows.yaml/badge.svg)](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_Windows.yaml)

Per the pre-fork README, `pysmartdl2` is a lightweight but full-fledged smart download manager for Python. Main features:

- Built-in download acceleration (with the [multipart downloading technique](http://stackoverflow.com/questions/93642/how-do-download-accelerators-work))
- Mirrors support
- Pausing and unpausing
- Speed limiting feature
- Hash checking
- Non-blocking, shows the progress bar, download speed and ETA
- Full support for custom headers and methods

Beyond what was mentioned earlier, `pysmartdl2` ships with the following improvements over the legacy `pysmartdl`:
- Smart handling of HTTP 429 errors with respecting Retry-After, per-thread chunk recovery, and other improvements to work reliably in the age of filters against AI bots
- Proper socket cleanup and `HEAD`-based probing to avoid connection leaks and CDN throttling
- Mid-download mirror failover (quite unique feature!) with per-mirror `Range` re-evaluation.
- Accurate speed limiting and proper thread cancellations
- A number of bugfixes related to thread-pool, pause/wait race conditions at retries or fast connections
- Up-to-date `User-Agent` pool for reliable CDN compatibility

 
## Installation

You can install `pysmartdl2` from PyPI through `pip`, with a simple:

```cmd
pip install pysmartdl2
```

Or you can install from the source in _editable_ mode, by cloning this repository and:

```cmd
pip install -e .
```
 
## Usage

Downloading with it is as simple as creating an instance and starting it:

```python
from pysmartdl2 import SmartDL

url = "https://raw.githubusercontent.com/amkrajewski/pysmartdl2/master/test/7za920.zip"
dest = "."  # <-- To download to current directory 
            # or '~/Downloads/' for Downloads directory on Linux
            # or "C:\\Downloads\\" for Downloads directory on Windows

obj = SmartDL(url, dest)
obj.start()
# [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########--------] [60%, 2s left]

path = obj.get_dest()
```
