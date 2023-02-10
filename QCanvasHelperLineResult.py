from QCanvasHelperBase import *
import numpy as np
from QSettings import *
from QUtility import *

class QCanvasHelperLineResult(QCanvasHelperBase):

    def display_current(self):
        self.clear_plot()

        points = []
        for item in self.data['name']:
            points.append(float(item.split()[-1][-8:-4]))

        fig = self.canv.figure

        sp1 = fig.add_subplot(331)
        sp1.text(0, 0.5, self.title, bbox={'facecolor':'white', 'pad':10})
        sp1.axis('off')

        sp2 = fig.add_subplot(332)
        sp2.plot(self.data['[NB]']/79.4, self.data['p_area_ana'], 'k.')
        sp2.plot((0, 100), (0, 6400), 'k-')
        sp2.set(xlim=(0, 10), ylim=(0, 640),
                xlabel='$\mathregular{\mu_B}$',
                ylabel="I(B') $\mathregular{(cm^{-2})}$")

        sp3 = fig.add_subplot(333)
        sp3.plot(points, self.data['H_area_ana'], 'k.')
        sp3.set(ylim=(0, None),
                ylabel='I(3107) $\mathregular{(cm^{-2})}$',
                xticklabels=[])

        sp4 = fig.add_subplot(334)
        sp4.plot(points, self.data['[NC]'], '.', label='$\mathregular{[N_C]}$')
        sp4.plot(points, self.data['[NA]'], '.', label='$\mathregular{[N_A]}$')
        sp4.plot(points, self.data['[NB]'], '.', label='$\mathregular{[N_B]}$')
        sp4.plot(points, self.data['[NT]'], '.', label='$\mathregular{[N_t]}$')
        sp4.set(ylim=(0, None),
                ylabel='concentration (ppm)',
                xticklabels=[])
        sp4.legend(loc='best')

        sp5 = fig.add_subplot(335)
        sp5.plot(points, (self.data['[NB]']/(self.data['[NA]']+self.data['[NB]'])), 'k.')
        sp5.set(ylim=(0, 1),
                ylabel='$\mathregular{[N_B]/[N_T]}$',
                xticklabels=[])

        sp6 = fig.add_subplot(336)
        sp6.plot(points, self.data['T'], 'k.')
        sp6.set(ylim=(1050, 1350),
                ylabel='$\mathregular{T_N (^{\circ}C)}$',
                xticklabels=[])

        sp7 = fig.add_subplot(337)
        sp7.plot(points, self.data['p_area_ana'], 'k.')
        sp7.set(ylim=(0, None),
                xlabel='#', ylabel="I(B') $\mathregular{(cm^{-2})}$")
        
        sp8 = fig.add_subplot(338)
        p0 = (self.data['[NB]']/79.4)*64
        deg = (1-(self.data['p_area_ana']/p0))
        sp8.plot(points, deg, 'k.')
        sp8.set(ylim=(0, 1),
                xlabel='#', ylabel="$\mathregular{1-(I(B')/I(B')_0)}$")
        
        sp9 = fig.add_subplot(339)
        lnstuff = np.log(np.log(p0/self.data['p_area_ana'])/(1000*1e6*365*24*60*60))
        Tp = ((88446)/(19.687-lnstuff)) -273
        sp9.plot(points, Tp, 'k.')
        sp9.set(ylim=(1050, 1350),
                xlabel='#', ylabel='$\mathregular{T_P (^{\circ}C)}$')

        fig.tight_layout(pad=0.7, w_pad=0, h_pad=0)
        self.canv.figure.suptitle('')
        self.canv.draw()

    def add_line_data(self, resfile):
        self.data = np.loadtxt(resfile, dtype=QUtility.results_dtype, delimiter=',', skiprows=2, usecols=(np.arange(len(QUtility.results_dtype))))
        self.title = resfile.split('/')[-1]
        self.maxidx = 1