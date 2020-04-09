import numpy as np
from QCanvasHelperBase import *
from QUtility import *

class QCanvasHelperSpectrum(QCanvasHelperBase):

    def display_current(self):
        self.clear_plot()
        spid = self.specids[self.current]
        spect = self.get_spec(spid)
        sp = self.canv.figure.add_subplot(111)
        sp.plot(spect[:,0], spect[:,1], 'k-')
        sp.invert_xaxis()
        self.canv.figure.suptitle(self.get_spec_name(spid))
        self.canv.draw()


    def add_spectra_files(self, files):
        self.specids = []
        for file in files:
            self.specids.append(file)

        self.maxidx = len(self.specids)

    def get_spec(self, id):
        if id.lower().endswith('.csv'):

            return QUtility.read_spec(id)

        else:
            raise Exception("Unknown identifier " + id + " in get_spec")

    def get_spec_name(self, id):
        if id.lower().endswith('.csv'):
            return id.split("/")[-1].split(".")[0]
        else:
            raise Exception("Unknown identifier " + id + " in get_spec_name")

    
