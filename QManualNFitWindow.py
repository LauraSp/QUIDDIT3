from QTclPopupWindow import *
from QSettings import *
from QCanvasHelperManualNFit import *

from matplotlib.figure import Figure


class QManualNFitWindow(QTclPopupWindow):
    def __init__(self, parent, title, spectrumfiles, is_modal=True):
        self.specfiles = spectrumfiles
        super().__init__(parent, title, is_modal)

    def loaded(self):
        self.canhelper = QCanvasHelperManualNFit(self.canvas)

        
    def make_gui(self, title):
        self.setwintitle(title)

        self.age = self.getvar(2700.)

        w = 24
        row = 0
        filefr = self.make_label_frame(lrow=row, lcol=0, caption='Select files', cspan=3, padx=(5,5), pady=(5,5))

        irow = 0
        self.specfileentry = self.makeentry(filefr, lrow=irow, erow=irow, ecol=1, caption='Spectra:', width=w)
        self.makebutton(filefr, erow=irow, ecol=2, caption='...', cmd=self.get_files, sticky=tk.E, padx=(0,5), pady=(0,5))
        self.set_file_num()

        irow += 1
        self.ageentry = self.makeentry(filefr, lrow=irow, erow=irow, caption = 'Age:', textvariable=self.age)
        self.makelabel(filefr, lrow=irow, lcol=2, caption='(Ma)')

        irow += 1
        self.loadbu = self.makebutton(filefr, erow=irow, ecol=0, caption='Load', sticky=tk.E, cmd=self.load_data, padx=(5,5), pady=(5,5))
        self.loadbu.configure(state=tk.DISABLED)

        row += 1
        canvfr = self.make_label_frame(lrow=row, lcol=0, caption='Manual Fit', cspan=3, padx=(5,5), pady=(5,5))
        jrow=0
        self.fig = Figure(dpi=100)
        self.canvas = self.make_mplcanvas(canvfr, fig=self.fig, erow=jrow, ecol=0)


        row += 1
        self.makebutton(erow=row, ecol=2, caption='Next', cmd=self.display_next, padx=(5,5), pady=(5,5), sticky=tk.E)
        self.makebutton(erow=row, ecol=0, caption='Previous', cmd=self.display_prev, padx=(5,5), pady=(5,5), sticky=tk.W)

        #row += 1
        self.add_std_buttons(row=row, dismisscol=1)

    def get_files(self):
        self.specfiles = fd.askopenfilenames(parent = self,
                    initialdir = QSettings.userhome,
                    title="Select files",
                    filetypes=(('CSV','*.CVS'),('CSV','*.csv'),('all','*.*'),('all','*.*')))
        self.set_file_num()
        if len(self.specfiles) >= 1:
            self.loadbu.configure(state=tk.NORMAL)
        

    def set_file_num(self):
        self.specfileentry.configure(state=tk.NORMAL)
        self.set_entry_text(self.specfileentry, '{} files'.format(len(self.specfiles)))
        self.specfileentry.configure(state=tk.DISABLED)


    def load_data(self):
        self.canhelper.add_data(self.specfiles, self.age)
        self.canhelper.display_first()


    def display_next(self):
        if self.canhelper != None:
            self.canhelper.display_next()

    def display_prev(self):
        if self.canhelper != None:
            self.canhelper.display_previous()
        

