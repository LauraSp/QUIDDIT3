# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 09:49:44 2019

@author: Laura
"""

from QImpWindowBasics import *
from QSettings import *

class QReviewInp:
    def __init__(self, spec_files, rev_file):
        self.spec_files = spec_files
        self.rev_file = rev_file
        

class QReviewInpWindow(QTclPopupWindow):
    def __init__(self, parent, title, reviewdta, is_modal=True):
        self.revdta = reviewdta
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)


    def loaded(self):
        pass
    
    def make_gui(self, title):
        self.setwintitle(title)
        
        self.spec_files = self.revdta.spec_files
        self.rev_file = self.revdta.rev_file
        
        w=44
        row = 0
        lfr = self.make_label_frame(lrow=row, lcol=0, caption='Select data for review', cspan=2, padx=(5,5), pady=(5,5))
        #tk.Label(self,
        #         text='Select files for baseline subtraction').grid(row=row, column=0, columnspan=3, sticky='w')
        
        irow = 0
        self.selfilesentry = self.makeentry(lfr, lrow=irow, erow=irow, ecol=1, caption="Select spectra*", width=w)
        self.makebutton(lfr, erow=irow, ecol=2, caption='...', cmd=self.get_spectra, sticky=tk.E, padx=(0,5))
        self.set_file_num()
        
        irow += 1
        self.revfileentry = self.makeentry(lfr, lrow=irow, erow=irow, ecol=1, caption="Review file", width=w)
        self.makebutton(lfr, erow=irow, ecol=2, caption='...', cmd=self.get_revfile, sticky=tk.E, padx=(0,5), pady=(0,5))

        row += 1
        self.makelabel(lrow=row, lcol=0, caption='*preferably baseline corrected', sticky=tk.NSEW, cspan=2)        
        row += 1
        self.add_std_buttons(okcol=1, cancelcol=0, row=row)
        
        
        
    def get_spectra(self):
        self.spec_files = fd.askopenfilenames(parent = self,
                                                initialdir = QSettings.home,
                                                title="Select spectra",
                                                filetypes=(('CSV','*.CSV'),('CSV','*.csv')))
        self.set_file_num()
        
    def get_revfile(self):
        revfile = fd.askopenfilename(parent=self,
                                       initialdir=QSettings.home,
                                       title='Select review file',
                                       filetypes=(('CSV','*.CSV'),('CSV','*.csv')))
        self.set_entry_text(self.revfileentry, revfile)
    
    def set_file_num(self):
        self.selfilesentry.configure(state=tk.NORMAL)
        self.set_entry_text(self.selfilesentry, "{} files".format(len(self.spec_files)))
        self.selfilesentry.configure(state=tk.DISABLED)
        
    def ok_pressed(self):
        self.revdta.spec_files = self.spec_files
        self.revdta.rev_file = self.revfileentry.get()
        super().ok_pressed()