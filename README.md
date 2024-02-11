# pysmartdl

This software is a fork of the `pySmartDL` or **Python Smart Download Manager** by iTaybb which appears to not be maintained anymore. I (1) went through its codebase to check if things work as expected in modern (Python 3.8-12+) versions of Python, (2) did some modernizing fixes here and there, (3) implemented test suites, and (4) restructured it to modern standards with `pyproject.toml`. 

Test suites go over all popular Python versions on all four platforms: Linux (Ubuntu), MacOS (Intel CPU), MacOS (M1 CPU), and Windows. Live status is shown below.

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_Linux.yaml/badge.svg)](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_Linux.yaml)

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_MacM1.yaml/badge.svg)](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_MacM1.yaml)

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_MacIntel.yaml/badge.svg)](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_MacIntel.yaml)

[![Multi-OS Multi-Python Build](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_Windows.yaml/badge.svg)](https://github.com/amkrajewski/pySmartDL/actions/workflows/test_Windows.yaml)

Per the original README, `pysmartdl` strives to be a full-fledged smart download manager for Python. Main features:

* Built-in download acceleration (with the [multipart downloading technique](http://stackoverflow.com/questions/93642/how-do-download-accelerators-work)).
* Mirrors support.
* Pause/Unpause feature.
* Speed limiting feature.
* Hash checking.
* Non-blocking, shows the progress bar, download speed and ETA.
* Full support for custom headers and methods.

 
## Installation

You can install `pysmartdl` from PyPI through `pip`, with a simple:

```cmd
pip install pysmartdl
```

Or you can install from the source in _editable_ mode, by cloning this repository and:

```cmd
pip install -e .
```
 
## Usage

Downloading is as simple as creating an instance and starting it:

```python
from pysmartdl import SmartDL

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