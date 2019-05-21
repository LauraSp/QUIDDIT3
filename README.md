# QUIDDIT 3
QUantification of Infrared active Defects in Diamond and Inferred Temperatures

The most recent version (v. 3) is easier to use, more manageable and expandable and comes with improved exception handling. See below for list of pending and completed tasks.

**license:** You are free to download and use QUIDDIT and all its components.

## Download
**Help us** by letting us know if you have downloaded QUIDDIT! Even if you don't end up using it, please let us know (you can email laura.speich@bristol.ac.uk). Thank you!

All necessary files can be downloaded by visiting the [this website](https://github.com/LauraSp/QUIDDIT3).

This includes commented Jupyter Notebooks documenting the baseline correction and main data processing (see https://jupyter.org/ for instructions on how to use Jupyter Notebook). A full manual of QUIDDIT in PDF format is available in the QUIDDIT GitHub repository as well.

## Installation instructions
### Install Python
In order to run QUIDDIT, you will need a working version of **Python 3**.

I recommend installing an integrated development environment (IDE) that includes the most commonly used libraries. To run QUIDDIT, you will need:
* [SciPy](https://www.scipy.org/)
* [NumPy](http://www.numpy.org/)
* [matplotlib](https://matplotlib.org/)
* [Tkinter](https://docs.python.org/2/library/tk.html)
* [webbrowser](https://docs.python.org/2/library/webbrowser.html)
* [Spectral Python (Spy)](http://www.spectralpython.net/)

All of these are part of the most common IDE for Python. The instructions in the manual were created for use with Spyder (which is part of the Anaconda package), so I recommend installing Anaconda and running scripts with Spyder for users not familiar with coding.

To install Anaconda, visit the [Anaconda download site](https://www.anaconda.com/download/)

Chose your operating system and follow the on-screen instructions.

### Install QUIDDIT
Download the **QUIDDIT** package from [GitHub](https://github.com/LauraSp/QUIDDIT3) and unpack the zip file. (To download, select "Clone or download" on the repository website)

To install **Spectral Python (Spy)**, you will have to open a command window (type "cmd" into the search function in your start menu if you are on a Windows system) and navigate to the directory that contains your Python (Anaconda) installation. The Anaconda installer will ask where to install Anaconda. It will most likely be located in "C:\Program Files\Anaconda3\Scripts" or "C:\Users\[Username]\AppData\Local\Continuum\Anaconda3\Scripts" or "C:\ProgramData\Anaconda3\Scripts". You will need to use the `cd [path]` command to do so.

Once you have navigated to the Scripts folder, type `pip install spectral`. Spectral Python should be installed in your system, this should only take a few minutes. You might be prompted to enter your password during installation.

Detailed instructions for the installation of spectral can be found [here](http://www.spectralpython.net/installation.html).


### Running QUIDDIT
To run QUIDDIT, open your python IDE of choice and find and run the **"QMainWindow"** file in the downloaded repository (you may need to unzip the files in the repository first). The GUI can also be run using IDLE (a very basic standard Python IDE) or from the command line.

If you are using Anaconda, start **Spyder** (either directly from the start menu if you are on a Windows system or by starting the Anaconda Navigator first and then selecting "Launch Spyder"). Spyder may take a few minutes to start. Once it is finished, you can open the QUIDDIT script by selecting "File", then "Open..." from the start menu or by clicking the "Open File" icon. Navigate to the QUIDDIT folder you have downloaded and unzipped and select the file **"QMainWindow.py"**. This is usually the only file you will have to open. To run the script, select "Run", then "Run" from the top or the single green arrow icon or hit the F5 key. If this is the first time you are running a script, you might be asked to agree to some run settings. You can confirm the defaults by clicking "Ok".

## Known Bugs and Issues
This section provides an overview over known issues with QUIDDIT in order of priority. The author is working on resolving them but no guarantee can be given at what point they will be fixed.

* moving the cursor to the diagram frame sometimes leads to flickering of the window because displaying x-y-data and toolbar info at the bottom changes 
sizing. (Note: This can be avoided by making the window bigger)
* quadplot looks ugly


## Tasks (version 3)
### Improving user/developer experience
- [x] Split up main file (aka "the god file") into more managable blocks
- [x] Improve layout of windows
- [x] Basic exception handling
- [ ] Add baseline correction to manual peak fitting


### New features
- [x] Determine diamond type (beta! Use with care.)
- [x] Converting ENVI files to CSV
- [x] Batch Peak fitting with output
- [x] Batch Peak fitting Review
- [x] 2-stage N aggregation modelling with file output
- [x] Quadplot
- [x] Manual N fitting
- [x] Manual Peak fitting
- [ ] Custom baseline correction (e.g. allow 1st or 2nd order polynomial instead of just 3rd order polynomial)


## Contact:
For further questions or suggestions, please contact

Laura Speich: laura.speich@bristol.ac.uk (ls1394@my.bristol.ac.uk)


## See also:
[Manual.pdf](https://github.com/LauraSp/QUIDDIT3/blob/master/Manual.pdf)

[QUIDDIT on Researchgate](https://www.researchgate.net/project/QUIDDIT-a-software-tool-for-automated-processing-of-diamond-IR-spectra)


