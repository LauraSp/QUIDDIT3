from QImpWindowBasics import *
from QSettings import *

class QENVIInp:
    def __init__(self, hdr, dat):
        self.hdr = hdr
        self.dat = dat

class QAskENVIWindow(QTclPopupWindow):
    """Input Window for ENVI conversion"""
    def __init__(self, parent, title, enviinp, is_modal=True):
        self.envidta = enviinp
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)

    def make_gui(self, title):
        """making he gui controls for this window
        """
        self.setwintitle(title)

        self.hdr = self.envidta.hdr
        self.dat = self.envidta.dat

        r = 0
        lfr = self.make_label_frame(self, lrow=r, cspan=2, caption='Select ENVI files for visualisation', padx=(5,5), pady=(5,5))

        w = 44
        ir = 0
        self.hdrentry = self.makeentry(lfr, lrow=ir, erow=ir, ecol=1, caption="Header file", width=w)
        self.makebutton(lfr, erow=ir, ecol=2, caption='...', cmd=self.get_hdrfile, padx=(0,5))

        ir += 1
        self.datentry = self.makeentry(lfr, lrow=ir, erow=ir, ecol=1, caption="Data file", width=w)
        self.makebutton(lfr, erow=ir, ecol=2, caption='...', cmd=self.get_datfile, padx=(0,5))

        r += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=r)


        
    def loaded (self):
        self.set_entry_text(self.hdrentry, self.envidta.hdr)
        self.set_entry_text(self.datentry, self.envidta.dat)


    def get_hdrfile(self):
        hdrfilevar = fd.askopenfilename(parent = self,
        initialdir = QSettings.userhome,
        title="Select header file",
        filetypes=(('HDR','*.HDR'),('HDR','*.hdr'),('all','*.*'),('all','*.*')))
        self.set_entry_text(self.hdrentry, hdrfilevar)

    def get_datfile(self):
        datfilevar = fd.askopenfilename(parent = self,
        initialdir = QSettings.userhome,
        title="Select data file",
        filetypes=(('DAT','*.DAT'),('DAT','*.dat'),('all','*.*'),('all','*.*')))
        self.set_entry_text(self.datentry, datfilevar)  


    def ok_pressed(self):
        self.envidta.hdr = self.hdrentry.get()
        self.envidta.dat = self.datentry.get()
        super().ok_pressed()