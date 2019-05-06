from QImpWindowBasics import *
from QSettings import *

class QENVIconversionInp:
    def __init__(self, hdr, dat, targetdir):
        self.hdr = hdr
        self.dat = dat
        self.targetdir = targetdir

class QENVIconversionWindow(QTclPopupWindow):
    """Input Window for ENVI conversion"""
    def __init__(self, parent, title, enviconvinp, is_modal=True):
        self.convdta = enviconvinp
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)

    def make_gui(self, title):
        """making he gui controls for this window
        """
        self.setwintitle(title)

        self.hdr = self.convdta.hdr
        self.dat = self.convdta.dat
        self.targetdir = self.convdta.targetdir

        r = 0
        lfr = self.make_label_frame(self, lrow=r, cspan=2, caption='Select ENVI files for conversion', padx=(5,5), pady=(5,5))

        w = 44
        ir = 0
        self.hdrentry = self.makeentry(lfr, lrow=ir, erow=ir, ecol=1, caption="Header file", width=w)
        self.makebutton(lfr, erow=ir, ecol=2, caption='...', cmd=self.get_hdrfile, padx=(0,5))

        ir += 1
        self.datentry = self.makeentry(lfr, lrow=ir, erow=ir, ecol=1, caption="Data file", width=w)
        self.makebutton(lfr, erow=ir, ecol=2, caption='...', cmd=self.get_datfile, padx=(0,5))

        ir += 1
        self.targetdirentry = self.makeentry(lfr, lrow=ir, erow=ir, ecol=1, caption="Save files to", width=w)
        self.makebutton(lfr, erow=ir, ecol=2, caption='...', cmd=self.get_targetdir, padx=(0,5), pady=(0,5))

        r += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=r)


        
    def loaded (self):
        self.set_entry_text(self.hdrentry, self.convdta.hdr)
        self.set_entry_text(self.datentry, self.convdta.dat)
        self.set_entry_text(self.targetdirentry, self.convdta.targetdir)


    def get_hdrfile(self):
        hdrfilevar = fd.askopenfilename(parent = self,
        initialdir = QSettings.home,
        title="Select header file",
        filetypes=(('HDR','*.HDR'),('HDR','*.hdr'),('all','*.*'),('all','*.*')))
        self.set_entry_text(self.hdrentry, hdrfilevar)

    def get_datfile(self):
        datfilevar = fd.askopenfilename(parent = self,
        initialdir = QSettings.home,
        title="Select data file",
        filetypes=(('DAT','*.DAT'),('DAT','*.dat'),('all','*.*'),('all','*.*')))
        self.set_entry_text(self.datentry, datfilevar)  

    def get_targetdir(self):
        targetdir = fd.askdirectory(parent=self,
                            initialdir=QSettings.home,
                            title='Select directory for individual spectra to be stored')
        self.set_entry_text(self.targetdirentry, targetdir)

    def ok_pressed(self):
        self.convdta.hdr = self.hdrentry.get()
        self.convdta.dat = self.datentry.get()
        self.convdta.targetdir = self.targetdirentry.get()
        super().ok_pressed()
