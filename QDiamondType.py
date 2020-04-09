import numpy as numpy
from QUtility import *
from QSettings import *

def diamondtype(filename, savecorrected=False, outpath=''):
    warn = []
    
    print('spectrum: {}'.format(filename))

    #IIa_spec = np.loadtxt(QSettings.IIa_path, delimiter = ',')

    spectrum_prelim = QUtility.read_spec(filename)
    
    if spectrum_prelim[:,1][-1] == 0:
        spectrum_new = spectrum_prelim[:-1]
        spectrum_prelim = spectrum_new
        print('removing rogue value')
        
    if spectrum_prelim[:,1][0] == 0:
        spectrum_new = spectrum_prelim[1:]
        spectrum_prelim = spectrum_new
        print('removing rogue value')
    
    
    spectrum_prelim = QUtility.spectrum_slice(spectrum_prelim, 675, 4000)

    min_wav = np.min(spectrum_prelim[:,0])
    max_wav = np.max(spectrum_prelim[:,0])
    
    min_range = (1000, 2803)

    if (min_wav > min_range[0] or max_wav < min_range[1]):
        raise ValueError('Spectrum does not include the minimum required wavenumber range: {} to {}. Only {} to {} was provided'.format(min_range[0], min_range[1], min_wav, max_wav))


    dia_region = QUtility.spectrum_slice(spectrum_prelim, 1900, 2250)
    dia_region_avg = np.average(dia_region[:,1])
    
    print('dia_region_avg: {}'.format(dia_region_avg))


    N_region = QUtility.spectrum_slice(spectrum_prelim, 1000, 1400)
    N_region_avg = np.average(N_region[:,1])
    
    print('N_region_avg: {}'.format(N_region_avg))

    saturated = 2.5
    if (dia_region_avg > saturated or N_region_avg > saturated):
        warn.append('spectrum may be saturated')

    
    print('baseline removal...')

    min_int = np.argmin(spectrum_prelim[:,1])
    #bl= -spectrum_prelim[-1][1]
    bl= -spectrum_prelim[min_int][1]
   
    spectrum_abs = spectrum_prelim[:,1] + bl              
    spectrum = np.column_stack((spectrum_prelim[:,0], spectrum_abs))
      
    mindiff = (QUtility.closest(1992.0, spectrum[:,0]))          # return wavenum closest to 1992
    row = np.where(spectrum == mindiff)[0][0]
    factor = 12.3/abs((spectrum[row,1]))                # calculate scaling factor    
    spectrum[:,1] *= factor

    spec_corr = spectrum
          
###############################################################################
################ FITTING AND SUBTRACTING TYPE IIa SPECTRUM #################### 
                                                  
    #print('final fit:')                                                    
    #two_phonon_left = QUtility.spectrum_slice(spectrum, 1500,2312)
    #two_phonon_right = QUtility.spectrum_slice(spectrum, 2391, 3000)
    #two_phonon_extra = QUtility.spectrum_slice(spectrum, 3800, 4000)
    #two_phonon = np.vstack((two_phonon_left, two_phonon_right, two_phonon_extra))

    #two_phonon_wav = np.arange(two_phonon[:,0][0], two_phonon[:,0][-1], 0.1)
    #two_phonon_ip = QUtility.inter(spectrum, two_phonon_wav, inttype='linear')          # interpolate slice of spectrum used for fitting    

    #IIa_spec_ip = QUtility.inter(IIa_spec, two_phonon_wav, inttype='linear')            # interpolate relevant area of type IIa spectrum
    #IIa_spec_ip_new = QUtility.inter(IIa_spec, spectrum[:,0:-1], inttype='linear')
    
    #IIa_args = (two_phonon_wav, two_phonon_ip, IIa_spec_ip)     # arguments needed for IIa_fit
    #IIa_x0 = [(1, 0, 0)]                                    #initial guess of parameters (normf, poly1, poly2)
    #IIa_bounds = [(0.0, None),(None, None),(None, None)]         #(min, max)-pairs for parameters 
    #IIa_res = op.minimize(QUtility.IIa, args=IIa_args, x0=IIa_x0, method='L-BFGS-B', bounds=IIa_bounds)
    #print(IIa_res)

    #if IIa_res.success == False:
    #    warn.append('baseline problem:' + str(IIa_res.message))
    
    #fit_IIa = QUtility.IIa_fit(IIa_res.x, spectrum[:,0].reshape(len(spectrum[:,0]),1), spectrum[:,1].reshape(len(spectrum[:,1]),1)) 

    #abs_temp = fit_IIa - IIa_spec_ip_new
    #spec_corr = np.column_stack((spectrum[:,0] , abs_temp))

################################################################################
########################### DETERMINING DIAMOND TYPE ###########################

    N_spec = QUtility.spectrum_slice(spec_corr, 1000, 1400)
    N_avg = np.average(N_spec[:,1])
    
    print('N_avg (after corr): {}'.format(N_avg))

    print('Testing for Boron')
    H_2802 = QUtility.height(2802, spec_corr)
    H_2665 = QUtility.height(2665, spec_corr)
    print('H_2802: {}'.format(H_2802))
    print('H_2665: {}'.format(H_2665))

    if abs(H_2802/H_2665) > 1.2:
        diamondtype = 'IIb'
        warn.append('Handle with care. B detection not fully tested.')

    elif N_avg <= 0.2:
        diamondtype = 'IIa'

    elif N_avg >= 0.2:
        print('N detected.')
        diamondtype = 'I'
        H_1282 = QUtility.height(1282, spec_corr)
        H_1130 = QUtility.height(1130, spec_corr)
        H_1344 = QUtility.height(1344, spec_corr)
        H_1170 = QUtility.height(1170, spec_corr)
        H_1399 = QUtility.height(1399, spec_corr)
        
        #if H_1344-H_1399 >=


        if H_1130 > H_1282:
            print('1130 is higher than 1282.')
        
        print('H_1282: {}'.format(H_1282))
        print('H_1130: {}'.format(H_1130))
        print('H_1344: {}'.format(H_1344))
        print('H_1170: {}'.format(H_1170))

        
        #H_1392 = QUtility.height(1392, spec_corr)

        if H_1130/H_1282 >= 2:
            warn.append('C may be present')
            if H_1344/H_1282 >= 1.8:
                warn.append('C probably present')
                diamondtype += 'b'
        elif H_1344/H_1282 < 1:
            diamondtype += 'a'
            if H_1170/H_1282 < 0.5:
                diamondtype += 'A'
            elif H_1170/H_1282 > 1.5:
                diamondtype += 'B'
            else:
                diamondtype += 'AB'

    
    if savecorrected == True:
        print('saving spectrum after IIa subtraction...')
        if outpath != '':
            output_path = outpath+ '/c' + filename.split('/')[-1]
        else:
            output_path = filename.split('/')[:-1] + '/c' + filename.split('/')[-1]
    
        np.savetxt(output_path, spec_corr, delimiter=',')

    warnstr = ''
    for message in warn:
        warnstr += (message + ', ')
    
    return diamondtype, warnstr #spec_corr, diamondtype, warnstr
