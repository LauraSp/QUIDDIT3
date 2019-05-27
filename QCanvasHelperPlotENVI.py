from QCanvasHelperBase import *
import spectral.io.envi as envi
from QSettings import *
from QUtility import *
import numpy as np


class QCanvasHelperPlotENVI(QCanvasHelperBase):
    def display_current(self):
        self.clear_plot()

        curr_band = self.idx_dta[self.current]
        actual_band = QUtility.closest(curr_band, self.bands)
        band_idx = np.where(self.bands == actual_band)[0]   
        
        view = self.envi_img[:,:,band_idx]

        fig = self.canv.figure
        fig.suptitle(str(curr_band) + ' $cm^{-1}$')
        sp = fig.add_subplot(111)


        sp.imshow(view.squeeze(), origin='lower',
                cmap=QSettings.STD_COLS)

        self.canv.draw()

    
    def add_files(self, hdr_file, dat_file):
        self.idx_dta = QSettings.ENVIITEMS
        self.envi_img = envi.open(hdr_file, dat_file)

        wavenum = envi.read_envi_header(hdr_file)['wavelength']
        self.bands = np.array([float(i) for i in wavenum])

        self.maxidx = len(self.idx_dta)
