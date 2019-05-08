from QImpWindowBasics import *
from QSettings import *

class QPlotBatchPeakMapInpWindow(QTclPopupWindow):
    """Create window for Plot map input
    """
    def __init__(self, parent, title, plotmapinp, is_modal=True):
        self.sel_file = plotmapinp.map_file
        self.clims = plotmapinp.clims
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)

    def loaded(self):
        pass

    def make_gui(self, title):
        self.setwintitle(title)

        self.min_x0var = self.getvar(self.clims['$x_0 (cm^{-1})$'][0])
        self.max_x0var = self.getvar(self.clims['$x_0 (cm^{-1})$'][1])
        self.min_Ivar = self.getvar(self.clims['$I (cm^{-1})$'][0])
        self.max_Ivar = self.getvar(self.clims['$I (cm^{-1})$'][1])
        self.min_FWHMvar = self.getvar(self.clims['FWHM $(cm^{-1})'][0])
        self.max_FWHMvar = self.getvar(self.clims['FWHM $(cm^{-1})'][1])
        self.min_sigmavar = self.getvar(self.clims['sigma (-)'][0])
        self.max_sigmavar = self.getvar(self.clims['sigma (-)'][1])
        self.min_pareavar = self.getvar(self.clims['peak area $(cm^{-2})$'][0])
        self.max_pareavar = self.getvar(self.clims['peak area $(cm^{-2})$'][1])


        w=44
        row = 0
        filefr = self.make_label_frame(lrow=row, lcol=0, caption='Select file', cspan=2, padx=(5,5), pady=(5,5))
        
        irow = 0
        self.selfileentry = self.makeentry(filefr, lrow=irow, erow=irow, ecol=1, caption='Result file:', width=w)
        self.makebutton(filefr, erow=irow, ecol=2, caption='...', cmd=self.get_file, sticky=tk.E, padx=(0,5), pady=(0,5))
        self.set_entry_text(self.selfileentry, self.sel_file)

        row += 1
        setfr = self.make_label_frame(lrow=row, caption='Set Colour Scales', cspan=2, padx=(5,5), pady=(5,5))
        
        jrow = 0
        self.makelabel(setfr, caption='min', lrow=jrow, lcol=1, sticky=tk.EW)
        self.makelabel(setfr, caption='max', lrow=jrow, lcol=2, sticky=tk.EW)

        jrow += 1
        self.min_x0, self.max_x0 = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='peak pos. (cm-1): ',
                                                var1=self.min_x0var, var2 = self.max_x0var,
                                                padx=(5,5), pady=(5,2))

        jrow += 1
        self.min_I, self.max_I = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='peak height (cm-1): ',
                                                var1=self.min_Ivar, var2=self.max_Ivar,
                                                padx=(5,5))

        jrow += 1
        self.min_FWHM, self.max_FWHM = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='FWHM (cm-1): ',
                                                var1=self.min_FWHMvar, var2=self.max_FWHMvar,
                                                padx=(5,5))

        jrow += 1
        self.min_sigma, self.max_sigma = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='sigma (-): ',
                                                var1=self.min_sigmavar, var2=self.max_sigmavar,
                                                padx=(5,5))

        jrow += 1
        self.min_parea, self.max_parea = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='peak area (cm-2): ',
                                                var1=self.min_pareavar, var2=self.max_pareavar,
                                                padx=(5,5))

        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)



    def get_file(self):
        selfilevar = fd.askopenfilename(parent = self,
                    initialdir = QSettings.home,
                    title="Select file",
                    filetypes=(('CSV','*.CVS'),('CSV','*.csv'),('all','*.*'),('all','*.*')))
        self.set_entry_text(self.selfileentry, selfilevar)


    def ok_pressed(self):
        self.sel_file = self.selfileentry.get() 
        self.clims['$x_0 (cm^{-1})$'] =  self.value_tuple(self.min_x0var, self.max_x0var)
        self.clims['$I (cm^{-1})$'] = self.value_tuple(self.min_Ivar, self.max_Ivar)
        self.clims['FWHM $(cm^{-1})'] = self.value_tuple(self.min_FWHMvar, self.max_FWHMvar)
        self.clims['sigma (-)'] = self.value_tuple(self.min_sigmavar, self.max_sigmavar)
        self.clims['peak area $(cm^{-2})$'] = self.value_tuple(self.min_pareavar, self.max_pareavar)
        super().ok_pressed()

    def value_tuple(self, first, second):
        fg = first.get()
        sg = second.get()

        return (None if fg == "" else fg, None if sg == "" else sg)