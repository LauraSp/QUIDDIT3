@echo off
pyinstaller ^
--paths "C:\Users\tiger\Anaconda3\envs\quiddit3\Library" ^
--add-data "CAXBD.csv;." ^
--add-data "typeIIa.csv;." ^
--add-data "QUIDDITlogo.gif;." ^
--windowed ^
--clean ^
QMainWindow.py

rem usage: pyinstaller [-h] [-v] [-D] [-F] [--specpath DIR] [-n NAME]
rem                    [--add-data <SRC;DEST or SRC:DEST>]
rem                    [--add-binary <SRC;DEST or SRC:DEST>] [-p DIR]
rem                    [--hidden-import MODULENAME]
rem                    [--additional-hooks-dir HOOKSPATH]
rem                    [--runtime-hook RUNTIME_HOOKS] [--exclude-module EXCLUDES]
rem                    [--key KEY] [-d [{all,imports,bootloader,noarchive}]] [-s]
rem                    [--noupx] [-c] [-w]
rem                    [-i <FILE.ico or FILE.exe,ID or FILE.icns>]
rem                    [--version-file FILE] [-m <FILE or XML>] [-r RESOURCE]
rem                    [--uac-admin] [--uac-uiaccess] [--win-private-assemblies]
rem                    [--win-no-prefer-redirects]
rem                    [--osx-bundle-identifier BUNDLE_IDENTIFIER]
rem                    [--runtime-tmpdir PATH] [--bootloader-ignore-signals]
rem                    [--distpath DIR] [--workpath WORKPATH] [-y]
rem                    [--upx-dir UPX_DIR] [-a] [--clean] [--log-level LEVEL]
rem                    scriptname [scriptname ...]

rem --add-data "CAXBD.csv;CAXBD.csv" ^
rem --add-data "typeIIa.csv;typeIIa.csv" ^
