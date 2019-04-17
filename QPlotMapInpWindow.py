from QImpWindowBasics import *
from QSettings import *
        
class QPlotMapInp:
    def __init__(self, map_file, clims):
        """Data type for QPlotMapInpWindow.
        """
        self.map_file = map_file
        self.clims = clims

class QPlotMapInpWindow(QTclPopupWindow):
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
        
        self.min_NTvar = self.getvar(self.clims['$[N_T]$ (ppm)'][0])
        self.max_NTvar = self.getvar(self.clims['$[N_T]$ (ppm)'][1])
        self.min_NAvar = self.getvar(self.clims['$[N_A]$ (ppm)'][0])
        self.max_NAvar = self.getvar(self.clims['$[N_A]$ (ppm)'][1])
        self.min_NBvar = self.getvar(self.clims['$[N_B]$ (ppm)'][0])
        self.max_NBvar = self.getvar(self.clims['$[N_B]$ (ppm)'][1])
        self.min_aggvar = self.getvar(self.clims['$[N_B]/[N_T]$'][0])
        self.max_aggvar = self.getvar(self.clims['$[N_B]/[N_T]$'][1])
        self.min_Tvar = self.getvar(self.clims[r'$T (^{\circ}C)$'][0])
        self.max_Tvar = self.getvar(self.clims[r'$T (^{\circ}C)$'][1])
        self.min_pareavar = self.getvar(self.clims['platelet peak area $(cm^{-2})$'][0])
        self.max_pareavar = self.getvar(self.clims['platelet peak area $(cm^{-2})$'][1])
        self.min_pposvar = self.getvar(self.clims['platelet peak position $(cm^{-1})$'][0])
        self.max_pposvar = self.getvar(self.clims['platelet peak position $(cm^{-1})$'][1])
        self.min_pwidthvar = self.getvar(self.clims['platelet peak width $(cm^{-1})$'][0])
        self.max_pwidthvar = self.getvar(self.clims['platelet peak width $(cm^{-1})$'][1])
        self.min_psymvar = self.getvar(self.clims['platelet peak symmetry $(cm^{-1})$'][0])
        self.max_psymvar = self.getvar(self.clims['platelet peak symmetry $(cm^{-1})$'][1])
        self.min_I3107var = self.getvar(self.clims['I(3107) $(cm^{-2})$'][0])
        self.max_I3107var = self.getvar(self.clims['I(3107) $(cm^{-2})$'][1])

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
        self.min_NT, self.max_NT = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='[NT] (ppm): ',
                                                var1=self.min_NTvar, var2 = self.max_NTvar,
                                                padx=(5,5), pady=(5,2))

        jrow += 1
        self.min_NA, self.max_NA = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='[NA] (ppm): ',
                                                var1=self.min_NAvar, var2=self.max_NAvar,
                                                padx=(5,5))

        jrow += 1
        self.min_NB, self.max_NB = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='[NB] (ppm): ',
                                                var1=self.min_NBvar, var2=self.max_NBvar,
                                                padx=(5,5))

        jrow += 1
        self.min_agg, self.max_agg = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='[NB]/[NT] (frac): ',
                                                var1=self.min_aggvar, var2=self.max_aggvar,
                                                padx=(5,5))

        jrow += 1
        self.min_T, self.max_T = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption='T (deg. C): ',
                                                var1=self.min_Tvar, var2=self.max_Tvar,
                                                padx=(5,5))

        jrow += 1
        self.min_ppos, self.max_ppos = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption="B' pos. (cm-1): ",
                                                var1=self.min_pposvar, var2=self.max_pposvar,
                                                padx=(5,5))

        jrow += 1
        self.min_parea, self.max_parea = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption="B' area (cm-2): ",
                                                var1=self.min_pareavar, var2=self.max_pareavar,
                                                padx=(5,5))

        jrow += 1
        self.min_pwidth, self.max_pwidth = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption="B' width (cm-1): ",
                                                var1=self.min_pwidthvar, var2=self.max_pwidthvar,
                                                padx=(5,5))
        
        jrow += 1
        self.min_psym, self.max_psym = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption="B' sym (cm-1): ",
                                                var1=self.min_psymvar, var2=self.max_psymvar,
                                                padx=(5,5))

        jrow += 1
        self.min_I3107, self.max_I3107 = self.make_double_entrypair(setfr, lrow=jrow, e1row=jrow, e2row=jrow,
                                                caption="3107 area (cm-1): ",
                                                var1=self.min_I3107var, var2=self.max_I3107var,
                                                padx=(5,5), pady=(2,5))

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
        self.clims['$[N_T]$ (ppm)'] =  self.value_tuple(self.min_NTvar, self.max_NTvar) # (self.min_NTvar.get(), self.max_NTvar.get())
        self.clims['$[N_A]$ (ppm)'] = self.value_tuple(self.min_NAvar, self.max_NAvar)
        self.clims['$[N_B]$ (ppm)'] = self.value_tuple(self.min_NBvar, self.max_NBvar)
        self.clims['$[N_B]/[N_T]$'] = self.value_tuple(self.min_aggvar, self.max_aggvar)
        self.clims[r'$T (^{\circ}C)$'] = self.value_tuple(self.min_Tvar, self.max_Tvar)
        self.clims['platelet peak area $(cm^{-2})$'] = self.value_tuple(self.min_pareavar, self.max_pareavar)
        self.clims['platelet peak position $(cm^{-1})$'] = self.value_tuple(self.min_pposvar, self.max_pposvar)
        self.clims['platelet peak width $(cm^{-1})$'] = self.value_tuple(self.min_pwidthvar, self.max_pwidthvar)
        self.clims['platelet peak symmetry $(cm^{-1})$'] = self.value_tuple(self.min_psymvar, self.max_psymvar)
        self.clims['I(3107) $(cm^{-2})$'] = self.value_tuple(self.min_I3107var, self.max_I3107var)
        super().ok_pressed()

    def value_tuple(self, first, second):
        fg = first.get()
        sg = second.get()

        return (None if fg == "" else fg, None if sg == "" else sg)