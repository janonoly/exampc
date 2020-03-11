import sys
from cx_Freeze import setup, Executable,finder

# Dependencies are automatically detected, but it might need fine tuning.
build_exe_options = {"packages": ["os"],  "path": sys.path,  "excludes": ["tkinter"], 'includes': ['sqlalchemy','xlrd','pyqt5','sqlalchemy_utils','sqlalchemy.ext.declarative','sqlalchemy.orm'], 'include_files':['controllers','model','config','resources','views']}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "单机考试系统",
        version = "1.0",
        description = "单机考试系统!",
        options = {"build_exe": build_exe_options},

        executables = [Executable("main.py", base=base)])