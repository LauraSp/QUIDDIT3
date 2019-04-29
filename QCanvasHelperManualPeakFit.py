from QCanvasHelperBase import *
from QSettings import *
from QUtility import *

import numpy as np
import scipy.optimize as op
from matplotlib.widgets import Slider
from matplotlib.widgets import Button as mplButton

class QCanvasHelperManualPeakFit(QCanvasHelperBase):
    def display_current(self):
        self.clear_plot()
    
    def read_spectrum(self, idx):
        """read current spectrum
        """
        filename = self.specfiles[idx]
        if filename.lower().endswith('.csv'):
            spec = np.loadtxt(filename, delimiter=',')
            return spec
        else:
            raise Exception("Unknown identifier " + filename + " in read_spectrum")

    def get_spec_name(self, idx):
        filename = self.specfiles[idx]
        if filename.lower().endswith('.csv'):
            return filename.split("/")[-1].split(".")[0]
        else:
            raise Exception("Unknown identifier " + filename + " in get_spec_name")

    def add_data(self, specfiles, age):
        self.specfiles = specfiles
        self.age = age
        self.maxidx = len(self.specfiles)
        self.__std = QSettings.std

    def widget_reset(self, event, sliders):
        for slider in sliders:
            slider.reset()

    def widget_update(self, val):
        pass