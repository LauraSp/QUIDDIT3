#-------------------------------------------------------------------------------
# Name:         QUIDDIT main
# Purpose:      spectral deconvolution
#
# Author:      Laura Speich
#
# Created:     20/11/2014
# Copyright:   (c) ls13943 2014
#-------------------------------------------------------------------------------

###############################################################################
####################### IMPORTING REQUIRED MODULES ############################
 
import numpy as np
import sys
import scipy.optimize as op
from scipy import integrate

from QUtility import *
from QSettings import *

###############################################################################
########################### INPUT & DATA ######################################

def deconvolution(filename, age, N_selection):

    N_selection = np.array((N_selection))

    results = np.zeros(1, dtype=QUtility.results_dtype)
    review = np.zeros(1, dtype=QUtility.review_dtype)


    C = np.column_stack((QSettings.std[:,0], QSettings.std[:,1]))
    A = np.column_stack((QSettings.std[:,0], QSettings.std[:,2]))    #generate C, A, X, B and D std
    X = np.column_stack((QSettings.std[:,0], QSettings.std[:,3]))    #spectra from CAXBD file
    B = np.column_stack((QSettings.std[:,0], QSettings.std[:,4]))   
    D = np.column_stack((QSettings.std[:,0], QSettings.std[:,5]))

    spectrum = np.loadtxt(filename, delimiter=',')          # generate np array from file

  
###############################################################################
############################ 3107cm-1 HYDROGEN PEAK ###########################

    print('fitting Pseudovoigt function to 3107 cm-1 hydrogen peak...')
    
# extract area around 3107 cm-1 H peak, fit and subtract baseline: 
    H_area = QUtility.spectrum_slice(spectrum, 3000, 3200)
    H_bg_left = QUtility.spectrum_slice(spectrum, 3000, 3050)
    H_bg_right = QUtility.spectrum_slice(spectrum, 3150, 3200)
    H_bg_both = np.vstack((H_bg_left, H_bg_right))
    
    H_p_bg = np.polyfit(H_bg_both[:,0], H_bg_both[:,1], 3)      # fit 3rd order polynomial baseline
    H_bg = np.polyval(H_p_bg, H_area[:,0])

    H_absorp_new = H_area[:,1] - H_bg
    H_wav_new = H_area[:,0]
    spec_new = np.column_stack((H_wav_new, H_absorp_new))
    
    H_bg_a, H_bg_b, H_bg_c, H_bg_d = H_p_bg
   

# fit Pseudovoigt function to 3107 cm-1 H peak:       
    H_x0 = (3107, 0, 1, 1, 0.5) #first guess for x0, I, HWHM_left and HWHM_right, sigma
    H_bounds = [(3106,3108),(0,None),(0.001,5),(0.001,5),(0,1)]

    wav_inter = np.arange(H_wav_new[0], H_wav_new[-1], 0.1)
    peak_inter = QUtility.inter(spec_new, wav_inter)

    H_res = op.minimize(QUtility.pseudovoigt, method='SLSQP', args=(wav_inter, peak_inter), x0=H_x0, bounds=H_bounds)

    #H_fit = QUtility.pseudovoigt_fit(H_wav_new, *H_res.x)
    
    H_pos, H_I, H_HWHM_l, H_HWHM_r, H_sigma = H_res.x
    
# calculate peak area:
    print('calculating peak area...')          
    H_spec = QUtility.spectrum_slice(spectrum, 3102, 3112)
    #H_spec2 = H_spec[:,1] - np.polyval(H_p_bg, H_spec[:,0])
    #H_area_numerical_data = integrate.simps(H_spec2)    
    #H_area_numerical_fit = integrate.simps(H_fit)      #integrate bg corrected fit
    H_area_analytical = 2*(H_res.x[1])*((H_res.x[2]+H_res.x[3])/2)*(H_res.x[4]*(np.pi/2)+(1-H_res.x[4])*np.sqrt(np.pi/2))      
          
###############################################################################
############################## PLATELET PEAK ##################################   
    
# extract area around platelet peak, fit and subtract preliminary background   
    print('fitting pseudovoigt function to platelet peak...')  
    pp = QUtility.spectrum_slice(spectrum, 1327, 1420)         # extract area around pp
    pp2 = QUtility.spectrum_slice(spectrum, 1350, 1380)
        
    #pp_wav_inter = np.arange(pp[0][0], pp[-1][0], 0.01)
    pp_wav_inter = np.arange(pp[0][0], pp[-1][0], 0.1)

    pp_inter = QUtility.inter(pp, pp_wav_inter)

# calculations for bounds
    I1405 = 0.257 * H_res.x[1]      #from empirical analysis on platelet degraded spectra 
    H_lb = I1405 * 0.8
    H_ub = I1405 * 1.2

    I1332 = QUtility.height(1332, pp)
    if I1332 <= 0:
         B_lb = 0
         B_ub = .5
    else:
        B_lb = I1332 - .1*I1332
        B_ub = I1332 + .1*I1332
    
    p_max = pp2[np.argmax(pp2[:,1])][0]
    p_lb = p_max - 1.5
    p_ub = p_max + 1.5
    
    cc = min(pp[:,1])
    if cc>=0:
        c_ub = cc
        c_lb = 0
    else:
        c_ub = 0
        c_lb = cc

# fit pseudovogt functions to platelet peak, 1405 and 1332 at the same time
    psv_x0 = (p_max, 0, 5, 5, 1, 1405, I1405, 5, 5, 1, 1332, I1332, 5, 5, 0, 0)
    p_bounds = [(p_lb,p_ub),(0,None),(.01,50),(.01,50),(0,1),(1404.5,1405.5),(H_lb,H_ub),(.1,5),(.1,5),(0,1),(1331,1333),(B_lb,B_ub),(.1,5),(.1,5),(0,1), (c_lb,c_ub)] 
    cons = ({'type': 'ineq', 'fun': QUtility.pp_cons1}, {'type': 'ineq', 'fun': QUtility.pp_cons2}, {'type': 'ineq', 'fun': QUtility.pp_cons3})    

    pp_res = op.minimize(QUtility.ultimatepsv, x0=psv_x0, args=(pp_wav_inter, pp_inter), method='SLSQP', bounds=p_bounds, constraints=cons)
    #pp_fit = QUtility.ultimatepsv_fit(pp_wav_inter, *pp_res.x)                        
    
    if pp_res.success != True:
        print('trying alternative method for fitting platelet peak')
        psv_x0 = QSettings.pp_res_prev
        pp_res = op.minimize(QUtility.ultimatepsv, x0=psv_x0, args=(pp_wav_inter, pp_inter), method='SLSQP', bounds=p_bounds, constraints=cons)
        #pp_fit = utility.ultimatepsv_fit(pp_wav_inter, *pp_res.x)                              
        
        
    pp_sumsqu = pp_res.fun     
      
    
    #if pp_res.success == True and pp_res.x[1]>=1:
    if pp_res.x[1]>0:
        p_x0, p_I, p_HWHM_l, p_HWHM_r, p_sigma, H1405_x0, H1405_I, H1405_HWHM_l, H1405_HWHM_r, H1405_sigma, B_x0, B_I, B_HWHM_l, B_HWHM_r, B_sigma, psv_c = pp_res.x       
        
        # calculate peak area in different ways:
        print('calculating peak area and peak symmetry...')
        if pp_res.x[2]<1:
            int_lower_bound = pp_res.x[0] - 15
        else:
            int_lower_bound = pp_res.x[0] - 15*pp_res.x[2]
        
        if pp_res.x[3]<1:
            int_upper_bound = pp_res.x[0] + 15
        else:
            int_upper_bound = pp_res.x[0] + 15*pp_res.x[3]
            
        pp_spec = QUtility.spectrum_slice(spectrum, int_lower_bound, int_upper_bound)
        
        #H1405_psv = utility.pseudovoigt_fit(pp_spec[:,0],*pp_res.x[5:10])
        
        #B_psv = utility.pseudovoigt_fit(pp_spec[:,0],*pp_res.x[10:-1])
        
        pp_abs_new = QUtility.pseudovoigt_fit(pp_spec[:,0],*pp_res.x[:5])
            
        p_area_numerical_data = integrate.simps(pp_abs_new)
        #p_area_numerical_fit = integrate.simps(utility.pseudovoigt_fit(pp_spec[:,0],*pp_res.x[:5]))      #integrate bg corrected fit
        p_area_analytical = 2*(pp_res.x[1])*((pp_res.x[2]+pp_res.x[3])/2)*(pp_res.x[4]*(np.pi/2)+(1-pp_res.x[4])*np.sqrt(np.pi/2))                                       
                                                                                                                                        

# symmetry calculations:
        sym_lower_bound = pp_res.x[0]-5*pp_res.x[2]
        sym_upper_bound = pp_res.x[0]+5*pp_res.x[3]
        
        wavenum_l = np.linspace(sym_lower_bound, pp_res.x[0], 100)
        wavenum_r = np.linspace(pp_res.x[0], sym_upper_bound, 100)
        
        absorp_l = QUtility.pseudovoigt_fit(wavenum_l, *pp_res.x[:5])
        absorp_r = QUtility.pseudovoigt_fit(wavenum_r, *pp_res.x[:5])         

# peak asymmetry factor (As):    
        I10 = 0.1 * pp_res.x[1]    
        wav10_l=np.where(absorp_l == QUtility.closest(I10, absorp_l))[0][0]
        wav10_r=np.where(absorp_r == QUtility.closest(I10, absorp_r))[0][0]

        a_As = wavenum_r[wav10_r]-pp_res.x[0]
        b_As = pp_res.x[0] - wavenum_l[wav10_l]
    
        asymmetry_factor=b_As/a_As

    
# tailing factor (Tf):
        I5 = 0.05 * pp_res.x[1]
        wav5_l=np.where(absorp_l == QUtility.closest(I5, absorp_l))[0][0]
        wav5_r=np.where(absorp_r == QUtility.closest(I5, absorp_r))[0][0]   

        a_Tf = wavenum_r[wav5_r]-pp_res.x[0]
        b_Tf = pp_res.x[0] - wavenum_l[wav5_l]
            
        tailing_factor=a_Tf+b_Tf/(2*a_Tf)

# integral breadth (beta):
        integral_breadth = p_area_numerical_data/pp_res.x[1]
    
# form factor (phi):
        form_factor = (pp_res.x[2]+pp_res.x[3])/integral_breadth
    
# centroid/weighted average:
        avg=(np.average(pp_spec[:,0], weights=pp_abs_new))         
        
        
    else:
        print('no platelet peak found')
        
        
        p_x0 = p_I = p_HWHM_l = p_HWHM_r = p_sigma = B_x0 = B_I = B_HWHM_l = B_HWHM_r = B_sigma = H1405_x0 = H1405_I = H1405_HWHM_l = H1405_HWHM_r = H1405_sigma = psv_c = np.nan       
        
        p_area_numerical_data = p_area_numerical_fit = p_area_analytical = asymmetry_factor = tailing_factor = integral_breadth = form_factor = avg = np.nan                                           

    pp_res_prev = pp_res.x

###############################################################################
########################### NITROGEN AGGREGATION ##############################        
    
# interpolate A, B and D spectra and sample spectrum:
    print('calculating N aggregation data...')
    N_area = QUtility.spectrum_slice(spectrum, 1001, 1399)
    N_wav_new = N_area[:,:-1]  

    C_new = QUtility.inter(C, N_wav_new)   
    A_new = QUtility.inter(A, N_wav_new)
    X_new = QUtility.inter(X, N_wav_new)                     # interpolate C, A, X, B and D spectra
    B_new = QUtility.inter(B, N_wav_new)
    D_new = QUtility.inter(D, N_wav_new)
    
    N_area_new = QUtility.inter(N_area, N_wav_new)          # interpolate measured spectrum (N part)
    N_area_new = N_area_new.flatten()
    
# initial parameters and bounds for fit:
    min_area = 5
    
    if p_area_analytical < min_area:
        N_x0_d = 0.0
    else:
        N_x0_d = None        

    
    if N_selection[-1] == 1:    
        
        polyx0 = N_area[-1,1]    
        if polyx0 >0:        
            polybounds = (0., polyx0)    
        else:
            polybounds = (polyx0, 0.)
    else:
        polyx0 = 0
        polybounds = (0.,0.)
    
                
    N_x0 = [i for i,j in zip((.5, .5, .1, .5, 0., -polyx0), N_selection) if j==1] # initial guess for c, a, x, b, d and poly1
    N_bounds =  [i for i,j in zip([(0.,None),(0.,None),(0.,None),(0.,None),(0., N_x0_d), polybounds], N_selection) if j==1] # bounds for c, a, x, b and d ((min, max)-pairs)

    N_args = np.column_stack((C_new, A_new, X_new, B_new, D_new))[:,np.where(N_selection[:-1]==1)[0]]     # arguments needed for least-squares fit of ABD-function
    
    # optimization:
    #N_cons = ({'type': 'ineq', 'fun': QUtility.Nd_bound, 'args': N_selection})
    #N_res = op.minimize(QUtility.CAXBD_err, x0=N_x0, args=(N_args, N_area_new), method='SLSQP', bounds=N_bounds, constraints=N_cons)
    N_cons = []
    N_res = []
    
    if (N_selection[4] == 1 & N_selection[3] == 1): #both B and D used
        if np.array_equal(N_selection, (0, 0, 0, 1, 1, 0)):       #BD
            N_cons = ({'type': 'ineq', 'fun': QUtility.Nd_bound1})
        elif np.array_equal(N_selection, (0, 0, 0, 1, 1, 1)):     #BDconst
            N_cons = ({'type': 'ineq', 'fun': QUtility.Nd_bound2})
        elif np.array_equal(N_selection, (0, 1, 0, 1, 1, 0)):     #ABD
            N_cons = ({'type': 'ineq', 'fun': QUtility.Nd_bound3})
        elif np.array_equal(N_selection, (0, 1, 0, 1, 1, 1)):     #ABDconst
            N_cons = ({'type': 'ineq', 'fun': QUtility.Nd_bound4})
        elif np.array_equal(N_selection, (1, 0, 0, 1, 1, 0)):     #CBD
            N_cons = ({'type': 'ineq', 'fun': QUtility.Nd_bound5})
        elif np.array_equal(N_selection, (1, 0, 0, 1, 1, 1)):     #CBDconst
            N_cons = ({'type': 'ineq', 'fun': QUtility.Nd_bound6})
        elif np.array_equal(N_selection, (1, 1, 1, 1, 1, 0)):     #CAXBD
            N_cons = ({'type': 'ineq', 'fun': QUtility.Nd_bound7})
        elif np.array_equal(N_selection, (1, 1, 1, 1, 1, 1)):     #CAXBDconst
            N_cons = ({'type': 'ineq', 'fun': QUtility.Nd_bound8})
        else:
            N_cons = ()
        N_res = op.minimize(QUtility.CAXBD_err, x0=N_x0, args=(N_args, N_area_new), method='SLSQP', bounds=N_bounds, constraints=N_cons)

    else:
        N_res = op.minimize(QUtility.CAXBD_err, x0=N_x0, args=(N_args, N_area_new), method='SLSQP', bounds=N_bounds) #no constraints

    print(N_res)
    
    c, a, x, b, d, N_poly = [], [], [], [], [], []
    N_res_idx = 0
    
    for (idx, val), comp in zip(enumerate(N_selection), (c, a, x, b, d, N_poly)):
        if val == 0:
            comp.append(np.nan)
        elif val == 1:
            comp.append(N_res.x[N_res_idx])
            N_res_idx += 1
            

    N_sumsqu = N_res.fun     # sum of squares of measured - fit

# calculate concentrations of A- and B-centres and total N (in ppm):    
    NC = float(c[0])*25
    NA = float(a[0])*16.5
    NB = float(b[0])*79.4
    NT = np.sum(np.nan_to_num((NC, NA, NB)))
    
    
###############################################################################
############################### TEMPERATURE ###################################    

# note: in python "ln" is log
    age_s = age * 1e6 * 365 * 24 * 60 * 60                  #age in seconds
    T = (-81160/(np.log(((NT/NA)-1)/(age_s*NT*293608)))) - 273.15    
    
    if T < 0:
        temperature= np.nan
    else:
        temperature = T         
           
                     
###############################################################################
##################### WRITE TO RESULTS FILE ###################################
																																									
    print('saving results to file...')
        
    results['name'] = filename

    results['p_x0'] = p_x0
    results['p_I'] = p_I
    results['p_HWHM_l'] = p_HWHM_l
    results['p_HWHM_r'] = p_HWHM_r
    results['p_sigma'] = p_sigma
    results['p_area_num_data'] = p_area_numerical_data
    results['p_area_ana'] = p_area_analytical
    results['avg'] = avg
    results['p_As'] = asymmetry_factor
    results['p_Tf'] = tailing_factor
    results['p_beta'] = integral_breadth
    results['p_phi']  = form_factor
    results['p_sumsqu'] = pp_sumsqu

    results['c'] = c
    results['a'] = a  
    results['x'] = x       
    results['b'] = b         
    results['d'] = d
    results['N_poly'] = N_poly
    results['[NC]'] = NC
    results['[NA]'] = NA        
    results['[NB]'] = NB                 
    results['[NT]'] = NT
    results['T'] = temperature
    results['N_sumsqu'] = N_sumsqu

    results['I_3107'] = H_I
    results['H_area_ana'] = H_area_analytical 
												
   
    review['name'] = filename

    review['p_x0'] = p_x0
    review['p_I'] = p_I
    review['p_HWHM_l'] = p_HWHM_l
    review['p_HWHM_r'] = p_HWHM_r
    review['p_sigma'] = p_sigma
    
    review['H1405_x0'] = H1405_x0
    review['H1405_I'] = H1405_I
    review['H1405_HWHM_l'] = H1405_HWHM_l
    review['H1405_HWHM_r'] = H1405_HWHM_r
    review['H1405_sigma'] = H1405_sigma
    
    review['B_x0'] = B_x0
    review['B_I'] = B_I
    review['B_HWHM_l'] = B_HWHM_l
    review['B_HWHM_r'] = B_HWHM_r
    review['B_sigma'] = B_sigma
    
    review['psv_c'] = psv_c
    review['avg'] = avg

    review['c'] = c
    review['a'] = a
    review['x'] = x
    review['b'] = b
    review['d'] = d
    review['N_poly'] = N_poly

    review['H_bg_a'] = H_bg_a
    review['H_bg_b'] = H_bg_b
    review['H_bg_c'] = H_bg_c
    review['H_bg_d'] = H_bg_d
    review['H_pos'] = H_pos
    review['H_I'] = H_I
    review['H_HWHM_l'] = H_HWHM_l
    review['H_HWHM_r'] = H_HWHM_r
    review['H_sigma'] = H_sigma

    review['path'] = filename                      

    return results, review             
                    

###############################################################################
############################## OVERALL PLOTTING ###############################


if __name__ == "__main__":
    deconvolution(sys.argv[0], sys.argv[1], sys.argv[2]) 