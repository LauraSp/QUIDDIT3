import numpy as np

class QDPTconverter:
    def __init__(self, dptconvinp):
        self.dptfile = dptconvinp.dpt_file
        self.targetdir =dptconvinp.target_dir

    def convert(self):

        data = np.loadtxt(self.dptfile, delimiter=',')

        wav = data[:, 0]
        spectra = data[:, 1:]


        i = 1
        for column in spectra.T:
            spectrum = np.column_stack((wav, column))
            np.savetxt((self.targetdir + '\\spectrum {:05d}.CSV'.format(i)), spectrum, delimiter=',' )
            i += 1


        #for column in range(1, no_of_spectra):
        #    abs = data[:, column]
        #    spectrum = np.column_stack((wav, row))
        #    np.savetxt((self.targetdir + 'spectrum {:05d}'.format(i)), spectrum, delimiter=',' )