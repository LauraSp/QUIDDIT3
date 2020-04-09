# -*- coding: utf-8 -*-
"""
Created on Mon Sep 04 16:10:39 2017
This file contains a number of settings used across QUIDDIT
@author: ls13943
"""
import json
import os
from pathlib import Path
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm


class QSettings:
        """Class for storing an retrieving the program settings.
           Settings are produced by defaults programmed here
           eventually overwrtittem by user configurations
           taken from a local json-file named quiddit.conf
        """
        home = os.getcwd()
        userhome = str(Path.home())

        version = '3.0-alpha'
        github_url = 'https://github.com/LauraSp/QUIDDIT3'
        
        #path to file with standard spectra of N components (CSV)
        std_path = os.getcwd() + '/CAXBD.csv'
        IIa_path = os.getcwd() + '/typeIIa.csv'
        IIa_alt_path = os.getcwd() + '/typeIIa_alt.csv'
        std = np.loadtxt(std_path, delimiter = ',')     # read CAXBD spectra

        #standard first guess for platelet fit (p_x0, p_I, p_HWHM_l, p_HWHM_r, p_sigma, 
        #H1405_x0, H1405_I, H1405_HWHM_l, H1405_HWHM_r, H1405_sigma, 
        #B_x0, B_I, B_HWHM_l, B_HWHM_r, B_sigma,
        #const)
        pp_res_prev = (1370, 0, 5, 5, 1, 
                1405, 0, 5, 5, 1, 
                1332, 0, 5, 5, 0, 
                1)

        ori_N_comp = np.array((0, 1, 0, 1, 1, 1)) 
        N_comp = np.array(ori_N_comp)

        ori_BLvar = 0
        BLvar = ori_BLvar

        #pp_res_prev = (1365, 1.2, 3, 3, 1, 
        #               1405, 0, 5, 5, 1, 
        #               1332, 0, 5, 5, 0, 
        #              1)

        #*this set of parameters is only used when the first attempt of fitting fails.
        ENVIITEMS = (1992, 1360, 1344, 1282, 1170, 1130)


        PLOTITEMS = ('$[N_T]$ (ppm)',
            '$[N_C]$ (ppm)',
            '$[N_A]$ (ppm)',
            '$[N_B]$ (ppm)',
            '$[N_B]/[N_T]$',
            r'$T (^{\circ}C)$',
            'platelet peak position $(cm^{-1})$',
            'platelet peak area $(cm^{-2})$',
            'platelet peak width $(cm^{-1})$',
            'platelet peak symmetry $(cm^{-1})$',
            'I(3107) $(cm^{-2})$')


        PEAKPLOTITEMS = ('$x_0 (cm^{-1})$',
                '$I (cm^{-1})$',
                'FWHM $(cm^{-1})',
                'sigma (-)',
                'peak area $(cm^{-2})$')


        MAPCLIMS = {'$[N_T]$ (ppm)': (None, None),
                '$[N_C]$ (ppm)': (None, None),
                '$[N_A]$ (ppm)': (None, None),
                '$[N_B]$ (ppm)': (None, None),
                '$[N_B]/[N_T]$': (0., 1.),
                r'$T (^{\circ}C)$': (1000, 1400),
                'platelet peak position $(cm^{-1})$':(1358., 1378.),
                'platelet peak area $(cm^{-2})$': (None, None),
                'platelet peak width $(cm^{-1})$': (None, 25.),
                'platelet peak symmetry $(cm^{-1})$': (-15., 5.),
                'I(3107) $(cm^{-2})$': (None, None)}


        BATCHPEAKMAPCLIMS = {'$x_0 (cm^{-1})$': (None, None),
                '$I (cm^{-1})$': (None, None),
                'FWHM $(cm^{-1})': (None, None),
                'sigma (-)': (0, 1),
                'peak area $(cm^{-2})$': (None, None)}


        STD_COLS = cm.get_cmap('jet')


        var_defaults = {'home' : home,
                'N_comp' : N_comp,
                'file_count' : '',
                'namevar' : '',
                'resultvar' : '',
                'reviewvar' : '',
                'agevar' : 2900.,
                'peakvar' : 3107.0,
                'c_NT_var' : 0.,
                'r_NT_var' : 0.,
                'c_agg_var' : 0.,
                'r_agg_var' : 0.,
                'plotmode' : '',
                'minvar' : 0.,
                'maxvar' : 1.,
                'peak' : 0}


        # settings for plotting

        colors = ['blue','green','red']
        levels = [0,1]

        cmap, norm = mpl.colors.from_levels_and_colors([1,63,76,79], ['blue','green','red'])

        f=16
        l=2
        m=3
        
        STD_DPI = 100
        STD_RES = 2000j
        user_conf_file = "quiddit.conf"

        @classmethod
        def read_user_cfg(cls): 
                """reading the user configs from a json.file
                """
                try:
                        with open(cls.userhome + '/quiddit.conf') as json_file:
                                alldata = json.load(json_file, object_hook=MyJsonEncoder.decode)
                        #cls.BLvar = alldata.BLvar()
                        cls.N_comp = (alldata.N_comp.C,
                                alldata.N_comp.A,
                                alldata.N_comp.X,
                                alldata.N_comp.B,
                                alldata.N_comp.D,
                                alldata.N_comp.const)
                except FileNotFoundError:
                        pass #silently accept when the file does not exist

        @classmethod
        def save_user_cfg(cls):
                """saving the user's special settings to a json file
                """
                alldta = AllUserConfData()
                alldta.N_comp = NCompConfData(cls.N_comp)
                alldta.BLvar = cls.BLvar
                with open(cls.userhome + '/quiddit.conf', 'w') as json_file:
                        json.dump(alldta, json_file, cls = MyJsonEncoder)

class AllUserConfData:
        def __init__(self):
                self.__AllUserConfData__ = True

class NCompConfData:
        def __init__(self, vector):
                self.__NCompConfData__ = True
                self.C = vector[0]
                self.A = vector[1]
                self.X = vector[2]
                self.B = vector[3]
                self.D = vector[4]
                self.const = vector[5]

class MyJsonEncoder(json.JSONEncoder):
        
        def default(self, o): # pylint: disable=E0202
                if isinstance(o, NCompConfData):
                        return o.__dict__
                if isinstance(o, AllUserConfData):
                        return o.__dict__
                elif isinstance(o, np.int32):
                        return int(o)
                else:
                        return super().default(o)

        @classmethod
        def decode(cls, dct):
                if "__NCompConfData__" in dct:
                        return NCompConfData((dct["C"], dct["A"], dct["X"], dct["B"], dct["D"], dct["const"] ))
                elif "__AllUserConfData__" in dct:
                        answ = AllUserConfData()
                        answ.N_comp = dct["N_comp"]
                        return answ
                else:
                        return dct
