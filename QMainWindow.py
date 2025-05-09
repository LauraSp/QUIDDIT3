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
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
from matplotlib.figure import Figure

#all popupwindows have to be imported
from QHistogramWindow import *
from QAboutWindow import *
from QAskSpectraWindow import *
from QAskFileWindow import *
from QAskENVIWindow import *
from QENVIconversionWindow import *
from QDPTConversionWindow import *
from QProcessDtaInpWindow import *
from QPeakfitInpWindow import *
from QReviewInpWindow import*
from QPlotMapInpWindow import *
from QPlotBatchPeakMapInpWindow import *
from QBaselineSubtrWindow import *
from QUserSettingsWindow import *
from QTwostageModelWindow import *
from QManualNFitWindow import *
from QManualPeakFitWindow import *
from QDiamondTypeWindow import *
from QSettings import *
from QCanvasHelperSpectrum import *
from QCanvasHelperLineResult import *
from QCanvasHelperSingleHisto import *
from QCanvasHelperMultiHisto import *
from QCanvasHelperMap import *
from QCanvasHelperBatchPeakMap import *
from QCanvasHelperQuadplot import *
from QCanvasHelperDeconvReview import *
from QCanvasHelperBatchPeakFitReview import *
from QCanvasHelperPlotENVI import *
import QBaselineAlt as bl
import QGeneralDeconvolution as decon
import QBatchPeakFit as peakfit
import QENVIconversion as envicon
import QDPTConverter as dptcon
import QDiamondType as diatp


class MainWindow(QTclBaseWindow):
    """Main window for QUIDDIT
    """
    def make_gui(self, title):
        """ create the gui
        """
        self.canhelper = None
        self.setwintitle(title)

        #Making the main menu
        menubar = self.create_menu_bar()
        self.master.config(menu=menubar)

        # making the controls
        row = 0
        self.main_fig = Figure(dpi=100)
        self.ax = self.main_fig.add_subplot(111)
        self.main_fig.gca().invert_xaxis()
        self.main_fig.suptitle('QUIDDIT')
        self.IIa_spec = QUtility.read_spec(QSettings.IIa_path)
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

        self.toolbar = NavigationToolbar2Tk(self.main_canvas, toolbar_frame)

        self.back_button = self.makebutton(erow=row, ecol=0, caption='Previous',
                                           cmd=self.display_prev,
                                           state=tk.DISABLED, padx=5, pady=5, sticky=tk.W)
        self.next_button = self.makebutton(erow=row, ecol=3, caption='Next',
                                           cmd=self.display_next,
                                           state=tk.DISABLED, padx=5, pady=5, sticky=tk.E)

        self.histo_button = self.makebutton(erow=row, ecol=2, caption='Histogram',
                                           cmd=self.histo_popup,
                                           state=tk.DISABLED, padx=5, pady=5, sticky=tk.E)

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
        self.convdptdta = QDPTconvinp('', '')
        self.plotenvidata = QENVIInp('', '')
        self.bldata = QBaselineSubtrInp([], '')
        self.revdta = QReviewInp([], '')
        self.peakrevdta = QReviewInp([], '')
        self.mapinp = QPlotMapInp('', QSettings.MAPCLIMS)
        self.batchpeakmapinp = QPlotMapInp('', QSettings.BATCHPEAKMAPCLIMS)
        self.diatypedta = QDiamondTypeInp('', [], '', 0)
        self.specs = []
        self.lineresultfile = ''
        self.historesultfile = ''
        self.quadplotresultfile = ''
        self.twostage_inp = QTwoStageModelInp(2700, 1600, 0.82, 400, 0.2)
        self.manualfit_files = []


    def print_message(self, textwidget, text):
        """print text to textwidget
        """
        textwidget['state'] = 'normal'
        textwidget.insert('end', text+'\n')
        textwidget['state'] = 'disabled'
        textwidget.see('end')

    def print_result(self, header, result):
        names = header.split(',')

        for idx, item in enumerate(zip(names, result)):
            if idx == 0:
                self.print_message(self.message, 'results for spectrum {}'.format(str(result['name']).split('/')[-1]))
            else:
                self.print_message(self.message, '{}: {}'.format(item[0], np.round(item[1], 2)))

        self.print_message(self.message, '\n')


    def create_menu_bar(self):
        """ Fill the menu
        """
        menubar = tk.Menu(self)
        filemenuopt = {'Convert ENVI file':self.convert_ENVI,
                        'Convert dpt file':self.convert_DPT,
                        'Open spectra':self.plot_spectra,
                        'Open ENVI': self.plot_ENVI,
                       'Exit':self.click_exit}
        filemenu = self.make_menu(menubar, 'File', filemenuopt)
        filemenu.insert_separator(2)

        optmenuopt = {'User settings':self.change_user_settings}

        self.make_menu(menubar, 'Settings', optmenuopt)

        baselinemenuopt = {'Correct baseline':self.baseline}
        self.make_menu(menubar, 'Baseline', baselinemenuopt)

        procmenuopt = {'General Deconvolution':self.process_data,
                       'Custom Peak Fit': self.peak_fit,
                       'Diamond type': self.diamondtype}
        self.make_menu(menubar, 'Batch Process', procmenuopt)

        revmenuopt = {'Review General Deconvolution':self.review_deconv,
                    'Review Custom Peak Fit':self.review_peakf}
        self.make_menu(menubar, 'Review', revmenuopt)

        plotmenuopt = {'Plot spectra':self.plot_spectra,
                       'Plot line results':self.plot_ls,
                       'Plot map results':self.plot_map,
                       'Plot maps from cust. peak fit':self.plot_batchpeakmap,
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
        try:
            if self.canhelper != None:
                histo = self.canhelper.get_current_histo_data()
                QHistogramWindow(mw, "Histogram", histo)

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)

    
    def convert_ENVI(self):
        try:
            enviwindow = QENVIconversionWindow(self, "ENVI Conversion", self.convenvidta)
            if enviwindow.dresult == 'OK':
                self.convenvidta = enviwindow.convdta
                self.print_message(self.message,
                            'Converting ENVI to CSV. This may take a while.\nFiles will be stored here: {}\n'.format(self.convenvidta.targetdir))
            
                conv = envicon.QENVIconverter(self.convenvidta)
                conv.convert()
                self.print_message(self.message, 'Conversion complete.\n')

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
               "Original message: {}".format(str(e)),
                e)


    def convert_DPT(self):
        try:
            dptwindow = QDPTConversionWindow(self, "dpt Converison", self.convdptdta)

            if dptwindow.dresult == 'OK':
                self.convdptdta = QDPTconvinp(dptwindow.dpt_file, dptwindow.target_dir)

                self.print_message(self.message,
                            'Converting dpt file to CSV. This may take a while.\nFiles will be stored here: {}\n'.format(self.convdptdta.target_dir))

                conv = dptcon.QDPTconverter(self.convdptdta)
                conv.convert()
                self.print_message(self.message, 'Conversion complete.\n')


        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
               "Original message: {}".format(str(e)),
                e)


    def change_user_settings(self):
        try:
            QUserSettingsWindow(mw, "User settings")

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def do_nothing(self):
        pass


    def click_exit(self):
        try:
            mwin = QTclMessageWindow(mw, "QUIDDIT Question", "Just to make sure ...", "Do you really want to quit QUIDDIT?")
            if mwin.dresult == 'OK':
                self.root.destroy()

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def display_next(self):
        if self.canhelper != None:
            self.canhelper.display_next()


    def display_prev(self):
        if self.canhelper != None:
            self.canhelper.display_previous()


    def baseline(self):
        try:
            bl_window = QBaselineSubtrWindow(self, "Baseline subtraction", self.bldata)
            if bl_window.dresult =='OK':
                self.bldta = bl_window.bldta

                i = 1
                for filename in self.bldta.sel_files:
                    self.print_message(self.message, 'Baseline removal {}/{}:\n{}'.format(i, len(self.bldta.sel_files), filename.split('/')[-1]))
                    bl.remove_baseline(filename, self.bldta.res_dir, bl_type=QSettings.BLvar)
                    self.update()
                    i += 1
                self.print_message(self.message, '\nBaseline removal complete.')
                self.update()

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def plot_spectra(self):
        try:
            spec_window = QAskSpectraWindow(self, "Select Spectra", self.specs)
            if spec_window.dresult =='OK':
                self.specs = spec_window.spec_files
                ch = QCanvasHelperSpectrum(self.main_canvas)
                ch.add_spectra_files(self.specs)
                ch.display_first()
                self.set_can_helper(ch)

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


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
        try:
            resfile_window = QAskFileWindow(self, "File Selection", 'Select linescan results', self.lineresultfile)
            if resfile_window.dresult=='OK':
                self.lineresultfile = resfile_window.sel_file
                ch = QCanvasHelperLineResult(self.main_canvas)
                ch.add_line_data(self.lineresultfile)
                ch.display_first()

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)
            
    def plot_map(self):
        try:
            resfile_window = QPlotMapInpWindow(self, "Input for map plotting", self.mapinp)
            if resfile_window.dresult=='OK':
                self.mapinp.map_file = resfile_window.sel_file
                self.mapinp.clims = resfile_window.clims
                self.historesultfile = resfile_window.sel_file
                ch = QCanvasHelperMap(self.main_canvas)
                ch.add_map_file(self.mapinp.map_file, self.mapinp.clims)
                self.print_message(self.message, 'Plotting map. This may take a few seconds...')
                ch.display_first()
                self.set_can_helper(ch)

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)

    def plot_batchpeakmap(self):
        try:
            resfile_window = QPlotBatchPeakMapInpWindow(self, "Input for map plotting", self.batchpeakmapinp)
            self.batchpeakmapinp.map_file = resfile_window.sel_file
            self.batchpeakmapinp.clims = resfile_window.clims
            ch = QCanvasHelperBatchPeakMap(self.main_canvas)
            ch.add_map_file(self.batchpeakmapinp.map_file, self.batchpeakmapinp.clims)
            self.print_message(self.message, 'Plotting map. This may take a few seconds...')
            ch.display_first()
            self.set_can_helper(ch)

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                e)

    def plot_histogram(self):
        try:
            resfile_window = QAskFileWindow(self, "File Selection", 'Select result file', self.historesultfile)
            if resfile_window.dresult=='OK':
                self.historesultfile = resfile_window.sel_file
                self.mapinp.mapfile = resfile_window.sel_file
                resultfile = resfile_window.sel_file
                ch = QCanvasHelperMultiHisto(self.main_canvas)
                ch.add_result_file(resultfile)
                ch.display_first()
                self.set_can_helper(ch)

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)
        
    def plot_quadplot(self):
        try:
            resfile_window = QAskFileWindow(self, "File Selection", 'Select result file', self.quadplotresultfile)
            if resfile_window.dresult == 'OK':
                self.quadplotresultfile = resfile_window.sel_file
                ch = QCanvasHelperQuadplot(self.main_canvas)
                ch.add_map_data(self.quadplotresultfile)
                ch.display_first()

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)

    def plot_ENVI(self):
        try:
            envifiles_window = QAskENVIWindow(self, "File Selection", self.plotenvidata)
            if envifiles_window.dresult == 'OK':
                self.plotenvidata = envifiles_window.envidta
                ch = QCanvasHelperPlotENVI(self.main_canvas)
                ch.add_files(self.plotenvidata.hdr, self.plotenvidata.dat)
                ch.display_first()
                self.set_can_helper(ch)

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def about(self):
        QAboutWindow(self, "About QUIDDIT")


    def review_deconv(self):
        try:
            revinp = QReviewInpWindow(self, "Review Input", self.revdta)
            if revinp.dresult =='OK':
                self.revdta = revinp.revdta
                ch = QCanvasHelperDeconvReview(self.main_canvas)
                ch.add_files(revinp.revdta)
                ch.display_first()
                self.set_can_helper(ch)

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def review_peakf(self):
        try:
            peakrevinp = QReviewInpWindow(self, "Review Input", self.peakrevdta)
            if peakrevinp.dresult =='OK':
                self.peakrevdta = peakrevinp.revdta
                ch = QCanvasHelperBatchPeakFitReview(self.main_canvas)
                ch.add_files(peakrevinp.revdta)
                ch.display_first()
                self.set_can_helper(ch)

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def process_data(self):
        #get a new input window initialised with process inp data
        try:
            inpf = QProcessDtaInpWindow(self, "Deconvolution Input", self.prcdta)
            
            if inpf.dresult =='OK':
                self.prcdta = inpf.prcdta

                specfiles = self.prcdta.selectedfiles
                assert(len(specfiles)>=1), "No files selected."
                
                resultfile = self.prcdta.result
                reviewfile = self.prcdta.review

                if resultfile == reviewfile:
                    reviewfile += '2'
                    self.print_message(self.message, 'The same name was entered for result and review file.\nSaving review as: {}'.format(reviewfile + '.csv'))

                resultfile += '.csv'
                reviewfile += '.csv'

                age = self.prcdta.age
                samplename = self.prcdta.name

                ch = QCanvasHelperSpectrum(self.main_canvas)

                #prepare files for results and review
                with open(resultfile, 'w') as res_fob:
                    res_fob.write('Results for sample %s - age: %.0f Ma' %(str(samplename), round(age, 3)) + ':\n')
                    res_fob.write(QUtility.res_header+'\n')

                with open(reviewfile, 'w') as rev_fob:
                    rev_fob.write('Review for sample %s' %(str(samplename)) + ':\n')
                    rev_fob.write(QUtility.rev_header+'\n')

                i = 1
                for filename in specfiles:
                    ch.add_spectra_files([filename])
                    ch.display_first()
                    self.print_message(self.message, 'Processing file {}/{}'.format(i, len(specfiles)))
                    result, review = decon.deconvolution(filename, self.prcdta.age, QSettings.N_comp)

                    self.print_result(QUtility.res_header, result[0])
                
                    with open(resultfile, 'a') as res_fob:
                        for item in result[0]:
                            res_fob.write(str(item)+',')
                        res_fob.write('\n')

                    with open(reviewfile, 'a') as rev_fob:
                        for item in review[0]:
                            rev_fob.write(str(item)+',')
                        rev_fob.write('\n')

                    i += 1
                    self.update()

                self.print_message(self.message, 'Deconvolution complete.')

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def peak_fit(self):
        try:
            peakinp = QPeakfitInpWindow(self, "Peak fit input", self.pkfitdta)
            if peakinp.dresult =='OK':
                self.pkfitdta = peakinp.pkdta
                samplename = self.pkfitdta.name
                resultfile = self.pkfitdta.result + '.csv'
                specfiles = self.pkfitdta.selectedfiles

                with open(resultfile, 'w') as res_fob:
                    res_fob.write('Results for sample ' + str(samplename) + ':\n')
                    res_fob.write(QUtility.peakfit_header + '\n')

                ch = QCanvasHelperSpectrum(self.main_canvas)

                i = 1
                for specfile in specfiles:
                    ch.add_spectra_files([specfile])
                    ch.display_first()
                    self.print_message(self.message, 'Processing File {}/{}'.format(i, len(specfiles)))
                    result = peakfit.fit_peak(specfile, self.pkfitdta.peak)

                    self.print_result(QUtility.peakfit_header, result[0])

                    with open(resultfile, 'a') as res_fob:
                        for item in result[0]:
                            res_fob.write(str(item)+',')
                        res_fob.write('\n')

                    i += 1
                    self.update()
            
                self.print_message(self.message, 'Deconvolution complete.')

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def diamondtype(self):
        try:
            diatype_window = QDiamondTypeWindow(self, "Diamond Type Determination", self.diatypedta)
            if diatype_window.dresult == 'OK':
                self.diatypedta = diatype_window.typedta
                spectra = self.diatypedta.selectedfiles
                save = False if self.diatypedta.savevar == 0 else True
                outpath = self.diatypedta.savedir

                resultfile = QSettings.userhome + '\\' + self.diatypedta.result + '.csv'
                with open(resultfile, 'w') as res_fob:
                    res_fob.write('name, type, note\n')

                ch = QCanvasHelperSpectrum(self.main_canvas)

                i=1
                for filename in spectra:
                    ch.add_spectra_files([filename])
                    ch.display_first()
                    diamondtype, warn = diatp.diamondtype(filename, save, outpath=outpath)
                    note = 'ok' if warn == '' else warn
                    self.print_message(self.message, 'Processing file {}/{}: {}'.format(i, len(spectra), filename))
                    self.print_message(self.message, 'type: {}\nnote: {}\n'.format(diamondtype, note))
                    with open(resultfile, 'a') as res_fob:
                        res_fob.write('{}, {}, {}\n'.format(filename, diamondtype, warn))

                    i += 1
                    self.update()

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def man_N_fit(self):
        try:
            QManualNFitWindow(self, 'Manual N fit', self.manualfit_files)
        
        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)

        
    def man_peakfit(self):
        try:
            QManualPeakFitWindow(self, 'Manual Peak fit', self.manualfit_files)

        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


    def twostage_model(self):
        try:
            QTwostageModelWindow(self, 'Two-stage nitrogen aggregation model', self.twostage_inp)
        
        except Exception as e:
            QTclMessageWindow(mw, "QUIDDIT Error", "An unhandled error has occured", 
                "Original message: {}".format(str(e)),
                 e)


if __name__ == '__main__':
    mw = MainWindow("QUIDDIT version {}".format(QSettings.version))
    mw.mainloop()
   