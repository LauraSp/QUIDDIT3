# Setup for cx_freeze deployment
import sys
import os
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
#build_exe_options = {"packages": ["os"], "excludes": ["tkinter"]}
#build_exe_options = {"packages": ["os"]}

# GUI applications require a different base on Windows (the default is for a
# console application).
base = 'Console'
#if sys.platform == "win32":
#    base = "Win32GUI"

conda_ticklp = os.path.join(sys.base_prefix, "tcl")
os.environ['TCL_LIBRARY'] = os.path.join(conda_ticklp, "tcl8.6")
os.environ['TK_LIBRARY']  = os.path.join(conda_ticklp, "tk8.6")

additional_mods = [
    'numpy.core._methods', 
    'numpy.lib.format',
    "scipy._distributor_init",
    "scipy.sparse.csgraph._validation",
    "scipy.optimize"
    ]

excluded_mods = [
    'scipy.spatial.cKDTree'
]

namespace_packages = [
    "mpl_toolkits"
]

libpath = os.path.join(sys.base_prefix, 'Library','bin')
build_exe_options = {
    'includes': additional_mods,
    'excludes': excluded_mods,
    'namespace_packages': namespace_packages,
    'include_files': [
        os.path.join(libpath, 'sqlite3.dll'),
        os.path.join(libpath, 'mkl_intel_thread.dll'),
        os.path.join(libpath, "mkl_core.dll"),
        os.path.join(libpath,'libiomp5md.dll'),
        os.path.join(libpath, 'mkl_core.dll'),
        os.path.join(libpath, 'mkl_def.dll'),
        "CAXBD.csv",
        "typeIIa.csv",
        "QUIDDITlogo.gif"
        ]
    }

setup(  name = "QUIDDIT",
        version = "3.0",
        description = "",
        options = {'build_exe': build_exe_options},
        executables = [Executable("QMainWindow.py", base=base)])
