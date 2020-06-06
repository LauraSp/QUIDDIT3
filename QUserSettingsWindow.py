from QImpWindowBasics import *
from QSettings import *

class QUserSettingsWindow(QTclPopupWindow):
    def __init__(self, parent, title, is_modal=True):
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)

    def make_gui(self, title):
        self.setwintitle(title)
        
        row = 0
        blset_frame = self.make_label_frame(lrow=row, cspan=2, caption='Baseline method', padx=(5,5))
        
        irow = 0
        self.BLvar = tk.StringVar()
        self.stdbl = self.makeradio(parent=blset_frame, erow=irow, caption = "standard", variable=self.BLvar, value="standard")

        irow += 1
        self.oldbl = self.makeradio(parent=blset_frame, erow=irow, caption = "old", variable=self.BLvar, value="old")
        
        row += 1
        fitset_frame = self.make_label_frame(self, lrow=row, cspan=2, caption='Fit settings', padx=(5,5))

        innerrow = 0
        self.makelabel(fitset_frame, lrow=innerrow, caption='included in N fit:')
        
        innerrow += 1
        self.Cvar = tk.IntVar()
        self.C = self.makecheck(fitset_frame, erow=innerrow, caption='C centre', variable=self.Cvar)
        self.Bvar = tk.IntVar()
        self.B = self.makecheck(fitset_frame, erow=innerrow, ecol=1, caption='B centre', variable=self.Bvar)

        innerrow += 1
        self.Avar = tk.IntVar()
        self.A = self.makecheck(fitset_frame, erow=innerrow, caption='A centre', variable=self.Avar)

        self.Dvar = tk.IntVar()
        self.D = self.makecheck(fitset_frame, erow=innerrow, ecol=1, caption='D centre', variable=self.Dvar)

        innerrow += 1
        self.Xvar = tk.IntVar()
        self.X = self.makecheck(fitset_frame, erow=innerrow, caption='X centre', variable=self.Xvar)
        
        self.constvar = tk.IntVar()
        self.const = self.makecheck(fitset_frame, erow=innerrow, ecol=1, caption='add constant', variable=self.constvar)

        row = row + 1
        self.makebutton(erow=row, ecol = 0, cspan=2, caption="Restore defaults", cmd=self.restore_defaults, sticky=tk.EW, padx=(5,5))

        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)        

    def loaded (self):
        self.Cvar.set(QSettings.N_comp[0])
        self.Avar.set(QSettings.N_comp[1])
        self.Xvar.set(QSettings.N_comp[2])
        self.Bvar.set(QSettings.N_comp[3])
        self.Dvar.set(QSettings.N_comp[4])
        self.constvar.set(QSettings.N_comp[5])
        self.BLvar.set(QSettings.BLvar)

    def restore_defaults(self):
        self.Cvar.set(QSettings.ori_N_comp[0])
        self.Avar.set(QSettings.ori_N_comp[1])
        self.Xvar.set(QSettings.ori_N_comp[2])
        self.Bvar.set(QSettings.ori_N_comp[3])
        self.Dvar.set(QSettings.ori_N_comp[4])
        self.constvar.set(QSettings.ori_N_comp[5])
        self.BLvar.set(QSettings.ori_BLvar)

    
    def ok_pressed(self):
        QSettings.N_comp = np.array(
            (self.Cvar.get(), 
            self.Avar.get(), 
            self.Xvar.get(),
            self.Bvar.get(),
            self.Dvar.get(),
            self.constvar.get()))

        QSettings.BLvar = self.BLvar.get()

        QSettings.save_user_cfg()
        super().ok_pressed()

    

    