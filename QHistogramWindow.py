from QImpWindowBasics import *
from QTclWindowBasics import *
from QCanvasHelperSingleHisto import *
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk



class QHistogramWindow (QTclPopupWindow):
    """histogram popup window
    """
    def __init__(self, parent, title, histo_data, ismodal=False):
        self.data = histo_data
        super().__init__(parent, title, ismodal)

    def loaded(self):
        ch = QCanvasHelperSingleHisto(self.histocanv)
        ch.add_histo_data(self.data)
        ch.display_first()
        self.set_min_max()


    def make_gui(self, title):
        self.setwintitle(title)
        
        row = 0
        fr = self.make_label_frame(lrow=row, cspan=4, caption="Histogram")

        irow = 0
        self.histofig = Figure(dpi=100)
        self.histocanv = self.make_mplcanvas(fr, fig=self.histofig, erow=irow, ecol=0, cspan=2)

        irow += 1
        toolbar_fr = self.make_frame(fr, erow=irow)
        self.toolbar = NavigationToolbar2Tk(self.histocanv, toolbar_fr)

        row += 1
        #self.makelabel(fr, lcol=1, lrow=irow, sticky=tk.W, caption='min: {}'.format(self.minvar.get()))
        self.min_entry = self.makeentry(erow=irow, lrow=irow, caption='min: ')

        #self.makelabel(fr, lcol=1, lrow=irow, sticky=tk.W, caption='max: {}'.format(self.maxvar.get()))
        self.max_entry = self.makeentry(erow=irow, lrow=irow, lcol=2, ecol=3, caption='max: ')

        row += 1
        self.add_std_buttons(row=row, dismisscol=0)

    def set_min_max(self):
        minval = np.round(np.min(self.data['data']), 2)
        maxval = np.round(np.max(self.data['data']), 2)

        self.min_entry.configure(state=tk.NORMAL)
        self.set_entry_text(self.min_entry, str(minval))
        self.min_entry.configure(state=tk.DISABLED)

        self.max_entry.configure(state=tk.NORMAL)
        self.set_entry_text(self.max_entry, str(maxval))
        self.max_entry.configure(state=tk.DISABLED)
        

