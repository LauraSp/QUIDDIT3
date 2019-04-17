from QCanvasHelperBase import *
import numpy as np

class QCanvasHelperSingleHisto(QCanvasHelperBase):    

    def display_current(self):
        self.clear_plot()
        sp = self.canv.figure.add_subplot(111)
        sp.hist(self.dat_array[~np.isnan(self.dat_array)], bins='auto')
        self.canv.figure.suptitle(self.title)
        self.canv.draw()

    def add_histo_data(self, data):
        self.title = data["title"]
        self.dat_array = data["data"]
        self.maxidx = 1
