# pySmartDL 

This software is a fork of the pySmartDL or **Python Smart Download Manager**, which appears to not be maintained anymore. I (1) went through its codebase to check if things work as expected in modern (Python 3.8-12) versions of Python, (2) did some modernizing fixes here and there, and (3) implemented test suites. These test suites go over currently popular Python version on four platforms: Linux (Ubuntu), MacOs (Intel CPU), MacOs (M1 CPU), and Windows.

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_Linux.yaml/badge.svg)](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_Linux.yaml)

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_MacM1.yaml/badge.svg)](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_MacM1.yaml)

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_MacIntel.yaml/badge.svg)](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_MacIntel.yaml)

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_Windows.yaml/badge.svg)](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_Windows.yaml)

Per the original README, `pySmartDL` strives to be a full-fledged smart download manager for Python. Main features:

* Built-in download acceleration (with the [multipart downloading technique](http://stackoverflow.com/questions/93642/how-do-download-accelerators-work)).
* Mirrors support.
* Pause/Unpause feature.
* Speed limiting feature.
* Hash checking.
* Non-blocking, shows the progress bar, download speed and ETA.
* Full support for custom headers and methods.

 
## Installation

You can install `pySmartDL` from PyPI through `pip`, with a simple:

```cmd
pip install pySmartDL
```

Or you can install from the source in _editable_ mode, by cloning this repository and:

```cmd
pip install -e .
```
 
## Usage

Downloading is as simple as creating an instance and starting it:

```python
from pySmartDL import SmartDL

url = "https://raw.githubusercontent.com/amkrajewski/pySmartDL/master/test/7za920.zip"
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