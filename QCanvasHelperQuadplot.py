from QCanvasHelperBase import *
from QUtility import *
from QSettings import *
import numpy as np
from scipy.stats import gaussian_kde


class QCanvasHelperQuadplot(QCanvasHelperBase):
    def display_current(self):

        plotkwargs = {'s':30, 'cmap':cm.Greys, 'edgecolor':'k', 'linewidth':0.1}

        self.clear_plot()

        data_temp = self.data
        mask=np.where(data_temp['p_I']/(data_temp['p_HWHM_l']+data_temp['p_HWHM_r'])>=0.05) #0.05
        data = data_temp[mask]

        qp1_x = np.arange(0, np.max(data['b'])+1)
        qp1_y = qp1_x * 64.
        qp2_x = qp3_x = qp4_x = np.arange(1358, 1378)
        qp2_y = qp2_x * 123.3 - 1678*1e2
        qp3_y = -0.987 * qp3_x + 1342
        qp4_y = 0.844 * qp4_x - 1142

        fig = self.canv.figure
        fig.suptitle(self.title)

        p_sym = data['p_x0']-data['avg']
        p_area = data['p_area_ana']
        p_pos = data['p_x0']
        mu_b = data['b']
        p_width = data['p_HWHM_l']+data['p_HWHM_r']

        Woods_idx, Woods_z = QUtility.make_Kde(mu_b, p_area)
        pos_area_idx, pos_area_z = QUtility.make_Kde(p_pos, p_area)
        pos_sym_idx, pos_sym_z = QUtility.make_Kde(p_pos, p_sym)
        pos_width_idx, pos_width_z = QUtility.make_Kde(p_pos, p_width)

        sp1 = fig.add_subplot(1,4,1)
        #sp1.plot(data['b'], data['p_area_ana'], 'ko')
        sp1.scatter(mu_b[Woods_idx], p_area[Woods_idx], c=Woods_z[Woods_idx], **plotkwargs)
      
        sp1.plot(qp1_x, qp1_y, 'k--')
        sp1.set(xlim=(0,None), ylim=(0,None),
                xlabel='$\mathregular{\mu_B}$',
                ylabel="I(B') ($\mathregular{cm^{-2}}$)")
        
        sp2 = fig.add_subplot(1,4,2)
        #sp2.plot(data['p_x0'], data['p_area_ana'], 'ko')
        sp2.scatter(p_pos[pos_area_idx], p_area[pos_area_idx], c=pos_area_z[pos_area_idx], **plotkwargs)

        sp2.plot(qp2_x, qp2_y, 'k--')
        sp2.set(xlim=(1358, 1378), xlabel='$\mathregular{x_0 (cm^{-1})}$',
                ylabel="I(B') ($\mathregular{cm^{-2}}$)")
        
        sp3 = fig.add_subplot(1,4,3)
        #sp3.plot(data['p_x0'], data['p_x0']-data['avg'], 'ko')
        sp3.scatter(p_pos[pos_sym_idx], p_sym[pos_sym_idx], c=pos_sym_z[pos_sym_idx], **plotkwargs)

        sp3.plot(qp3_x, qp3_y, 'k--')
        sp3.set(xlim=(1358, 1378), xlabel='$\mathregular{x_0 (cm^{-1})}$',
                ylabel='symmetry (cm$^{-1}$)')
        
        sp4 = fig.add_subplot(1,4,4)
        #sp4.plot(data['p_x0'], data['p_HWHM_l']+data['p_HWHM_r'],'ko')
        sp4.scatter(p_pos[pos_width_idx], p_width[pos_width_idx], c=pos_width_z[pos_width_idx], **plotkwargs)
        sp4.plot(qp4_x, qp4_y, 'k--')
        sp4.set(xlim=(1358, 1378), xlabel='$\mathregular{x_0 (cm^{-1})}$',
                ylabel='FWHM (cm$^{-1}$)')
        
        #fig.tight_layout()

        self.canv.draw()

    def add_map_data(self, resfile):
        tmp_data = np.loadtxt(resfile, dtype=QUtility.results_dtype, delimiter=',', skiprows=2)
        mask=np.where(tmp_data['p_I'] / (tmp_data['p_HWHM_l'] + tmp_data['p_HWHM_r'])>=0.05)
        self.data=tmp_data[mask]
        self.title = resfile.split('/')[-1]
        self.maxidx = 1