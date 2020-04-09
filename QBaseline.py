from QUtility import *
from QSettings import *
import numpy as np
import os
import scipy.optimize as op
import sys

def remove_baseline(filename, output_path):
    IIa_spec = QUtility.read_spec(QSettings.IIa_path)

    spectrum_prelim = QUtility.read_spec(filename)
    spectrum_prelim = QUtility.spectrum_slice(spectrum_prelim, 675, 4000)
    
    print('preliminary correction...')
    bl= -spectrum_prelim[-1][1]
   
    spectrum_abs = spectrum_prelim[:,1] + bl              
    spectrum = np.column_stack((spectrum_prelim[:,0], spectrum_abs))
      
    mindiff = (QUtility.closest(1992.0, spectrum[:,0]))          # return wavenum closest to 1992
    row = np.where(spectrum == mindiff)[0][0]
    factor = 12.3/abs((spectrum[row,1]))                # calculate scaling factor    
    spectrum[:,1] *= factor
          
###############################################################################
################ FITTING AND SUBTRACTING TYPE IIa SPECTRUM #################### 
                                                  
    print('final fit:')                                                    
    two_phonon_left = QUtility.spectrum_slice(spectrum, 1500,2312)
    two_phonon_right = QUtility.spectrum_slice(spectrum, 2391, 3000)
    two_phonon_extra = QUtility.spectrum_slice(spectrum, 3800, 4000)
    two_phonon = np.vstack((two_phonon_left, two_phonon_right, two_phonon_extra))

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
    
    
    print('saving spectrum after IIa subtraction...')

    #np.savetxt(output_path + '/c' + filename.split('/')[-1], spec_temp, delimiter=',') 
    new_spec = os.path.join(output_path, ('c'+os.path.basename(filename)))
    np.savetxt(new_spec, spec_temp, delimiter=',')
    
    print('--------------------------------------------------------------------')

    #plt.figure()
    #plt.subplot(3,1,1)
    #plt.plot(spectrum_prelim[:,0], spectrum_prelim[:,1], 'k.', label='original')
    #plt.plot(spectrum[:,0], spectrum[:,1], label='after prelim corr.')
    #plt.legend(loc='best')
    
    #plt.subplot(3,1,2)
    #plt.plot(spectrum[:,0], spectrum[:,1], label='after prelim corr.')
    #plt.legend(loc='best')


    #plt.subplot(3,1,3)
    #plt.plot(spec_temp[:,0], spec_temp[:,1], label='final spec')
    #plt.plot(IIa_spec[:,0], IIa_spec[:,1], 'k-', label='IIa spec')
    #plt.plot(spectrum[:,0], fit_IIa, '.', label='fit')
    #plt.legend(loc='best')
    #plt.show()


  
if __name__ == "__main__":
    remove_baseline(sys.argv[1], sys.argv[2])