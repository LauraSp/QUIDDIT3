# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 11:09:40 2019

@author: Laura
"""

import os
import sys
import webbrowser
from QImpWindowBasics import *
import numpy as np

import matplotlib
#matplotlib.use('TkAgg')
#Papi: Läuft bei mir auf einen LoadError
#from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

#alle popupwindows have to be imported
from QHistogramWindow import *
from QAboutWindow import *
from QAskSpectraWindow import *
from QAskFileWindow import *
from QENVIconversionWindow import *
from QProcessDtaInpWindow import *
from QPeakfitInpWindow import *
from QReviewInpWindow import*
from QPlotMapInpWindow import *
from QBaselineSubtrWindow import *
from QUserSettingsWindow import *
from QTwostageModelWindow import *
from QSettings import *
from QCanvasHelperSpectrum import *
from QCanvasHelperLineResult import *
from QCanvasHelperSingleHisto import *
from QCanvasHelperMultiHisto import *
from QCanvasHelperMap import *
from QCanvasHelperDeconvReview import *
import QBaseline as bl
import QGeneralDeconvolution as decon


class MainWindow(QTclBaseWindow):
    """Main window for QUIDDIT
    """
    def make_gui(self, title):
        """ create the gui
        """
        self.canhelper = None
        self.setwintitle(title)

        #self.set_defaults()

        #Making the main menu
        menubar = self.create_menu_bar()
        self.master.config(menu=menubar)

        # making the controls
        row = 0
        self.main_fig = Figure(dpi=100)
        self.ax = self.main_fig.add_subplot(111)
        self.main_fig.gca().invert_xaxis()
        self.main_fig.suptitle('QUIDDIT')
        self.IIa_spec = np.loadtxt(QSettings.IIa_path, delimiter=',')
        self.ax.plot(self.IIa_spec[:, 0], self.IIa_spec[:, 1], 'k-')

        self.main_canvas = self.make_mplcanvas(fig=self.main_fig, erow=row, ecol=0, cspan=4)

        self.message = tk.Text(self, state='disabled', relief=STDRELIEF)
        self.message.grid(row=row, column=4, columnspan=2, sticky=tk.NSEW, padx=5)
        scrl_bar = tk.Scrollbar(self, command=self.message.yview)
        scrl_bar.grid(row=row, column=6, sticky=tk.NSEW)
        self.message['yscrollcommand'] = scrl_bar.set

        row += 1

        toolbar_frame = tk.Frame(self)
        toolbar_frame.grid(row=row, column=1, sticky=tk.W)
        #Papi: den habe ich nicht self.toolbar = NavigationToolbar2TkAgg(self.main_canvas, toolbar_frame)
        self.toolbar = NavigationToolbar2Tk(self.main_canvas, toolbar_frame)
        #self.position = 0

        self.back_button = self.makebutton(erow=row, ecol=0, caption='Previous',
                                           cmd=self.display_prev,
                                           state=tk.DISABLED, padx=5, pady=5)
        self.next_button = self.makebutton(erow=row, ecol=3, caption='Next',
                                           cmd=self.display_next,
                                           state=tk.DISABLED, padx=5, pady=5, sticky='e')

        self.histo_button = self.makebutton(erow=row, ecol=2, caption='Histogram',
                                           cmd=self.histo_popup,
                                           state=tk.DISABLED, padx=5, pady=5, sticky='e')

        for i in range(row):
            self.rowconfigure(i, weight=1, pad=5)
        self.rowconfigure(row, weight=0, pad=5)

        for j in range(6):
            self.columnconfigure(j, weight=1, pad=5)

        self.pack(fill=tk.BOTH, expand=tk.YES)


    def loaded(self):
        """Das Window wurde aufgebaut
        """
        QSettings.read_user_cfg()
        self.print_message(self.message, 'Welcome to QUIDDIT v. {}\n'.format(QSettings.version))
        self.std = QSettings.std
        self.prcdta = QProcessDtaInp('','','',2900,[])
        self.pkfitdta = QPeakfitInp('', 3107., '', [])
        self.convenvidta = QENVIconversionInp('','','')
        self.bldata = QBaselineSubtrInp([], '')
        self.revdta = QReviewInp([], '')
        self.peakrevdta = QReviewInp([], '')
        self.mapinp = QPlotMapInp('', QSettings.MAPCLIMS)
        self.specs = []
        self.lineresultfile = ''
        self.historesultfile = ''
        self.twostage_inp = QTwoStageModelInp(2700, 1600, 0.82, 400, 0.2)

    def print_message(self, textwidget, text):
        """print text to textwidget
        """
        textwidget['state'] = 'normal'
        textwidget.insert('end', text+'\n')
        textwidget['state'] = 'disabled'
        textwidget.see('end')

    #Papi: Was ist das?
    #def restore_defaults(variables):
    #   for var in variables:
    
    def set_defaults(self):
        """Set all the defaults
        """
        self.home = QSettings.home
        self.N_comp = QSettings.N_comp
        self.file_count = self.getvar('')
        self.github_url = 'https://github.com/LauraSp/QUIDDIT'
        self.namevar = self.getvar('')
        self.resultvar = self.getvar('')
        self.reviewvar = self.getvar('')
        self.agevar = self.getvar(2900)
        self.peakvar = self.getvar(3107.0)
        self.c_NT_var = self.getvar(0.)
        self.r_NT_var = self.getvar(0.)
        self.c_agg_var = self.getvar(0.)
        self.r_agg_var = self.getvar(0.)
        self.plotmode = self.getvar('')
        self.minvar = self.getvar(0.)
        self.maxvar = self.getvar(1.)
        self.peak = self.getvar(0)


    def create_menu_bar(self):
        """ Fill the menu
        """
        menubar = tk.Menu(self)
        filemenuopt = {'Convert ENVI file...':self.convert_ENVI,
                        'Open spectra':self.plot_spectra,
                       'Exit':self.click_exit}
        filemenu = self.make_menu(menubar, 'File', filemenuopt)
        filemenu.insert_separator(1)

        optmenuopt = {'User settings':self.change_user_settings}
                      #'Custom baseline':self.do_nothing}
        self.make_menu(menubar, 'Settings', optmenuopt)

        baselinemenuopt = {'Correct baseline':self.baseline}
        self.make_menu(menubar, 'Baseline', baselinemenuopt)

        procmenuopt = {'General Deconvolution':self.process_data,
                       'Batch Peak Fit': self.peak_fit}
        self.make_menu(menubar, 'Process', procmenuopt)

        revmenuopt = {'Review General Deconvolution':self.review_deconv,
                    'Review Batch Peak Fit':self.review_peakf}
        self.make_menu(menubar, 'Review', revmenuopt)

        plotmenuopt = {'Plot spectra':self.plot_spectra,
                       'Plot line results':self.plot_ls,
                       'Plot map results':self.plot_map,
                       'Plot histograms': self.plot_histogram,
                       'Quadplot':self.plot_quadplot}
        self.make_menu(menubar, 'Plot', plotmenuopt)
        
        manualmenuopt = {'Fit N region manually': self.man_N_fit,
                         'Fit peak manually': self.man_peakfit}
        self.make_menu(menubar, 'Manual fit', manualmenuopt)
        
        manualmenuopt = {'Model N aggregation': self.twostage_model}
        self.make_menu(menubar, '2-stage modelling', manualmenuopt)

        helpmenuopt = {'GitHub':(lambda s=self: webbrowser.open(QSettings.github_url)),
                       'About':self.about}
        helpmenu = self.make_menu(menubar, 'Help', helpmenuopt)
        helpmenu.insert_separator(1)

        return menubar

    def histo_popup(self):
        if self.canhelper != None:
            histo = self.canhelper.get_current_histo_data()
            histopop = QHistogramWindow(mw, "Histogram", histo)

    
    def convert_ENVI(self):
        QENVIconversionWindow(self, "ENVI Conversion", self.convenvidta)

    def change_user_settings(self):
        QUserSettingsWindow(mw, "User settings")

    def do_nothing(self):
        pass

    def click_exit(self):
        try:
            mwin = QTclMessageWindow(mw, "QUIDDIT Question", "Just to make sure ...", "Do you really want to quit QUIDDIT?")
            if mwin.dresult == 'OK':
                self.root.destroy()
        except Exception as e:
            mwin = QTclMessageWindow(mw, "QUODDIT Error", "An unhandled error has occured", 
                "The original message was: {}".format(str(e)),
                 e)

    def display_next(self):
        if self.canhelper != None:
            self.canhelper.display_next()

    def display_prev(self):
        if self.canhelper != None:
            self.canhelper.display_previous()
        
    def baseline(self):
        bl_window = QBaselineSubtrWindow(self, "Baseline subtraction", self.bldata)
        if bl_window.dresult =='OK':
            self.bldta = bl_window.bldta
            i = 1
            for filename in self.bldta.sel_files:
                self.print_message(self.message, 'Baseline removal {}/{}:\n{}'.format(i, len(self.bldta.sel_files), filename.split('/')[-1]))
                bl.remove_baseline(filename, self.bldta.res_dir)
                i += 1
            self.print_message(self.message, '\nBaseline removal complete.')

    def plot_spectra(self):
        spec_window = QAskSpectraWindow(self, "Select Spectra", self.specs)
        if spec_window.dresult =='OK':
            self.specs = spec_window.spec_files
            ch = QCanvasHelperSpectrum(self.main_canvas)
            ch.add_spectra_files(self.specs)
            ch.display_first()
            self.set_can_helper(ch)


    def set_can_helper(self, ch):
        self.canhelper = ch
        if ch==None:
            self.next_button.config(state=tk.DISABLED)
            self.back_button.config(state=tk.DISABLED)
            self.histo_button.config(state=tk.DISABLED)
        else:
            self.next_button.config(state=tk.NORMAL)
            self.back_button.config(state=tk.NORMAL)
            if type(ch) is QCanvasHelperMap:
                self.histo_button.config(state=tk.NORMAL)
            else:
                self.histo_button.config(state=tk.DISABLED)


    def plot_ls(self):
        resfile_window = QAskFileWindow(self, "File Selection", 'Select linescan results', self.lineresultfile)
        if resfile_window.dresult=='OK':
            self.lineresultfile = resfile_window.sel_file
            ch = QCanvasHelperLineResult(self.main_canvas)
            ch.add_line_data(self.lineresultfile)
            ch.display_first()
            
    def plot_map(self):
        resfile_window = QPlotMapInpWindow(self, "Input for map plotting", self.mapinp)
        if resfile_window.dresult=='OK':
            self.mapinp.map_file = resfile_window.sel_file
            self.historesultfile = resfile_window.sel_file
            clims = resfile_window.clims
            ch = QCanvasHelperMap(self.main_canvas)
            ch.add_map_file(self.mapinp.map_file, clims)
            self.print_message(self.message, 'Plotting map. This may take a few seconds...')
            ch.display_first()
            self.set_can_helper(ch)

    def plot_histogram(self):
        resfile_window = QAskFileWindow(self, "File Selection", 'Select result file', self.historesultfile)
        if resfile_window.dresult=='OK':
            self.historesultfile = resfile_window.sel_file
            self.mapinp.mapfile = resfile_window.sel_file
            resultfile = resfile_window.sel_file
            ch = QCanvasHelperMultiHisto(self.main_canvas)
            ch.add_result_file(resultfile)
            ch.display_first()
            self.set_can_helper(ch)
        
    def plot_quadplot(self):
        pass

    def about(self):
        QAboutWindow(self, "About QUIDDIT")

    def review_deconv(self):
        revinp = QReviewInpWindow(self, "Review Input", self.revdta)
        if revinp.dresult =='OK':
            self.revdta = revinp.revdta
            ch = QCanvasHelperDeconvReview(self.main_canvas)
            ch.add_files(revinp.revdta)
            ch.display_first()
            self.set_can_helper(ch)

    def review_peakf(self):
        peakrevinp = QReviewInpWindow(self, "Review Input", self.peakrevdta)
        if peakrevinp.dresult =='OK':
            self.peakrevdta = peakrevinp.revdta

    def process_data(self):
        #get a new input window initialised with process inp data
        inpf = QProcessDtaInpWindow(self, "Deconvolution Input", self.prcdta)
        if inpf.dresult =='OK':
            self.prcdta = inpf.prcdta

            specfiles = self.prcdta.selectedfiles
            resultfile = self.prcdta.result
            reviewfile = self.prcdta.review
            age = self.prcdta.age
            samplename = self.prcdta.name

            #prepare files for results and review
            with open(resultfile, 'w') as res_fob:
                res_fob.write('Results for sample %s - age: %.0f Ma' %(str(samplename), round(age, 3)) + ':\n')
                res_fob.write(QUtility.res_header+'\n')

            with open(reviewfile, 'w') as rev_fob:
                rev_fob.write('Review for sample %s' %(str(samplename)) + ':\n')
                rev_fob.write(QUtility.rev_header+'\n')

            i = 1
            for filename in specfiles:
                self.print_message(self.message, 'Processing file {}/{}'.format(i, len(specfiles)))
                result, review = decon.deconvolution(filename, self.prcdta.age, QSettings.N_comp)
                
                with open(resultfile, 'a') as res_fob:
                    for item in result[0]:
                        res_fob.write(str(item)+',')
                    res_fob.write('\n')

                with open(reviewfile, 'a') as rev_fob:
                    for item in review[0]:
                        rev_fob.write(str(item)+',')
                    rev_fob.write('\n')
                i += 1

            self.print_message(self.message, '\nDeconvolution complete.')


    def peak_fit(self):
        peakinp = QPeakfitInpWindow(self, "Peak fit input", self.pkfitdta)
        if peakinp.dresult =='OK':
            self.pkfitdta = peakinp.peakdta

    def man_N_fit(self):
        pass
        
    def man_peakfit(self):
        pass

    def twostage_model(self):
        QTwostageModelWindow(self, 'Two-stage nitrogen aggregation model', self.twostage_inp)
         
if __name__ == '__main__':
    mw = MainWindow("QUIDDIT version 2.0")
    mw.mainloop()
   