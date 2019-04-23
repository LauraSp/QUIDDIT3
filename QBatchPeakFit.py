# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 08:14:03 2019

@author: Laura
"""

import sys
import numpy as np
import scipy.optimize as op
from scipy import integrate
from QUtility import *

def fit_peak(specfile, peak):
    
    print('Reading spectrum: {}'.format(specfile))
    spectrum = np.loadtxt(specfile, delimiter=',')
    aoi_spec = QUtility.spectrum_slice(spectrum, peak-50, peak+50)
    
    print('Fitting baseline to spectrum.')
    bg_spec_l = QUtility.spectrum_slice(spectrum, peak-50, peak-20)
    bg_spec_r = QUtility.spectrum_slice(spectrum, peak+20, peak+50)
    bg_spec = np.vstack((bg_spec_l, bg_spec_r))
    
    aoi_bg_params = np.polyfit(bg_spec[:,0], bg_spec[:,1], 3)      # fit 3rd order polynomial baseline
    aoi_bg = np.polyval(aoi_bg_params, aoi_spec[:,0])
    
    (bg_a, bg_b, bg_c, bg_d) = aoi_bg_params
    
    absorp_new = aoi_spec[:,1] - aoi_bg
    wav_new = aoi_spec[:,0]
    spec_new = np.column_stack((wav_new, absorp_new))
    
    print('Fitting peak at {}.'.format(peak))
    wav_inter = np.arange(wav_new[0], wav_new[-1], 0.1)
    peak_inter = QUtility.inter(spec_new, wav_inter)

    first_guess = (peak, 0, 1, 1, 0.5) #first guess for x0, I, HWHM_left and HWHM_right, sigma
    bounds = [(peak-2,peak+2),(0,None),(0.001,10),(0.001,10),(0,1)]
    res = op.minimize(QUtility.pseudovoigt, method='SLSQP', args=(wav_inter, peak_inter), x0=first_guess, bounds=bounds)

    #fit = utility.pseudovoigt_fit(wav_new, *res.x)
    (pos, I, HWHM_l, HWHM_r, sigma) = res.x
    area_ana = QUtility.peak_area(I, HWHM_l, HWHM_r, sigma)
    
    area_num = integrate.simps(absorp_new)
    
    for item in zip((pos, I, HWHM_l, HWHM_r, sigma), ('pos','I', 'HWHM_l','HWHM_r','sigma')):
        print(item[1]+': '+str(item[0])+'\n') 
        
    return (specfile, pos, I, HWHM_l, HWHM_r, sigma, area_ana, area_num, bg_a, bg_b, bg_c, bg_d)

if __name__ == "__main__":
    fit_peak(sys.argv[1], sys.argv[2])