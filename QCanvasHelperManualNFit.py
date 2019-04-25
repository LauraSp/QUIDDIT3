from QCanvasHelperBase import *
from QSettings import *
from QUtility import *

import numpy as np
import scipy.optimize as op
from matplotlib.widgets import Slider
from matplotlib.widgets import Button as mplButton

class QCanvasHelperManualNFit(QCanvasHelperBase):
    def display_current(self):
        self.clear_plot()

        fig = self.canv.figure
        fig.suptitle(self.get_spec_name(self.current))
        spectrum = self.read_spectrum(self.current)

        fit_area = QUtility.spectrum_slice(spectrum, 1001, 1399)
        wav_new = np.arange(fit_area[0][0], fit_area[-1][0], 0.01)
        self.fit_area_inter = QUtility.inter(fit_area, wav_new)
        self.fit_area_inter = self.fit_area_inter.flatten()

        std = QSettings.std
        C = np.column_stack((std[:,0], std[:,1]))
        A = np.column_stack((std[:,0], std[:,2]))    #generate C, A, X, B and D std
        X = np.column_stack((std[:,0], std[:,3]))    #spectra from CAXBD file
        B = np.column_stack((std[:,0], std[:,4]))   
        D = np.column_stack((std[:,0], std[:,5]))

        C_new = QUtility.inter(C, wav_new)   
        A_new = QUtility.inter(A, wav_new)
        X_new = QUtility.inter(X, wav_new)                     # interpolate C, A, X, B and D spectra
        B_new = QUtility.inter(B, wav_new)
        D_new = QUtility.inter(D, wav_new)
        self.all_comp = np.column_stack((C_new, A_new, X_new, B_new, D_new))


        sp = fig.add_subplot(111)
        sp.invert_xaxis()

        N_comp = np.array((QSettings.N_comp))
        if N_comp[-1] == 1:
            polyx0 = fit_area[-1,1]    
            if polyx0 >0:        
                polybounds = (0., polyx0)    
            else:
                polybounds = (polyx0, 0.)
        else:
            polyx0 = 0
            polybounds = (0., 0.)
            
        x0 = [i for i,j in zip((.5, .5, .1, .5, 0., -polyx0), N_comp) if j==1]
        bounds =  [i for i,j in zip([(0.,None),(0.,None),(0.,None),(0.,None),(0., None), polybounds], N_comp) if j==1]
        mask = np.where(N_comp[:-1]==1)[0]
        fit_args = self.all_comp[:, mask]
            
        fit_res = op.minimize(QUtility.CAXBD_err, x0=x0, args=(fit_args, self.fit_area_inter), method='SLSQP', bounds=bounds)
        fit = QUtility.CAXBD(fit_res.x, fit_args)

        fig.subplots_adjust(left=0.25, bottom=0.4)


        sp.plot(fit_area[:,0], fit_area[:,1], 'k.', label='data')
        self.l, =sp.plot(wav_new, fit, 'g-')
        self.l2, = sp.plot(wav_new, (fit - self.fit_area_inter),'r-')
        sp.axhline(y=0, ls='--', color='k')

        axcolor = 'lightgoldenrodyellow'
            
        ax_C = fig.add_axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
        ax_A = fig.add_axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
        ax_X = fig.add_axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
        ax_B = fig.add_axes([0.25, 0.25, 0.65, 0.03], facecolor=axcolor)
        ax_D = fig.add_axes([0.25, 0.3, 0.65, 0.03], facecolor=axcolor)
        ax_poly1 = fig.add_axes([0.25, 0.35, 0.65, 0.03], facecolor=axcolor)
        
        axes = (ax_C, ax_A, ax_X, ax_B, ax_D, ax_poly1)
        self.sliders = []
        limits = {'C':(0,10), 'A':(0,20), 'X':(0,2), 'B':(0,3), 'D':(0,3), 'const.':(-1,1)}           
                
        i = 0       
        for yesno, axis, name in zip(N_comp, axes, limits):
            if name == 'const.':
                slider = Slider(axis, name, fit_res.x[-1]-5, fit_res.x[-1]+5, valinit = fit_res.x[-1], valfmt='%1.1f')
            else:
                if yesno == 1:
                    slider = Slider(axis, name, limits[name][0]*fit_res.x[i], limits[name][1]*fit_res.x[i], valinit=fit_res.x[i])
                    i += 1
                else:
                    slider = Slider(axis, name, 0, 5, valinit=0, valfmt='%1.1f')
            slider.on_changed(self.widget_update)
            self.sliders.append(slider)
            
        C = self.sliders[0].val
        A = self.sliders[1].val
        X = self.sliders[2].val
        B = self.sliders[3].val
        D = self.sliders[4].val
            
        N_c = np.round(C * 25, 1)
        N_a = np.round(A * 16.5, 1)
        N_b = np.round(B * 79.4, 1)
        N_t = N_a + N_b + N_c
        IaB = np.round(N_b/N_t)

        T = np.round(QUtility.Temp_N(self.age.get()*1e6*365*24*60*60, N_t, N_b/N_t))
        self.fig_text = fig.text(0.01, 0.75,
                            '[NC]: {}\n[NA]: {}\n[NB]: {}\n%B.: {}\nT: {}C \nmax D: {}'.format(N_c, N_a, N_b, IaB, T, np.round(B*0.365, 2)))             

        resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])

        self.reset_button = mplButton(resetax, 'Reset', color=axcolor, hovercolor='0.975')
        self.reset_button.on_clicked( lambda event, arg=self.sliders: self.widget_reset(event, arg))

        self.canv.draw()


    def read_spectrum(self, idx):
        """read current spectrum
        """
        filename = self.specfiles[idx]
        if filename.lower().endswith('.csv'):
            spec = np.loadtxt(filename, delimiter=',')
            return spec
        else:
            raise Exception("Unknown identifier " + filename + " in read_spectrum")

    def get_spec_name(self, idx):
        filename = self.specfiles[idx]
        if filename.lower().endswith('.csv'):
            return filename.split("/")[-1].split(".")[0]
        else:
            raise Exception("Unknown identifier " + filename + " in get_spec_name")

    def add_data(self, specfiles, age):
        self.specfiles = specfiles
        self.age = age
        self.maxidx = len(self.specfiles)
        self.__std = QSettings.std

    def widget_reset(self, event, sliders):
        for slider in sliders:
            slider.reset()

    def widget_update(self, val):
        C = self.sliders[0].val
        A = self.sliders[1].val
        X = self.sliders[2].val
        B = self.sliders[3].val
        D = self.sliders[4].val
        poly1 = self.sliders[5].val

        factors = np.array([C, A, X, B, D, poly1])
        
        N_c = np.round(C * 25, 1)
        N_a = np.round(A * 16.5, 1)
        N_b = np.round(B * 79.4, 1)
        N_t = N_a + N_b + N_c
        IaB = np.round(N_b/N_t)
        T = np.round(QUtility.Temp_N(self.age.get()*1e6*365*24*60*60, N_t, N_b/N_t))
        
        self.l.set_ydata(QUtility.CAXBD(factors, self.all_comp))
        self.l2.set_ydata(QUtility.CAXBD(factors, self.all_comp)-self.fit_area_inter)
        #self.fig_text.
        self.fig_text.set(text='[NC]: {}\n[NA]: {}\n[NB]: {}\n%B.: {}\nT: {}C \nmax D: {}'.format(N_c, N_a, N_b, IaB, T, np.round(B*0.365, 2)))
