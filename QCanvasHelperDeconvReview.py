from QCanvasHelperBase import *
from QSettings import *
from QUtility import *
import numpy as np

class QCanvasHelperDeconvReview(QCanvasHelperBase):
    def display_current(self):
        self.clear_plot()
        fig = self.canv.figure
        fig.suptitle(self.get_spec_name(self.current))

        spec = self.read_spectrum(self.current)
        rev = self.rev_data[self.current]

        N_abs_new = QUtility.inter(spec, np.array(QSettings.std[:, 0]))
        c = rev['c']
        a = rev['a']
        x = rev['x']
        b = rev['b']
        d = rev['d']
        const = rev['N_poly']
        N_fit = QUtility.CAXBD(np.array((c, a, x, b, d, const)), QSettings.std[:, 1:])

        NC = np.round(c * 25, 1)
        NA = np.round(a * 16.5, 1)
        NB = np.round(b * 79.4, 1)
        NT = np.sum(np.nan_to_num((NC, NA, NB)))

        p_spec = QUtility.spectrum_slice(spec, 1327, 1420)
        p_wav = p_spec[:, 0]
        p_params = (rev['p_x0'], rev['p_I'], rev['p_HWHM_l'], rev['p_HWHM_r'], rev['p_sigma'],
                    rev['H1405_x0'], rev['H1405_I'], rev['H1405_HWHM_l'], rev['H1405_HWHM_r'], rev['H1405_sigma'],
                    rev['B_x0'], rev['B_I'], rev['B_HWHM_l'], rev['B_HWHM_r'], rev['B_sigma'],
                    rev['psv_c'])

        p_fit = QUtility.ultimatepsv_fit(p_wav, *p_params)
        p_peak_area = np.round(QUtility.peak_area(*p_params[1:5]), 1)

        H_spec = QUtility.spectrum_slice(spec, 3000, 3200)
        H_wav = H_spec[:, 0]
        H_params = (rev['H_pos'], rev['H_I'], rev['H_HWHM_l'], rev['H_HWHM_r'], rev['H_sigma'])
        H_bg_params = (rev['H_bg_a'], rev['H_bg_b'], rev['H_bg_c'], rev['H_bg_d'])
        H_fit = QUtility.pseudovoigt_fit(H_wav, *H_params) + np.polyval(H_bg_params, H_wav)
        H_peak_area = np.round(QUtility.peak_area(*H_params[1:]), 1)


        sp1 = fig.add_subplot(311)
        sp1.axhline(y=0, color='0.7', linestyle='--')
        sp1.plot(spec[:,0], spec[:,1], 'k.', label='data')
        sp1.plot(np.array(QSettings.std[:, 0]),
                        N_fit,
                        'g-', label='fit')
        sp1.plot(np.array(QSettings.std[:, 0]),
                        N_abs_new - N_fit,
                        'r-', label='misfit')
        sp1.set(xlim=(1400, 1000))
        
        #self.print_message(self.message,
        #                   self.selected_items[self.index])
        #self.print_message(self.message,
        #                   '\nNC: {} ppm\nNA: {} ppm\nNB: {} ppm\ntotal: {} ppm'.format(NC, NA, NB, NT))
        #self.print_message(self.message,
        #                   'platelet peak area: {0:.2f} cm-2'.format(p_peak_area))
        #self.print_message(self.message,
        #                   'platelet peak position: {0:.2f} cm-1'.format(rev['p_x0']))
        #self.print_message(self.message,
        #                  '3107 peak area: {0:.2f} cm-2\n'.format(H_peak_area))

        sp2 = fig.add_subplot(312)
        sp2.axhline(y=0, color='0.7', linestyle='--')
        sp2.plot(spec[:,0], spec[:,1], 'k.', label='data')
        sp2.plot(p_wav, p_fit,
                'g-', label='fit')
        sp2.plot(p_wav, p_fit - p_spec[:, 1],
                'r-', label='misfit')
        sp2.set(xlim=(1420, 1327))

        sp3 = fig.add_subplot(313)
        sp3.plot(spec[:,0], spec[:,1], 'k.', label='data')
        sp3.axhline(y=0, color='0.7', linestyle='--')
        sp3.plot(H_wav, H_fit,
                'g-', label='fit')
        sp3.plot(H_wav, H_fit - H_spec[:, 1],
                'r-', label='misfit')
        sp3.set(xlim=(3200, 3000),
                xlabel='wavenumber ($\mathregular{cm^{-1}}$)')
        sp3.legend(loc='best')

        self.canv.draw()

    
    def add_files(self, reviewinput):
        """Add review file and spectra
        """
        rev_file = reviewinput.rev_file
        self.spec_files = reviewinput.spec_files
        self.rev_data = np.loadtxt(rev_file, dtype=QUtility.review_dtype, delimiter=',', skiprows=2) 

        if len(self.rev_data) != len(self.spec_files):
            raise ValueError('The number of spectra ({}) does not match the length of the review file ({}).'.format(len(self.spec_files), len(self.rev_data)))
    
        else:
            self.maxidx = len(self.rev_data)

    def read_spectrum(self, idx):
        """read current spectrum
        """
        filename = self.spec_files[idx]
        if filename.lower().endswith('.csv'):
            spec = np.loadtxt(filename, delimiter=',')
            return spec
        else:
            raise Exception("Unknown identifier " + filename + " in read_spectrum")

    def get_spec_name(self, idx):
        filename = self.spec_files[idx]
        if filename.lower().endswith('.csv'):
            return filename.split("/")[-1].split(".")[0]
        else:
            raise Exception("Unknown identifier " + filename + " in get_spec_name")