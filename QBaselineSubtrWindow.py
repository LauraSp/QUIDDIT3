# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 15:59:10 2019

@author: Laura
"""

from QImpWindowBasics import *
from QSettings import *

class QBaselineSubtrInp:
    def __init__(self, sel_files, res_dir):
        self.sel_files = sel_files
        self.res_dir = res_dir        

class QBaselineSubtrWindow(QTclPopupWindow):
    def __init__(self, parent, title, baselinedta, is_modal=True):
        self.bldta = baselinedta
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)


    def loaded(self):
        pass
    
    def make_gui(self, title):
        self.setwintitle(title)

        self.sel_files = self.bldta.sel_files
        self.res_dir = self.bldta.res_dir
        
        w=44
        row = 0
        lfr = self.make_label_frame(lrow=row, lcol=0, caption='Select files for baseline subtraction', cspan=2, padx=(5,5), pady=(5,5))
        
        irow = 0
        self.selfilesentry = self.makeentry(lfr, lrow=irow, erow=irow, ecol=1, caption="Select spectra", width=w)
        self.makebutton(lfr, erow=irow, ecol=2, caption='...', cmd=self.get_spectra, sticky=tk.E, padx=(0,5))
        self.set_file_num()
        
        irow += 1
        self.resdirentry = self.makeentry(lfr, lrow=irow, erow=irow, ecol=1, caption="Directory for corrected spectra", width=w)
        self.makebutton(lfr, erow=irow, ecol=2, caption='...', cmd=self.get_dir, sticky=tk.E, padx=(0,5), pady=(0,5))
        self.set_entry_text(self.resdirentry, self.res_dir)
        
        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)
        
        
        
    def get_spectra(self):
        self.sel_files = fd.askopenfilenames(parent = self,
                                                initialdir = QSettings.userhome,
                                                title="Select spectra",
                                                filetypes=(('CSV','*.CSV'),('CSV','*.csv')))
        self.set_file_num()
        
    def get_dir(self):
        targetdir = fd.askdirectory(parent=self,
        initialdir=QSettings.userhome,
        title='Select directory for individual spectra')
        self.set_entry_text(self.resdirentry, targetdir)
    
    def set_file_num(self):
        self.selfilesentry.configure(state=tk.NORMAL)
        self.set_entry_text(self.selfilesentry, "{} files".format(len(self.sel_files)))
        self.selfilesentry.configure(state=tk.DISABLED)
        
    def ok_pressed(self):
        self.bldta.sel_files = self.sel_files
        self.bldta.res_dir = self.resdirentry.get()
        super().ok_pressed()
