from QCanvasHelperBase import *
from QSettings import *
from QUtility import *
import numpy as np

class QCanvasHelperBatchPeakFitReview(QCanvasHelperBase):
    def display_current(self):
        self.clear_plot()

        fig = self.canv.figure
        fig.suptitle(self.get_spec_name(self.current))

        spec = self.read_spectrum(self.current)
        rev = self.rev_data[self.current]

        peak = QUtility.spectrum_slice(spec, rev['x0']-50, rev['x0']+50)
        wav = np.arange(peak[0,0], peak[-1,0], 0.1)

        peak_interp = QUtility.inter(peak, wav)

        psv = QUtility.pseudovoigt_fit(wav, rev['x0'], rev['I'], rev['HWHM_l'], rev['HWHM_r'], rev['sigma'])
        bg = np.polyval((rev['bg_a'], rev['bg_b'], rev['bg_c'], rev['bg_d']), wav)   
        fit = psv + bg

        sp = fig.add_subplot(111)
        sp.plot(peak[:,0], peak[:,1], 'k.', label='data')
        sp.plot(wav, bg, '--', label='background')
        sp.plot(wav, fit, 'g-', label='fit')
        sp.plot(wav, peak_interp-fit, 'r-', label='misfit')
        sp.invert_xaxis()
        sp.legend(loc='best')
        

        self.canv.draw()
    
    
    def add_files(self, reviewinput):
        """Add review file and spectra
        """
        rev_file = reviewinput.rev_file
        self.spec_files = reviewinput.spec_files
        self.rev_data = np.loadtxt(rev_file, dtype=QUtility.peakfit_dtype, delimiter=',', skiprows=2) 

        if len(self.rev_data) != len(self.spec_files):
            raise ValueError('The number of spectra ({}) does not match the length of the review file ({}).'.format(len(self.spec_files), len(self.rev_data)))
    
        else:
            self.maxidx = len(self.rev_data)

    def read_spectrum(self, idx):
        """read current spectrum
        """
        filename = self.spec_files[idx]
        if filename.lower().endswith('.csv'):
            spec = np.loadtxt(filename, delimiter=',')
            return spec
        else:
            raise Exception("Unknown identifier " + filename + " in read_spectrum")

    def get_spec_name(self, idx):
        filename = self.spec_files[idx]
        if filename.lower().endswith('.csv'):
            return filename.split("/")[-1].split(".")[0]
        else:
            raise Exception("Unknown identifier " + filename + " in get_spec_name")