import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
import tkinter.filedialog as fd

from QTclPopupWindow import *
import QTwoStageModelCalc as ts
from QSettings import *


class QTwoStageModelInp:
    def __init__(self, duration, core_NT, core_agg, rim_NT, rim_agg):
        self.duration = duration
        self.cNT = core_NT
        self.cagg = core_agg
        self.rNT = rim_NT
        self.ragg = rim_agg

class QTwostageModelWindow(QTclPopupWindow):
    def __init__(self, parent, title, twostage_inp, is_modal=False):
        self.dresult = "NONE"
        self.durvar = self.getvar(twostage_inp.duration)
        self.cNTvar = self.getvar(twostage_inp.cNT)
        self.caggvar = self.getvar(twostage_inp.cagg)
        self.rNTvar = self.getvar(twostage_inp.rNT)
        self.raggvar = self.getvar(twostage_inp.ragg)
        super().__init__(parent, title, is_modal)

    def loaded(self):
        pass

    def make_gui(self, title):
        self.setwintitle(title)

        row = 0
        setfr = self.make_label_frame(lrow=row, caption='Enter data for core and rim', padx=(5,2), pady=(5,5))

        irow=0
        self.makelabel(setfr, lrow=irow, lcol=1, caption='core', sticky=tk.EW)
        self.makelabel(setfr, lrow=irow, lcol=2, caption='rim', sticky=tk.EW)

        irow += 1
        self.cNT, self.rNT = self.make_double_entrypair(setfr, lrow=irow, e1row=irow, e2row=irow,
                                        caption='[NT]: ',
                                        var1=self.cNTvar, var2 = self.rNTvar,
                                        padx=(5,5), pady=(5,2))
        self.makelabel(setfr, lrow=irow, lcol=3, caption='(ppm)', sticky=tk.W)

        irow += 1
        self.cNT, self.rNT = self.make_double_entrypair(setfr, lrow=irow, e1row=irow, e2row=irow,
                                        caption='[NB]/[NT]: ',
                                        var1=self.caggvar, var2 = self.raggvar,
                                        padx=(5,5), pady=(2,2))
        self.makelabel(setfr, lrow=irow, lcol=3, caption='(-)', sticky=tk.W)

        irow += 1
        self.make_double_entry(setfr, lrow=irow, erow=irow, caption='Total duration: ',
                                textvariable=self.durvar, padx=(2,2), pady=(2,5))
        self.makelabel(setfr, lrow=irow, lcol=2, caption='(Ma)', sticky=tk.W)

        irow += 1
        self.makebutton(setfr, erow=irow, ecol=1, cmd=self.calc_model, caption='Calculate')
        self.savebutton = self.makebutton(setfr, erow=irow, ecol=2, cmd=self.save_to_file, caption='Save results to file')
        self.savebutton.config(state=tk.DISABLED)


        plotfr = self.make_label_frame(lrow=row, lcol=2, caption='Model', pady=(5,5))
        self.fig = Figure(dpi=100)
        jrow = 0
        self.canv = self.make_mplcanvas(plotfr, fig=self.fig, erow=jrow)

        jrow +=1
        toolbar_fr = self.make_frame(plotfr, erow=jrow)
        self.toolbar = NavigationToolbar2Tk(self.canv, toolbar_fr)
        
        row += 1
        self.add_std_buttons(row=row, dismisscol=0)


    def calc_model(self):
        for ax in self.fig.get_axes():
            self.fig.delaxes(ax)

        self.durations, self.temps1, self.temps2 = ts.model(self.durvar.get(),
                                                    self.cNTvar.get(), self.caggvar.get(),
                                                    self.rNTvar.get(), self.raggvar.get())
        sp = self.fig.add_subplot(111)
        sp.plot(self.durations, self.temps1, 'r.', label='core')
        sp.plot(self.durations, self.temps2, 'b.', label='rim')
        sp.set(ylim=(1000, 1500), xlim=(0, float(self.durvar.get())),
               xlabel='Duration of first anneal (Ma)',
               ylabel ='Temperature ($\mathregular{^{\circ}}$C)')
        sp.legend(loc='best')

        self.canv.draw()
        self.savebutton.config(state=tk.NORMAL)

    def save_to_file(self):
        fname = fd.asksaveasfilename(title='Save results to...', initialdir=QSettings.home, defaultextension='.csv')
        if fname != '':
            data = np.column_stack((self.durations, self.temps1, self.temps2))

            header = 'two-stage model with {} Ma; core: NT {} agg {}; rim: NT {} ragg {}\nduration of first anneal, T_core, T_rim'.format(self.durvar.get(),
                                                                        self.cNTvar.get(), self.caggvar.get(), self.rNTvar.get(), self.raggvar.get())
            np.savetxt(fname, data, delimiter=',', header=header)
        else:
            raise NameError('No file created, results not saved.')
        