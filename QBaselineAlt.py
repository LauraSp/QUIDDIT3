from QUtility import *
from QSettings import *
import numpy as np
import os
import scipy.optimize as op
import sys
import matplotlib.pyplot as plt

def remove_baseline_alt(filename, output_path, bl_type='standard'):

    #assert(bl_type in ('standard','saturated')), "Baseline type not recognised.")

    IIa_spec = QUtility.read_spec(QSettings.IIa_path)

    spectrum_prelim = QUtility.read_spec(filename)
    spectrum_prelim = QUtility.spectrum_slice(spectrum_prelim, 675, 4000)
    
    bl= -spectrum_prelim[-1][1]
   
    spectrum_abs = spectrum_prelim[:,1] + bl              
    spectrum = np.column_stack((spectrum_prelim[:,0], spectrum_abs))


    print('preliminary correction...')
    if bl_type == 'standard':
        mindiff = (QUtility.closest(1992.0, spectrum[:,0]))          # return wavenum closest to 1992
        row = np.where(spectrum == mindiff)[0][0]
        factor = 12.3/abs((spectrum[row,1]))                        # calculate scaling factor    
    
    elif bl_type == 'saturated':
        I_2670 = QUtility.height(2670, spectrum)
        I_2442 = QUtility.height(2442, spectrum)
    
        dist = I_2442 - I_2670
        target_dist = 4
        factor = target_dist/dist

    spectrum[:,1] *= factor
    
    #plt.figure()
    #plt.plot(spectrum_prelim[:,0], spectrum_prelim[:,1], '.', label='orig. data')
    #plt.plot(spectrum[:,0], spectrum[:,1], '.', label='spec after prelim. cor.')

    
          
###############################################################################
################ FITTING AND SUBTRACTING TYPE IIa SPECTRUM #################### 
                                                  
    print('final fit:')                                                    
    if bl_type == 'standard':
        two_phonon_left = QUtility.spectrum_slice(spectrum, 1500,2312)
        two_phonon_right = QUtility.spectrum_slice(spectrum, 2391, 3000)
        two_phonon_extra = QUtility.spectrum_slice(spectrum, 3800, 4000)

        two_phonon = np.vstack((two_phonon_left, two_phonon_right, two_phonon_extra))  
    
    elif bl_type == 'saturated':
        two_phonon_left = QUtility.spectrum_slice(spectrum, 1600, 1800)
        two_phonon_right = QUtility.spectrum_slice(spectrum, 2391, 3000)
        two_phonon_extra = QUtility.spectrum_slice(spectrum, 3900, 4000)
        #two_phonon_extra = QUtility.spectrum_slice(spectrum, 3200, 4000)

        two_phonon = np.vstack((two_phonon_left, two_phonon_right))#, two_phonon_extra))
        #plt.plot(two_phonon[:,0], two_phonon[:,1], 'o', color='0.6')


    two_phonon_wav = np.arange(two_phonon[:,0][0], two_phonon[:,0][-1], 0.1)
    two_phonon_ip = QUtility.inter(spectrum, two_phonon_wav, inttype='linear')          # interpolate slice of spectrum used for fitting    

    IIa_spec_ip = QUtility.inter(IIa_spec, two_phonon_wav, inttype='linear')            # interpolate relevant area of type IIa spectrum
    IIa_spec_ip_new = QUtility.inter(IIa_spec, spectrum[:,0:-1], inttype='linear')
    
    IIa_args = (two_phonon_wav, two_phonon_ip, IIa_spec_ip)     # arguments needed for IIa_fit
    IIa_x0 = [(1, 0, 0)]                                    #initial guess of parameters (normf, poly1, poly2)
    IIa_bounds = [(0.0, None),(None, None),(None, None)]         #(min, max)-pairs for parameters 
    IIa_res = op.minimize(QUtility.IIa, args=IIa_args, x0=IIa_x0, method='L-BFGS-B', bounds=IIa_bounds)
        
    
    print(IIa_res)
    
    fit_IIa = QUtility.IIa_fit(IIa_res.x, spectrum[:,0].reshape(len(spectrum[:,0]),1), spectrum[:,1].reshape(len(spectrum[:,1]),1)) 
    #sumsqu = IIa_res.fun
    abs_temp = fit_IIa - IIa_spec_ip_new
    
    spec_temp = np.column_stack((spectrum[:,0] , abs_temp))
    
    #plt.plot(IIa_spec[:,0], IIa_spec[:,1], '-.', label='IIa')
    ##plt.plot(spectrum[:,0], fit_IIa, 'k-', label='fit to IIa')
    #plt.plot(spec_temp[:,0], spec_temp[:,1], '.', label='final cor.')
    #plt.legend(loc='best')
    #ax = plt.gca()
    #ax.invert_xaxis()
    
    
    print('saving spectrum after IIa subtraction...')

    #np.savetxt(output_path + '/c' + filename.split('/')[-1], spec_temp, delimiter=',')

    new_spec = os.path.join(output_path, ('c'+os.path.basename(filename)))
    np.savetxt(new_spec, spec_temp, delimiter=',')
    #np.savetxt(output_path + '/c' + filename.split('\\')[-1], spec_temp, delimiter=',')
    
    print('--------------------------------------------------------------------')
  
if __name__ == "__main__":
    remove_baseline_alt(sys.argv[1], sys.argv[2], sys.argv[3])
