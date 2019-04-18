# -*- coding: utf-8 -*-
"""
Created on Mon Sep 04 12:21:20 2017
This file contains all functions created for QUIDDIT
@author: ls13943
"""
##############################################################################
##################### IMPORT STANDARD PYTHON LIBRARIES #######################

import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as op
from scipy import interpolate
from scipy import integrate
from scipy import stats
#import matplotlib as mpl

##############################################################################
############################# DEFINE FUNCTIONS ###############################
class QUtility:
    @staticmethod
    def closest(target, collection):
        """returns value from collection that is closest to target"""
        return min((abs(target-i),i) for i in collection)[1]

    @staticmethod
    def spectrum_slice(spec, lower, higher):
        """returns a slice of a spectrum with wavenumbers between (and including) lower and higher"""
        spec_slice = [x for x in spec if lower <= x[0] <=higher]
        return np.array(spec_slice, dtype='float64')  
    
    @staticmethod
    def inter(spectrum, wav_new, inttype='linear'):
        """returns interpolated spectrum"""
        spec_interp = interpolate.interp1d(spectrum[:,0],spectrum[:,1], kind=inttype, bounds_error=False, fill_value=0)
        return spec_interp(wav_new)
    
    @staticmethod
    def IIa(params, wavenum, absorp, IIa):
        normf, poly1, poly2 = params
        fitted_spec = absorp * normf - np.polyval((poly1, poly2), wavenum)
        residual = IIa - fitted_spec
        return np.sum(residual**2)
    
    @staticmethod
    def IIa_fit(params, wavenum, absorp):
        """returns type IIa spectrum multiplied by normf plus linear baseline"""
        normf, poly1, poly2 = params
        model_spec = absorp * normf - np.polyval((poly1, poly2), wavenum)
        return model_spec   
    
    @staticmethod
    def height(wavenum, spectrum):
        mindiff = np.where(QUtility.closest(wavenum, spectrum[:,0]) == spectrum[:,0])[0]
        I = spectrum[mindiff,1]
        return float(I)
 
    @staticmethod
    def peak_area(I, HWHM_l, HWHM_r, sigma):
        return I*(HWHM_l+HWHM_r)*(sigma*(np.pi/2)+(1-sigma)*np.sqrt(np.pi/2))

    @staticmethod 
    def lorentzian(x, x0, I, HWHM_l, HWHM_r):
        """returns two lorentzian functions with the same x0 (position of peak maximum) and 
        I (intensity at peak maximum) but different HWHM (half width at half maximum)"""
    #numerator =  (HWHM**2 )
    #denominator = ( x - x0 )**2 + HWHM**2
    #return I*(numerator/denominator)
    
        x_left = x[(x<=x0)]
        x_right = x[(x>x0)]
        numerator_left = HWHM_l**2
        denominator_left = (x_left - x0)**2 + HWHM_l**2
        y_left = I * (numerator_left/denominator_left) #Lorentzian #1
    
        numerator_right = HWHM_r**2   
        denominator_right = (x_right - x0)**2 + HWHM_r**2    
        y_right = I * (numerator_right/denominator_right) #Lorentzian #2
    
        return np.hstack((y_left, y_right))    #return combination of both Lorentzians
    
    @staticmethod
    def gaussian(x, x0, I, HWHM_l, HWHM_r):
        """returns two gaussian functions with the same x0 (position of peak maximum) and 
        I (intensity at peak maximum) but different HWHM (half width at half maximum)"""
    #    numerator = (x-x0)**2
    #    denominator = 2*HWHM**2
    #    return I*np.exp(-numerator/denominator)

        x_l = x[(x<=x0)]
        x_r = x[(x>x0)]
    
        numerator_l = (x_l-x0)**2    
        denominator_l = 2*HWHM_l**2
        y_l = I*np.exp(-numerator_l/denominator_l)
    
        numerator_r = (x_r-x0)**2      
        denominator_r = 2*HWHM_r**2  
        y_r = I*np.exp(-numerator_r/denominator_r)
    
        return np.hstack((y_l, y_r))    #return combination of both Gaussians

    @staticmethod
    def pseudovoigt(params, *args):
        """returns the sum of (measured-model)**2 using a Pseudovoigt function 
        P(x) = sigma*L(x) + (1-sigma)*G(x) as model and measured absorptions"""
    
        x0, I, HWHM_l, HWHM_r, sigma = params      
        psv = sigma*QUtility.lorentzian(args[0],x0,I,HWHM_l, HWHM_r) + (1-sigma)*QUtility.gaussian(args[0],x0,I,HWHM_l,HWHM_r)
    
        error = args[1] - psv
        return np.sum(error**2)

    @staticmethod
    def pseudovoigt_const(params, *args):
        """returns the sum of (measured-model)**2 using a Pseudovoigt function 
        P(x) = sigma*L(x) + (1-sigma)*G(x) as model and measured absorptions"""
    
        x0, I, HWHM_l, HWHM_r, sigma, const = params      
        psv = sigma*QUtility.lorentzian(args[0],x0,I,HWHM_l, HWHM_r) + (1-sigma)*QUtility.gaussian(args[0],x0,I,HWHM_l,HWHM_r) + const
    
        error = args[1] - psv
        return np.sum(error**2)
    
    @staticmethod
    def pseudovoigt_fit(x,x0,I,HWHM_l,HWHM_r,sigma):
        """a Pseudovoigt function P(x) = sigma*L(x) + (1-sigma)*G(x)"""
        psv = sigma*QUtility.lorentzian(x,x0,I,HWHM_l, HWHM_r) + (1-sigma)*QUtility.gaussian(x,x0,I,HWHM_l,HWHM_r)
        return psv
    
    @staticmethod
    def ultimatepsv(params, *args):
        p_x0, p_I, p_HWHM_l, p_HWHM_r, p_sigma, H_x0, H_I, H_HWHM_l, H_HWHM_r, H_sigma, B_x0, B_I, B_HWHM_l, B_HWHM_r, B_sigma, c = params
        p_psv = p_sigma*QUtility.lorentzian(args[0],p_x0,p_I,p_HWHM_l, p_HWHM_r) + (1-p_sigma)*QUtility.gaussian(args[0],p_x0,p_I,p_HWHM_l,p_HWHM_r)
        H_psv = H_sigma*QUtility.lorentzian(args[0],H_x0,H_I,H_HWHM_l, H_HWHM_r) + (1-H_sigma)*QUtility.gaussian(args[0],H_x0,H_I,H_HWHM_l,H_HWHM_r)
        B_psv = B_sigma*QUtility.lorentzian(args[0],B_x0,B_I,B_HWHM_l, B_HWHM_r) + (1-B_sigma)*QUtility.gaussian(args[0],B_x0,H_I,B_HWHM_l,B_HWHM_r)
        psv_all = p_psv + H_psv + B_psv + c
        error = args[1] - psv_all
        return np.sum(error**2)
    
    @staticmethod
    def ultimatepsv_fit(x, p_x0, p_I, p_HWHM_l, p_HWHM_r, p_sigma, H_x0, H_I, H_HWHM_l, H_HWHM_r, H_sigma, B_x0, B_I, B_HWHM_l, B_HWHM_r, B_sigma, c):  
        p_psv = p_sigma*QUtility.lorentzian(x,p_x0,p_I,p_HWHM_l, p_HWHM_r) + (1-p_sigma)*QUtility.gaussian(x,p_x0,p_I,p_HWHM_l,p_HWHM_r)
        H_psv = H_sigma*QUtility.lorentzian(x,H_x0,H_I,H_HWHM_l, H_HWHM_r) + (1-H_sigma)*QUtility.gaussian(x,H_x0,H_I,H_HWHM_l,H_HWHM_r)
        B_psv = B_sigma*QUtility.lorentzian(x,B_x0,B_I,B_HWHM_l, B_HWHM_r) + (1-B_sigma)*QUtility.gaussian(x,B_x0,H_I,B_HWHM_l,B_HWHM_r)
        psv_all = p_psv + H_psv + B_psv + c
        if psv_all.size == 0:
            psv_all = np.zeros(len(x))
            psv_all[:] = np.nan
        return psv_all  

    @staticmethod
    def ABD(params, *args):
        """returns the sum of (measured-model)**2 using interpolated model spectra for the A, B and D components""" 
        absorp, A, B, D = args    
        a, b, d, poly1 = params  
        model_spec = a*A + b*B + d*D + poly1
        residual = absorp - model_spec
        return np.sum(residual**2)

    @staticmethod
    def ABD_fit(a, b, d, poly1, A, B, D):
        """returns sum of A, B and D spectra weighted by a, b and d"""
        return a*A + b*B + d*D + poly1 

    @staticmethod
    def CAXBD(factors, components):
        """returns sum of A, B and D spectra weighted by a, b and d"""
        #print('factors: {}'.format(factors))
        #print('components: {}'.format(components))
        factors = np.nan_to_num(factors)
        model_spec = np.sum(factors[:-1] * components, axis=1) + factors[-1]
        return np.array(model_spec)
    
    @staticmethod
    def CAXBD_err(factors, components, absorp):
        model_spec = QUtility.CAXBD(factors, components)
        residual = absorp - model_spec
        return np.sum(residual**2)   

    @staticmethod
    def Temp_N(t, NT, IaB):
        """calculate T in celsius using age in seconds (t), NT and aggregation state (IaB)"""   
        NA = NT * (1-IaB)
        T = (-81160/(np.log(((NT/NA)-1)/(t*NT*293608))))
        return T-273

    @staticmethod
    def aggregate(T1, NT, T2, IaB_measured, t1, t2):
        """input: NT,t1,t2, measured agg (prop. of B), T2.
        vary T1, until IaB2 matches IaBt
        """
        EaR = 81160
        preexp = 293608
        NA0 = NT    #A centres before aggregation starts
        rate1 = preexp * np.exp(-EaR/(T1+273))
        NA1 =  NA0/(1+(rate1*NA0)*t1)     #A centres after first stage of annealing
        rate2 = preexp * np.exp(-EaR/(T2+273))
        NA2 = NA1/(1+(rate2*NA1)*t2)      #A centres after second stage of annealing
        IaB_calc = 1-(NA2/NT)
        error = IaB_measured - IaB_calc
        return error**2   

    @staticmethod
    def Nd_bound1(params):
        b, d = params
        return .365*b - d

    @staticmethod
    def Nd_bound2(params):
        b, d, const = params
        return .365*b - d 

    @staticmethod
    def Nd_bound3(params):
        a, b, d = params
        return .365*b - d 

    @staticmethod
    def Nd_bound4(params):
        a, b, d, const = params
        return .365*b - d 

    @staticmethod
    def Nd_bound5(params):
        c, a, x, b, d = params
        return .365*b - d

    @staticmethod
    def Nd_bound6(params):
        c, a, x, b, d, const = params
        return .365*b - d
    
    @staticmethod
    def pp_cons1(params):
        p_x0, p_I, p_HWHM_l, p_HWHM_r, p_sigma, H_x0, H_I, H_HWHM_l, H_HWHM_r, H_sigma, B_x0, B_I, B_HWHM_l, B_HWHM_r, B_sigma, c = params
        return 10-abs(H_HWHM_l - H_HWHM_r)
    
    @staticmethod
    def pp_cons2(params):
        p_x0, p_I, p_HWHM_l, p_HWHM_r, p_sigma, H_x0, H_I, H_HWHM_l, H_HWHM_r, H_sigma, B_x0, B_I, B_HWHM_l, B_HWHM_r, B_sigma, c = params
        return 10-abs(B_HWHM_l - B_HWHM_r)

    @staticmethod
    def pp_cons3(params):
        p_x0, p_I, p_HWHM_l, p_HWHM_r, p_sigma, H_x0, H_I, H_HWHM_l, H_HWHM_r, H_sigma, B_x0, B_I, B_HWHM_l, B_HWHM_r, B_sigma, c = params
        return 10-abs(p_HWHM_r-p_HWHM_l)

    @staticmethod
    def make_2dgrid(x, y, grid_x, grid_y, param):
        grid = interpolate.griddata((x,y), param, (grid_x,grid_y), method='linear', fill_value=np.nan)
        return grid.T


###############################################################################
######################### QUIDDIT DATA TYPES ##################################
    
    results_dtype=np.dtype([('name', '|O8'),('p_x0','float64'),('p_I','float64'), ('p_HWHM_l','float64'),('p_HWHM_r','float64'),('p_sigma','float64'), 
        ('avg','float64'), ('p_area_num_data','float64'), ('p_area_ana','float64'), 
        ('p_As','float64'), ('p_Tf','float64'), ('p_beta','float64'), ('p_phi','float64'), ('p_sumsqu','float64'), 
        ('c','float64'),('a','float64'), ('x', 'float64'), ('b','float64'), ('d', 'float64'), ('N_poly','float64'),
        ('[NC]','float64'), ('[NA]','float64'), ('[NB]','float64'), ('[NT]','float64'), ('T', 'float64'), ('N_sumsqu','float64'), 
        ('I_3107','float64'), ('H_area_ana','float64'),])
    
    res_header = 'name, p_x0, p_I, p_HWHM_l, p_HWHM_r, p_sigma, avg, area_num_data, area_ana, As, Tf, beta, phi, pp_sumsqu, c, a, x, b, d, const, [NC], [NA], [NB], [Nt], T, N_sumsqu, I_3107, H_area_ana'

                    
    review_dtype=np.dtype([('name', '|O8'), ('p_x0','float64'),('p_I','float64'), ('p_HWHM_l','float64'),('p_HWHM_r','float64'),('p_sigma','float64'),
        ('H1405_x0', 'float64'), ('H1405_I', 'float64'), ('H1405_HWHM_l','float64'), ('H1405_HWHM_r','float64'), ('H1405_sigma','float64'),
        ('B_x0','float64'), ('B_I', 'float64'), ('B_HWHM_l','float64'), ('B_HWHM_r','float64'), ('B_sigma','float64'), ('psv_c','float64'), ('p_s2n','float64'),
        ('avg','float64'), ('c','float64'),('a','float64'), ('x', 'float64'), ('b','float64'), ('d', 'float64'), ('N_poly', 'float64'), 
        ('H_bg_a','float64'),('H_bg_b','float64'), ('H_bg_c','float64'),('H_bg_d','float64'), ('H_pos','float64'),('H_I','float64'), 
        ('H_HWHM_l','float64'),('H_HWHM_r','float64'),('H_sigma','float64') , ('path', 'S100')])
    
    rev_header = 'name, p_x0, p_I, p_HWHM_l, p_HWHWM_r, p_sigma, H1405_x0, H1405_I, H1405_HWHM_l, H1405_HWHWM_r, H1405_sigma, B_x0, p_I, B_HWHM_l, B_HWHWM_r, B_sigma, p_s2n, psv_c, avg, c, a, x, b, d, const, H_bg_a, H_bg_b, H_bg_c, H_bg_d, H_x0, H_I, H_HWHM_l, H_HWHM_r, H_sigma, path'


    peakfit_dtype = np.dtype([('name', '|O8'), ('x0','float64'),('I','float64'), ('HWHM_l','float64'),('HWHM_r','float64'),('sigma','float64'),('area_ana','float64'),('area_num','float64'),
        ('bg_a','float64'),('bg_b','float64'), ('bg_c','float64'),('bg_d','float64')])
    
    peakfit_header = 'name, x0, I, HWHM_l, HWHM_r, sigma, area_ana, area_num, bg_a, bg_b, bg_c, bg_d'