from QImpWindowBasics import *
from QSettings import *

class QUserSettingsWindow(QTclPopupWindow):
    def __init__(self, parent, title, is_modal=True):
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)

    def make_gui(self, title):
        self.setwintitle(title)

        row = 0
        blset_frame = self.make_label_frame(
            lrow=row,
            cspan=2,
            caption='Baseline method',
            padx=(5, 5)
            )

        irow = 0
        # variables already created in loaded(); just create widgets
        self.stdbl = self.makeradio(
            parent=blset_frame,
            erow=irow,
            caption="standard",
            variable=self.BLvar,
            value="standard"
            )

        irow += 1
        self.oldbl = self.makeradio(
            parent=blset_frame,
            erow=irow,
            caption="difference",
            variable=self.BLvar,
            value="difference"
            )

        row += 1
        fitset_frame = self.make_label_frame(
            self,
            lrow=row,
            cspan=2,
            caption='Fit settings',
            padx=(5, 5)
            )

        innerrow = 0
        self.makelabel(fitset_frame,
                       lrow=innerrow, caption='included in N fit:')

        innerrow += 1
        self.C = self.makecheck(
            fitset_frame,
            erow=innerrow,
            caption='C centre',
            variable=self.Cvar
            )
        self.B = self.makecheck(
            fitset_frame,
            erow=innerrow,
            ecol=1,
            caption='B centre',
            variable=self.Bvar
            )

        innerrow += 1
        self.A = self.makecheck(
            fitset_frame,
            erow=innerrow,
            caption='A centre',
            variable=self.Avar
            )

        self.D = self.makecheck(
            fitset_frame,
            erow=innerrow,
            ecol=1,
            caption='D centre',
            variable=self.Dvar
            )

        innerrow += 1
        self.X = self.makecheck(
            fitset_frame,
            erow=innerrow,
            caption='X centre',
            variable=self.Xvar
            )

        self.const = self.makecheck(
            fitset_frame,
            erow=innerrow,
            ecol=1,
            caption='add constant',
            variable=self.constvar
            )

        row = row + 1
        otherset_frame = self.make_label_frame(
            self,
            lrow=row,
            cspan=2,
            caption='Other settings',
            padx=(5, 5)
            )

        innerrow = 0

        # new setting: plot spectra during deconvolution
        self.plotdeconv = self.makecheck(
            otherset_frame,
            erow=innerrow,
            caption='plot during deconvolution',
            variable=self.plotdeconvvar
            )

        innerrow += 1
        # new setting: long print output
        self.longprint = self.makecheck(
            otherset_frame,
            erow=innerrow,
            caption='long print output',
            variable=self.longprintvar
            )

        row = row + 1
        self.makebutton(
            erow=row,
            ecol=0,
            cspan=2,
            caption="Restore defaults",
            cmd=self.restore_defaults,
            sticky=tk.EW,
            padx=(5, 5)
            )

        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)        

    def loaded(self):
        # create tk variables early so they exist when this method runs
        self.BLvar = tk.StringVar()
        self.Cvar = tk.IntVar()
        self.Bvar = tk.IntVar()
        self.Avar = tk.IntVar()
        self.Dvar = tk.IntVar()
        self.Xvar = tk.IntVar()
        self.constvar = tk.IntVar()
        # whether to show spectra during deconvolution:
        self.plotdeconvvar = tk.IntVar()
        # whether to show detailed deconvolution results:
        self.longprintvar = tk.IntVar()

        # initialise from settings
        self.Cvar.set(QSettings.N_comp[0])
        self.Avar.set(QSettings.N_comp[1])
        self.Xvar.set(QSettings.N_comp[2])
        self.Bvar.set(QSettings.N_comp[3])
        self.Dvar.set(QSettings.N_comp[4])
        self.constvar.set(QSettings.N_comp[5])
        self.BLvar.set(QSettings.BLvar)
        self.plotdeconvvar.set(1 if QSettings.plot_during_deconv else 0)
        self.longprintvar.set(1 if QSettings.long_print_output else 0)

    def restore_defaults(self):
        self.Cvar.set(QSettings.ori_N_comp[0])
        self.Avar.set(QSettings.ori_N_comp[1])
        self.Xvar.set(QSettings.ori_N_comp[2])
        self.Bvar.set(QSettings.ori_N_comp[3])
        self.Dvar.set(QSettings.ori_N_comp[4])
        self.constvar.set(QSettings.ori_N_comp[5])
        self.BLvar.set(QSettings.ori_BLvar)
        self.plotdeconvvar.set(1 if QSettings.ori_plot_during_deconv else 0)
        self.longprintvar.set(1 if QSettings.ori_long_print_output else 0)

    def ok_pressed(self):
        QSettings.N_comp = np.array(
            (self.Cvar.get(),
            self.Avar.get(),
            self.Xvar.get(),
            self.Bvar.get(),
            self.Dvar.get(),
            self.constvar.get()))

        QSettings.BLvar = self.BLvar.get()
        QSettings.plot_during_deconv = bool(self.plotdeconvvar.get())
        QSettings.long_print_output = bool(self.longprintvar.get())

        QSettings.save_user_cfg()
        super().ok_pressed()
