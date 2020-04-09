from QCanvasHelperBase import *
from QSettings import *
from QUtility import *
import numpy as np
from scipy import interpolate
from mpl_toolkits.axes_grid1 import make_axes_locatable


class QCanvasHelperMap(QCanvasHelperBase):

    def add_map_file(self, file, clims):
        self.clims = clims
        dta = np.loadtxt(file, dtype=QUtility.results_dtype, delimiter=',', skiprows=2)
        self.x = []
        self.y = []
        for name in dta['name']:
            xy = name.lower().split('/')[-1]
            self.x.append(float(xy.split(' ')[0][2:]))
            self.y.append(float(xy.split(' ')[1].strip(".csv")[1:]))

        self.mapextent = (min(self.x), max(self.x), min(self.y), max(self.y))
        resolution = QSettings.STD_RES
        self.grid_x, self.grid_y = np.mgrid[self.mapextent[0]:self.mapextent[1]:resolution,
                                self.mapextent[2]:self.mapextent[3]:resolution]

        self.idx_data = QSettings.PLOTITEMS
        self.map_data = {'$[N_T]$ (ppm)': dta['[NT]'],
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

        self.maxidx = len(self.map_data)


    def display_current(self):
        """plot map
        """
        self.clear_plot()
        
        key = self.idx_data[self.current]
        data = self.map_data[key]
        clim = self.clims[key]
        dtagrid = self.make_2d_grid(data)

        fig = self.canv.figure
        sp = fig.add_subplot(111)
        img = sp.imshow(dtagrid, origin='lower',
                extent=self.mapextent,
                cmap=QSettings.STD_COLS,
                clim=clim)
        divider = make_axes_locatable(sp)
        cax = divider.append_axes("right", size="5%", pad=0.3)
        self.cbar = fig.colorbar(img, cax=cax)
        fig.suptitle(key)

        fig.tight_layout(rect=[0, 0.03, 1, 0.95])

        self.canv.draw()
        

    def make_2d_grid(self, dta):
        grid = interpolate.griddata((self.x,self.y), dta, (self.grid_x,self.grid_y), method='linear', fill_value=np.nan)
        return grid.T

    def get_current_histo_data(self):
        key = self.idx_data[self.current]
        return {
                "title" : key,
                "data" : self.map_data[key]
            }

