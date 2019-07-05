from QImpWindowBasics import *
from QSettings import *
from QTclMessageWindow import *

class QDPTconvinp:
    def __init__(self, dptfile, targetdir):
        self.dpt_file = dptfile
        self.target_dir = targetdir

class QDPTConversionWindow(QTclPopupWindow):
    def __init__(self, parent, title, dptconvinp, is_modal=True):
        self.dpt_file = dptconvinp.dpt_file
        self.target_dir = dptconvinp.target_dir
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)


    def loaded(self):
        pass
    
    def make_gui(self, title):
        self.setwintitle(title)

        w=44
        row = 0
        lfr = self.make_label_frame(lrow=row, lcol=0, caption='Select files', cspan=2, padx=(5,5), pady=(5,5))
        
        irow = 0
        self.selfileentry = self.makeentry(lfr, lrow=irow, erow=irow, ecol=1, caption='dpt file:', width=w)
        self.makebutton(lfr, erow=irow, ecol=2, caption='...', cmd=self.get_dptfile, sticky=tk.E, padx=(0,5), pady=(0,5))
        self.set_entry_text(self.selfileentry, self.dpt_file)

        irow += 1
        self.targetdirentry = self.makeentry(lfr, lrow=irow, erow=irow, ecol=1, caption='Save files to:', width=w)
        self.makebutton(lfr, erow=irow, ecol=2, caption='...', cmd=self.get_targetdir, sticky=tk.E, padx=(0,5), pady=(0,5))
        self.set_entry_text(self.targetdirentry, self.target_dir)

        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)


    def get_dptfile(self):
        selfilevar = fd.askopenfilename(parent=self,
                    initialdir = QSettings.userhome,
                    title="Select file",
                    filetypes=(('DPT','*.dpt'),('DPT','*.dpt'),('all','*.*'),('all','*.*')))
        self.set_entry_text(self.selfileentry, selfilevar)


    def get_targetdir(self):
        targetdir = fd.askdirectory(parent=self,
                            initialdir=QSettings.userhome,
                            title='Select directory for converted spectra to be stored')
        self.set_entry_text(self.targetdirentry, targetdir)


    def ok_pressed(self):
        self.dpt_file = self.selfileentry.get()
        self.target_dir = self.targetdirentry.get()
        super().ok_pressed()