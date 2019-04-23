from QCanvasHelperBase import *
from QUtility import *
from QSettings import *


class QCanvasHelperQuadplot(QCanvasHelperBase):
    def display_current(self):
        self.clear_plot()

        data = self.data

        qp1_x = np.arange(0, np.max(data['b'])+1)
        qp1_y = qp1_x * 64.
        qp2_x = qp3_x = qp4_x = np.arange(1358, 1378)
        qp2_y = qp2_x * 123.3 - 1678*1e2
        qp3_y = -0.987 * qp3_x + 1342
        qp4_y = 0.844 * qp4_x - 1142

        fig = self.canv.figure
        fig.suptitle(self.title)

        sp1 = fig.add_subplot(1,4,1)
        sp1.plot(data['b'], data['p_area_ana'], 'ko')        
        sp1.plot(qp1_x, qp1_y, 'k--')
        sp1.set(xlim=(0,None), ylim=(0,None),
                xlabel='$\mathregular{\mu_B}$',
                ylabel="I(B') ($\mathregular{cm^{-2}}$)")
        
        sp2 = fig.add_subplot(1,4,2)
        sp2.plot(data['p_x0'], data['p_area_ana'], 'ko')
        sp2.plot(qp2_x, qp2_y, 'k--')
        sp2.set(xlim=(1358, 1378), xlabel='$\mathregular{x_0 (cm^{-1})}$',
                ylabel="I(B') ($\mathregular{cm^{-2}}$)")
        
        sp3 = fig.add_subplot(1,4,3)
        sp3.plot(data['p_x0'], data['p_x0']-data['avg'], 'ko')
        sp3.plot(qp3_x, qp3_y, 'k--')
        sp3.set(xlim=(1358, 1378), xlabel='$\mathregular{x_0 (cm^{-1})}$',
                ylabel='symmetry (cm$^{-1}$)')
        
        sp4 = fig.add_subplot(1,4,4)
        sp4.plot(data['p_x0'], data['p_HWHM_l']+data['p_HWHM_r'],'ko')
        sp4.plot(qp4_x, qp4_y, 'k--')
        sp4.set(xlim=(1358, 1378), xlabel='$\mathregular{x_0 (cm^{-1})}$',
                ylabel='FWHM (cm$^{-1}$)')
        
        fig.tight_layout()

        self.canv.draw()

    def add_map_data(self, resfile):
        tmp_data = np.loadtxt(resfile, dtype=QSettings.results_dtype, delimiter=',', skiprows=2)
        mask=np.where(tmp_data['p_I'] / (tmp_data['p_HWHM_l'] + tmp_data['p_HWHM_r'])>=0.05)
        self.data=tmp_data[mask]
        self.title = resfile.split('/')[-1]
        self.maxidx = 1