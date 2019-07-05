from QImpWindowBasics import *
from QSettings import *

class QPeakfitInp:
    def __init__(self, name, peak, result, selectedfiles):
        self.name = name
        self.peak = peak
        self.result = result
        self.selectedfiles = selectedfiles


class QPeakfitInpWindow(QTclPopupWindow):
    """Input Window for batch peak fitting"""
    def __init__(self, parent, title, peakfitinp, is_modal=True):
        self.pkdta = peakfitinp
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)
        
    def make_gui(self, title):
        self.setwintitle(title)

        self.namevar = self.getvar(self.pkdta.name)
        self.peakvar = self.getvar(self.pkdta.peak)
        self.resultvar = self.getvar(self.pkdta.result)
        self.selectedfilesvar = self.pkdta.selectedfiles

        row = 0
        myfr = self.make_label_frame(caption='Please enter data for peak fitting', cspan=2, padx=(5,5), pady=(5,5))
        
        irow = 0
        self.sample_name = self.makeentry(myfr, lrow=irow, erow=irow,
                                            caption="Sample name",
                                            width=24,
                                            textvariable=self.namevar)

        irow += 1 
        self.selected_peak = self.makeentry(myfr, lrow=irow, erow=irow,
                                                   caption='Approx. wavenumber',
                                                   width=24,
                                                   textvariable=self.peakvar)
        self.makelabel(myfr, lrow=irow, lcol=2, caption='(cm-1)', sticky=tk.W)

        irow += 1
        self.result_name = self.makeentry(myfr, erow=irow, lrow=irow,
                                            caption='Name for results file: ',
                                            width=24,
                                            textvariable=self.resultvar)
        
        self.makelabel(myfr, lrow=irow, lcol=2, caption='.csv', sticky=tk.W)
        
        irow += 1
        self.spectrac = self.makeentry(myfr, lrow=irow, erow=irow, ecol=1, caption="Spectra", width=24)
        self.set_file_num()
        self.makebutton(myfr, erow=irow, ecol=2, caption='...', cmd=self.get_filenames, pady=(0,5))

        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)

    def loaded(self):
        pass


    def ok_pressed(self):
        self.pkdta.name = self.namevar.get()
        self.pkdta.peak = self.peakvar.get()
        self.pkdta.result = self.resultvar.get()
        self.pkdta.selectedfiles = self.selectedfilesvar
        super().ok_pressed()

    def set_file_num(self):
        self.spectrac.configure(state=tk.NORMAL)
        self.set_entry_text(self.spectrac, "{} files".format(len(self.selectedfilesvar)))
        self.spectrac.configure(state=tk.DISABLED)

    def get_filenames(self):
        self.selectedfilesvar = fd.askopenfilenames(parent = self,
            initialdir = QSettings.userhome,
            title="Select spectra",
            filetypes=(('CSV','*.CSV'),('CSV','*.csv')))
        self.set_file_num()
