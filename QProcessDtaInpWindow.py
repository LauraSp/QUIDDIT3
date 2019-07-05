from QImpWindowBasics import *
from QSettings import *

class QProcessDtaInp:
    def __init__(self, name, result, review, age, selfiles):
        self.name = name
        self.result = result
        self.review = review
        self.age = age
        self.selectedfiles = selfiles

    def clone(self):
        return QProcessDtaInp(self.name,
            self.result,
            self.review,
            self.age,
            self.selectedfiles)

class QProcessDtaInpWindow(QTclPopupWindow):

    def __init__(self, parent, title, processdtainp, is_modal=True):
        self.prcdta = processdtainp
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)


    def loaded(self):
        pass

    def make_gui(self, title):
        self.setwintitle(title)

        row = 0
        myfr = self.make_label_frame(caption="Please enter sample name and mantle storage duration", 
                                     cspan=2,
                                     padx=(5,5), pady=(5,5))

        self.namevar = self.getvar(self.prcdta.name)
        self.resultvar = self.getvar(self.prcdta.result)
        self.reviewvar = self.getvar(self.prcdta.review)
        self.agevar = self.getvar(self.prcdta.age)
        self.selectedfilesvar = self.prcdta.selectedfiles

        irow = 0
        self.sample_name = self.makeentry(myfr,
                                          lrow=irow, erow=irow,
                                          caption="Sample name",
                                          width=24,
                                          textvariable=self.namevar)
        #self.sample_name.bind('<Tab>', self.on_input)
        #self.sample_name.focus_force()
        
        irow += 1
        self.result_name = self.makeentry(myfr,
                                        erow=irow, lrow=irow,
                                        caption='Name for results file: ',
                                        width=24,
                                        textvariable=self.resultvar)

        self.makelabel(myfr, lrow=irow, lcol=2, caption=".csv", sticky=tk.W)

        irow += 1
        self.review_name = self.makeentry(myfr,
                                        erow=irow, lrow=irow,
                                        caption='Name for review file: ',
                                        width=24,
                                        textvariable=self.reviewvar)

        self.makelabel(myfr, lrow=irow, lcol=2, caption=".csv", sticky=tk.W)

        irow += 1
        self.age = self.make_double_entry(myfr,
                                        erow=irow, lrow=irow,
                                        caption='Storage duration',
                                        width=24,
                                        textvariable=self.agevar)
        self.makelabel(myfr, lrow=irow, lcol=2, caption="(Ma)", sticky=tk.W)

        irow += 1
        self.spectrac = self.makeentry(myfr, lrow=irow, erow=irow, ecol=1, caption="Spectra", width=24)
        self.set_file_num()
        self.makebutton(myfr, erow=irow, ecol=2, caption='...', cmd=self.get_filenames, pady=(0,5))

        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)

    def ok_pressed(self):
        self.prcdta.name = self.namevar.get()
        self.prcdta.result = self.resultvar.get()
        self.prcdta.review = self.reviewvar.get()
        self.prcdta.age = self.agevar.get()
        self.prcdta.selectedfiles = self.selectedfilesvar
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