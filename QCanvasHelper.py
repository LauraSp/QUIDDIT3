import matplotlib
from matplotlib.figure import Figure
from mpl_toolkits.axes_grid1 import make_axes_locatable
from scipy import interpolate
import numpy as np
from QSettings import *
from QUtility import *

class QCanvasHelper:
    """class to help with populating the canvas
    """
    SPECTRUM = 1
    HISTO = 2
    MAPRESULTS = 3
    LINERESULTS = 4
    REVIEW = 5
    PREVIEW = 6
    PRESULTS = 7


    def __init__(self, canvas, typ):
        if not (typ>0 and typ<8) :
            raise ValueError('canvas type does not match any allowed type')

        self.canv = canvas
        self.type = typ
        self.current = 0
        self.specids = None
        #self.mapids = None
        self.mapextent = None
        self.maptitles = []
        self.histdta = None
        self.bins = 200

    def add_spectra_files(self, files):
        self.specids = []
        for file in files:
            self.specids.append(file)

    def add_map_file(self, file):
        self.maptitles = QSettings.PLOTITEMS
        self.specids = []
        dta = np.loadtxt(file, dtype=QUtility.results_dtype, delimiter=',', skiprows=2)

        self.x = []
        self.y = []
        for name in dta['name']:
            xy = name.split('/')[-1]
            self.x.append(float(xy.split(' ')[0][2:]))
            self.y.append(float(xy.split(' ')[1].strip(".csv'")[1:]))
        self.mapextent = (min(self.x), max(self.x), min(self.y), max(self.y))
        resolution = QSettings.STD_RES
        self.grid_x, self.grid_y = np.mgrid[self.mapextent[0]:self.mapextent[1]:resolution,
                                self.mapextent[2]:self.mapextent[3]:resolution]

        MAPS = {'$[N_T]$ (ppm)': dta['[NT]'],
            '$[N_C]$ (ppm)': dta['[NC]'],
            '$[N_A]$ (ppm)': dta['[NA]'],
            '$[N_B]$ (ppm)': dta['[NB]'],
            '$[N_B]/[N_T]$': (dta['[NB]']/dta['[NT]']),
            '$T (^{\circ}C)$': dta['T'],
            'platelet peak position $(cm^{-1})$': dta['p_x0'],
            'platelet peak area $(cm^{-2})$': dta['p_area_ana'],
            'platelet peak width $(cm^{-1})$': (dta['p_HWHM_l'] + dta['p_HWHM_r']),
            'platelet peak symmetry $(cm^{-1})$': (dta['p_x0'] - dta['avg']),
            'I(3107) $(cm^{-2})$': dta['H_area_ana']}

        for title in self.maptitles:
            self.specids.append(MAPS[title])


    def display_first(self):
        if len(self.specids) >= 1:
            self.current = 0
            self.display_current()
        else:
            raise Exception("no spectra files were added before display_first was used")

    def display_last(self):
        if len(self.specids) >= 1:
            self.current = len(self.specids)
            self.display_current()
        else:
            raise Exception("no spectra files were added before display_first was used")
    
    def get_spec_name(self, id):
        if id.lower().endswith('.csv'):
            return id.split("/")[-1].split(".")[0]
        else:
            raise Exception("Unknown identifier " + id + " in get_spec")

    def display_next(self):
        if self.current < len(self.specids) - 1:
            self.current += 1
        else:
            self.current = 0
        
        self.display_current()

    def display_current(self):
        if len(self.specids) < self.current or self.current < 0:
            raise Exception("index out of range")
            
        self.clear_plot()
        t = self.type
        if t== QCanvasHelper.SPECTRUM:
            self.plot_spectrum()
        elif t == QCanvasHelper.REVIEW:
            raise NotImplementedError("plot type not yet implmented")
        elif t == QCanvasHelper.PREVIEW:
            raise NotImplementedError("plot type not yet implmented")
        elif t == QCanvasHelper.PRESULTS:
            raise NotImplementedError("plot type not yet implmented")
        elif t == QCanvasHelper.MAPRESULTS:
            self.plot_map()
        elif t == QCanvasHelper.LINERESULTS:
            raise NotImplementedError("plot type not yet implmented")
        elif t == QCanvasHelper.HISTO:
            self.plot_histogram(bins=self.bins)
        else:
            raise NotImplementedError("unknon plot type")

        self.canv.draw()


    def plot_spectrum(self):
        """plot spectrum
        """
        spid = self.specids[self.current]
        spect = self.get_spec(spid)
        sp = self.canv.figure.add_subplot(111)
        sp.plot(spect[:,0], spect[:,1], 'k-')
        sp.invert_xaxis()
        self.canv.figure.suptitle(self.get_spec_name(spid))

    def plot_map(self):
        """plot map
        """
        mpid = self.specids[self.current]
        mtitle = self.maptitles[self.current]
        clim = QSettings.MAPCLIMS[mtitle]
        resolution = QSettings.STD_RES
        dtagrid = self.make_2d_grid(mpid)

        fig = self.canv.figure
        sp = fig.add_subplot(111)
        img = sp.imshow(dtagrid, origin='lower',
                extent=self.mapextent,
                cmap=QSettings.STD_COLS,
                clim=clim)
        divider = make_axes_locatable(sp)
        cax = divider.append_axes("right", size="5%", pad=0.3)
        self.cbar = fig.colorbar(img, cax=cax)
        fig.suptitle(mtitle)
    
    def plot_histogram(self, array, bins):
        self.histdta = array
        sp = self.canv.figure.add_subplot(111)
        sp.hist(array, bins=bins)



    def display_previous(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = len(self.specids) - 1
        
        self.display_current()

    def get_spec(self, id):
        if id.lower().endswith('.csv'):
            return np.loadtxt(id, delimiter=',')
        else:
            raise Exception("Unknown identifier " + id + " in get_spec")
    

    def clear_plot(self):
        fig = self.canv.figure
        for ax in fig.get_axes():
            fig.delaxes(ax)

        fig.suptitle("QUIDDIT")

    def make_2d_grid(self, dta):
        grid = interpolate.griddata((self.x,self.y), dta, (self.grid_x,self.grid_y), method='linear', fill_value=np.nan)
        return grid.T