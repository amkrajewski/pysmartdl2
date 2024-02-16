# pysmartdl2

[![GitHub top language](https://img.shields.io/github/languages/top/amkrajewski/pysmartdl2)](https://github.com/amkrajewski/pysmartdl2)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysmartdl2)](https://pypi.org/project/pysmartdl2)
![GitHub License](https://img.shields.io/github/license/amkrajewski/pysmartdl2)
[![PyPI - Version](https://img.shields.io/pypi/v/pysmartdl2?label=PyPI&color=green)](https://pypi.org/project/pysmartdl2)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pysmartdl2)](https://pypi.org/project/pysmartdl2)

This software is a fork of the `pySmartDL` or **Python Smart Download Manager** by iTaybb which appears to not be maintained anymore. I (1) went through its codebase to check if things work as expected in modern (Python 3.8-12+) versions of Python, (2) did some modernizing fixes here and there, (3) fixed broken test suites, (4) implemented automated testing workflows, and (4) restructured the package to modern standards (e.g., `pyproject.toml`). Enjoy!

Test suites go over all popular Python versions (Python 3.8 - 3.13) on all four platforms enabled by GitHub Action Runners: Linux (Ubuntu), MacOS (Intel CPU), MacOS (M1 CPU), and Windows. Live status is shown below.

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_Linux.yaml/badge.svg)](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_Linux.yaml)

[![Multi-OS Multi-Python Build2](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_MacM1.yaml/badge.svg)](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_MacM1.yaml)

[![Multi-OS Multi-Python Build3](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_MacIntel.yaml/badge.svg)](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_MacIntel.yaml)

[![Multi-OS Multi-Python Build4](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_Windows.yaml/badge.svg)](https://github.com/amkrajewski/pysmartdl2/actions/workflows/test_Windows.yaml)

Per the original README, `pysmartdl` strives to be a full-fledged smart download manager for Python. Main features:

* Built-in download acceleration (with the [multipart downloading technique](http://stackoverflow.com/questions/93642/how-do-download-accelerators-work)).
* Mirrors support.
* Pause/Unpause feature.
* Speed limiting feature.
* Hash checking.
* Non-blocking, shows the progress bar, download speed and ETA.
* Full support for custom headers and methods.

 
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

Copyright (C) 2023-2024 Adam M. Krajewski

Copyright (C) 2014-2020 Itay Brandes.
