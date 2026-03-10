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

    version = '3.2-alpha'
    github_url = 'https://github.com/LauraSp/QUIDDIT3'

    # Path to file with standard spectra of N components (CSV)
    std_path = os.getcwd() + '/CAXBD.csv'

    IIa_path = os.getcwd() + '/typeIIa.csv'
    IIa_alt_path = os.getcwd() + '/typeIIa_alt.csv'
    std = np.loadtxt(std_path, delimiter=',')     # read CAXBD spectra

    # Standard first guess for platelet fit (p_x0, p_I, p_HWHM_l, p_HWHM_r, p_sigma,
    # H1405_x0, H1405_I, H1405_HWHM_l, H1405_HWHM_r, H1405_sigma, 
    # B_x0, B_I, B_HWHM_l, B_HWHM_r, B_sigma,
    # const)

    pp_res_prev = (1370, 0, 5, 5, 1,
                   1405, 0, 5, 5, 1,
                   1332, 0, 5, 5, 0,
                   1)

    ori_N_comp = np.array((0, 1, 0, 1, 1, 1))
    N_comp = np.array(ori_N_comp)

    ori_BLvar = "standard"
    BLvar = ori_BLvar

    # whether spectra should be shown during batch deconvolution
    ori_plot_during_deconv = True
    plot_during_deconv = ori_plot_during_deconv

    # whether to show detailed deconvolution results in message window
    ori_long_print_output = True
    long_print_output = ori_long_print_output

    saturated = 3.8

    ENVIITEMS = (1992, 1360, 1344, 1282, 1170, 1130)

    PLOTITEMS = (
        '$[N_T]$ (ppm)',
        '$[N_C]$ (ppm)',
        '$[N_A]$ (ppm)',
        '$[N_B]$ (ppm)',
        '$[N_B]/[N_T]$',
        r'$T (^{\circ}C)$',
        'platelet peak position $(cm^{-1})$',
        'platelet peak area $(cm^{-2})$',
        'platelet peak width $(cm^{-1})$',
        'platelet peak symmetry $(cm^{-1})$',
        'I(3107) $(cm^{-2})$'
        )

    PEAKPLOTITEMS = (
        '$x_0 (cm^{-1})$',
        '$I (cm^{-1})$',
        'FWHM $(cm^{-1})$',
        'sigma (-)',
        'peak area $(cm^{-2})$'
        )

    MAPCLIMS = {
        '$[N_T]$ (ppm)': (None, None),
        '$[N_C]$ (ppm)': (None, None),
        '$[N_A]$ (ppm)': (None, None),
        '$[N_B]$ (ppm)': (None, None),
        '$[N_B]/[N_T]$': (0., 1.),
        r'$T (^{\circ}C)$': (1000, 1400),
        'platelet peak position $(cm^{-1})$': (1358., 1378.),
        'platelet peak area $(cm^{-2})$': (None, None),
        'platelet peak width $(cm^{-1})$': (None, 25.),
        'platelet peak symmetry $(cm^{-1})$': (-15., 5.),
        'I(3107) $(cm^{-2})$': (None, None)
        }

    BATCHPEAKMAPCLIMS = {
        '$x_0 (cm^{-1})$': (None, None),
        '$I (cm^{-1})$': (None, None),
        'FWHM $(cm^{-1})$': (None, None),
        'sigma (-)': (0, 1),
        'peak area $(cm^{-2})$': (None, None)
        }

    STD_COLS = cm.get_cmap('jet')

    var_defaults = {
        'home': home,
        'N_comp': N_comp,
        'file_count': '',
        'namevar': '',
        'resultvar': '',
        'reviewvar': '',
        'agevar': 2900.,
        'peakvar': 3107.0,
        'c_NT_var': 0.,
        'r_NT_var': 0.,
        'c_agg_var': 0.,
        'r_agg_var': 0.,
        'plotmode': '',
        'minvar': 0.,
        'maxvar': 1.,
        'peak': 0,
        'plot_during_deconv': plot_during_deconv,
        'long_print_output': long_print_output
        }

    # settings for plotting
    colors = ['blue', 'green', 'red']
    levels = [0, 1]

    cmap, norm = mpl.colors.from_levels_and_colors(
        [1, 63, 76, 79], ['blue', 'green', 'red'])

    f = 16
    l = 2
    m = 3

    STD_DPI = 100
    STD_RES = 2000j
    user_conf_file = "quiddit.conf"

    @classmethod
    def read_user_cfg(cls): 
        """reading the user configs from a json.file"""
        try:
            with open(cls.userhome + '/quiddit.conf') as json_file:
                alldata = json.load(
                    json_file, object_hook=MyJsonEncoder.decode)

                cls.N_comp = (
                    alldata.N_comp.C,
                    alldata.N_comp.A,
                    alldata.N_comp.X,
                    alldata.N_comp.B,
                    alldata.N_comp.D,
                    alldata.N_comp.const
                    )
                cls.BLvar = alldata.BLvar.BLvar
                # output settings
                if hasattr(alldata, 'plot_flag'):
                    if isinstance(alldata.plot_flag, dict):
                        cls.plot_during_deconv = bool(
                            alldata.plot_flag.get(
                                'plot_during_deconv', cls.ori_plot_during_deconv))
                        cls.long_print_output = bool(
                            alldata.plot_flag.get(
                                'long_print_output', cls.ori_long_print_output))
                    else:
                        cls.plot_during_deconv = bool(
                            getattr(
                                alldata.plot_flag,
                                'plot_during_deconv',
                                cls.ori_plot_during_deconv))
                        cls.long_print_output = bool(
                            getattr(
                                alldata.plot_flag,
                                'long_print_output',
                                cls.ori_long_print_output))

        except FileNotFoundError:
            pass
            # silently accept when the file does not exist

    @classmethod
    def save_user_cfg(cls):
        """
        saving the user's special settings to a json file"""
        alldta = AllUserConfData()
        alldta.N_comp = NCompConfData(cls.N_comp)
        alldta.BLvar = BLandNormVar(cls.BLvar)
        alldta.plot_flag = OutputSettingsConfData(cls.plot_during_deconv, cls.long_print_output)

        with open(cls.userhome + '/quiddit.conf', 'w') as json_file:
                json.dump(alldta, json_file, cls=MyJsonEncoder)


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


class BLandNormVar:
    def __init__(self, var):
        self.__BLvar__ = True
        self.BLvar = var


class OutputSettingsConfData:
    def __init__(self, plot_val, print_val):
        self.__OutputSettingsConfData__ = True
        self.plot_during_deconv = plot_val
        self.long_print_output = print_val


class MyJsonEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if isinstance(o, NCompConfData):
            return o.__dict__
        elif isinstance(o, BLandNormVar):
            return o.__dict__
        elif isinstance(o, OutputSettingsConfData):
            return o.__dict__
        elif isinstance(o, AllUserConfData):
            return o.__dict__
        elif isinstance(o, np.int32):
            return int(o)
        elif isinstance(o, np.int64):
            return int(o)
        else:
            return super().default(o)

    @classmethod
    def decode(cls, dct):
        if "__NCompConfData__" in dct:
            return NCompConfData((dct["C"],
                                  dct["A"],
                                  dct["X"],
                                  dct["B"],
                                  dct["D"],
                                  dct["const"]))

        elif "__BLvar__" in dct:
            return BLandNormVar(dct["BLvar"])

        elif "__OutputSettingsConfData__" in dct:
            return OutputSettingsConfData(
                dct.get("plot_during_deconv"),
                dct.get("long_print_output", QSettings.ori_long_print_output))

        elif "__PlotDuringDeconvConfData__" in dct:
            return OutputSettingsConfData(
                dct.get("plot_during_deconv", QSettings.ori_plot_during_deconv),
                QSettings.ori_long_print_output)

        elif "__AllUserConfData__" in dct:
            answ = AllUserConfData()
            answ.N_comp = dct["N_comp"]
            answ.BLvar = dct["BLvar"]
            # handle optional flag if saved
            if "plot_flag" in dct:
                answ.plot_flag = dct["plot_flag"]
            return answ
        else:
            return dct
