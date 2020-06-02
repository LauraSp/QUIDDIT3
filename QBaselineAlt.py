from QUtility import *
from QSettings import *
import numpy as np
import os
import scipy.optimize as op
import sys
import matplotlib.pyplot as plt

def remove_baseline(filename, output_path, bl_type='standard'):

    IIa_spec = QUtility.read_spec(QSettings.IIa_path)

    spec_orig = QUtility.read_spec(filename)
    spec_orig = QUtility.spectrum_slice(spec_orig, 400, 7000)
  
    #unsaturated = np.where(spectrum_pre[:,1] < 3.8)
    #spectrum_prelim = spectrum_pre[unsaturated]
    
    #bl = -QUtility.height(np.max(spectrum_prelim[:,0]), spectrum_prelim)
    bl = -spec_orig[-1][1]

    spec_prelim_abs = spec_orig[:,1] + bl

    spec_prelim = np.column_stack((spec_orig[:,0], spec_prelim_abs))

    IIa_spec_ip = QUtility.inter(IIa_spec, spec_prelim[:,0:-1], inttype='linear')


    print('preliminary correction...')
    if bl_type == 'old':
        I_1992 = QUtility.height(1992, spec_prelim)
        factor = 12.3/abs(I_1992)                       # calculate scaling factor 

        spec_prelim[:,1] *= factor

        two_phonon_left = QUtility.spectrum_slice(spec_prelim, 1500,2312)
        two_phonon_right = QUtility.spectrum_slice(spec_prelim, 2391, 3000)
        two_phonon_extra = QUtility.spectrum_slice(spec_prelim, 3800, 4000)
        two_phonon = np.vstack((two_phonon_left, two_phonon_right, two_phonon_extra))

        two_phonon_wav = np.arange(two_phonon[:,0][0], two_phonon[:,0][-1], 0.1)
        two_phonon_ip = QUtility.inter(spec_prelim, two_phonon_wav, inttype='linear')          # interpolate slice of spectrum used for fitting    
        
        IIa_spec_ip_new = QUtility.inter(IIa_spec, two_phonon_wav, inttype='linear')            # interpolate relevant area of type IIa spectrum
    
        IIa_args = (two_phonon_wav, two_phonon_ip, IIa_spec_ip_new)     # arguments needed for IIa_fit
        IIa_x0 = [(1, 0, 0)]                                    #initial guess of parameters (normf, poly1, poly2)
        IIa_bounds = [(0.0, None),(None, None),(None, None)]         #(min, max)-pairs for parameters 
        IIa_res = op.minimize(QUtility.IIa, args=IIa_args, x0=IIa_x0, method='L-BFGS-B', bounds=IIa_bounds)
        
        print(IIa_res)
    
        fit_IIa = QUtility.IIa_fit(IIa_res.x,
                                    spec_prelim[:,0].reshape(len(spec_prelim[:,0]),1),
                                                            spec_prelim[:,1].reshape(len(spec_prelim[:,1]),1)) 
        abs_temp = fit_IIa - IIa_spec_ip
    
        spec_final = np.column_stack((spec_prelim[:,0] , abs_temp))

    
    elif bl_type == 'standard':
        I_2670 = QUtility.height(2670, spec_prelim)
        I_2442 = QUtility.height(2442, spec_prelim)

        dist = I_2442 - I_2670
        target_dist = 4
        factor = target_dist/dist

        spec_prelim[:,1] *= factor

        IIa_spec_ip = QUtility.inter(IIa_spec, spec_prelim[:,0:-1], inttype='linear')

        new_abs = spec_prelim[:,1] - IIa_spec_ip.flatten()
        new_spec = np.column_stack((spec_prelim[:,0], new_abs))


        sloping_area_left = QUtility.spectrum_slice(new_spec, 1400, 7000)
        sloping_area = np.vstack((sloping_area_left, new_spec[-1]))

        poly_params = np.polyfit(sloping_area[:,0], sloping_area[:,1], 1)

        linear_baseline = np.polyval(poly_params, new_spec[:,0])

        abs_final = new_spec[:,1] - linear_baseline

        spec_final = np.column_stack((new_spec[:,0], abs_final))


    else:
        print("")
      
    print('saving spectrum after IIa subtraction...')

    new_spec = os.path.join(output_path, ('c'+os.path.basename(filename)))
    np.savetxt(new_spec, spec_final, delimiter=',')
    
    print('--------------------------------------------------------------------')
  
if __name__ == "__main__":
    remove_baseline_alt(sys.argv[1], sys.argv[2], sys.argv[3])
