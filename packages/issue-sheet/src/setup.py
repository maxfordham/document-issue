# -*- coding: utf-8 -*-

# A very simple setup script to create a single executable
#
# hello.py is a very simple 'Hello, world' type script which also displays the
# environment in which the script runs
#
# Run the build process by running the command 'python setup.py build'
#
# If everything works well you should find a subdirectory in the build
# subdirectory that contains the files needed to run the script without Python

import sys, os
from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("__main__.py", base=base)]

additional_mods = ["numpy.core._methods", "numpy.lib.format"]
exclude_mods = [
    "babel",
    "mf_pyIES",
    "scipy",
    "PyQt5",
    "tornado",
    "zmq",
    "sphinx",
    "sphinx_rtd_theme",
    "psutil",
    "notebook",
    "nbconvert",
    "lxml",
    "cryptography",
    "bottleneck",
    "matplotlib",
    "mf_xlwings",
]

build_exe_options = {
    "excludes": exclude_mods,
    "includes": additional_mods,
    "optimize": 1,
}

os.environ["TCL_LIBRARY"] = r"C:\ProgramData\Miniconda3\tcl\tcl8.6"
os.environ["TK_LIBRARY"] = r"C:\ProgramData\Miniconda3\tcl\tk8.6"

setup(
    name="document_issue",
    version="0.1",
    includes=["os"],
    options={"build_exe": build_exe_options},
    description="Document issue freeze",
    executables=executables,
    include_package_data=True,
)
