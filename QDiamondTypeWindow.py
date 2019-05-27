from QTclPopupWindow import *

from QImpWindowBasics import *
from QSettings import *

class QDiamondTypeInp:
    def __init__(self, result, selectedfiles, savedir='', savevar=0):
        self.result = result
        self.selectedfiles = selectedfiles
        self.savevar = savevar
        self.savedir = savedir

class QDiamondTypeWindow(QTclPopupWindow):
    """Input Window for diamond type determination"""
    def __init__(self, parent, title, diamondtypeinput, is_modal=True):
        self.typedta = diamondtypeinput
        self.dresult = "NONE"
        self.savedir = self.typedta.savedir
        super().__init__(parent, title, is_modal)
        
    def make_gui(self, title):
        self.setwintitle(title)

        self.resultvar = self.getvar(self.typedta.result)
        self.selectedfilesvar = self.typedta.selectedfiles
        self.savevar = self.getvar(self.typedta.savevar)

        w = 24
        row = 0
        myfr = self.make_label_frame(lrow=row, caption='Enter data for diamond type determination', cspan=2, padx=(5,5), pady=(5,5))

        irow = 0
        self.result_name = self.makeentry(myfr, erow=irow, lrow=irow,
                                            caption='Name for results file: ',
                                            width=24,
                                            textvariable=self.resultvar)
        
        self.makelabel(myfr, lrow=irow, lcol=2, caption='.csv', sticky=tk.W)
        
        irow += 1
        self.spectrac = self.makeentry(myfr, lrow=irow, erow=irow, ecol=1, caption="Spectra: ", width=w)
        self.set_file_num()
        self.makebutton(myfr, erow=irow, ecol=2, caption='...', cmd=self.get_filenames, pady=(0,5))

        row += 1
        self.makelabel(lrow=row, cspan=2,
                    caption='Spectra will be baseline corrected for diamond type\ndetermination. Would you like to save them?',
                    sticky=tk.W, padx=(5,5), pady=(5,5))

        row += 1 
        self.makecheck(erow=row, caption='Save', variable=self.savevar, command=self.set_save, cspan=2, sticky=tk.W, padx=(5,5), pady=(0,5))

        row += 1
        self.savefr = self.make_label_frame(lrow=row, caption='Save baseline corrected spectra', cspan=2, padx=(5,5), pady=(5,5))

        irow +=1
        self.savecorrected = self.makeentry(self.savefr, lrow=irow, erow=irow, caption='Destination: ', width=w)
        self.dir_button = self.makebutton(self.savefr, erow=irow, ecol=2, caption='...', cmd=self.get_directory, pady=(0,5))
        self.set_save()

        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)


    def loaded(self):
        pass
        

    def set_file_num(self):
        self.spectrac.configure(state=tk.NORMAL)
        self.set_entry_text(self.spectrac, "{} files".format(len(self.selectedfilesvar)))
        self.spectrac.configure(state=tk.DISABLED)


    def get_filenames(self):
        self.selectedfilesvar = fd.askopenfilenames(parent = self,
            initialdir = QSettings.home,
            title="Select spectra",
            filetypes=(('CSV','*.CSV'),('CSV','*.csv')))
        self.set_file_num()


    def get_directory(self):
        self.savedir = fd.askdirectory(parent=self,
                    initialdir = QSettings.home,
                    title="Select directory")
        self.set_entry_text(self.savecorrected, self.savedir)


    def set_save(self):
        if self.savevar.get() == 1:
            self.savecorrected.configure(state=tk.NORMAL)
            self.dir_button.configure(state=tk.NORMAL)
            self.set_entry_text(self.savecorrected, self.savedir)

        else:
            self.savecorrected.configure(state=tk.DISABLED)
            self.dir_button.configure(state=tk.DISABLED)


    def ok_pressed(self):
        self.typedta.result = self.resultvar.get()
        self.typedta.selectedfiles = self.selectedfilesvar
        self.typedta.savevar = self.savevar
        self.typedta.savedir = self.savedir
        super().ok_pressed()


        