import sys
import numpy as np
import spectral.io.envi as envi
from QTclPopupWindow import *

class QENVIconverter:
    def __init__(self, enviconvinp):
        self.hdr = enviconvinp.hdr
        self.dat = enviconvinp.dat
        self.targetdir = enviconvinp.targetdir

    def convert(self):
        with open(self.hdr, 'r+') as hdr:
            assert(any('byte order' in line for line in hdr)), "Byte order information missing from header file.\nDepending on what operating system the header file was CREATED on,\nyou can manually insert\n'byte order = 0' (Windows, Linux) or 'byte order = 1' (MacOS)\ninto the header file:\n{}".format(self.hdr)
            #bo_found = any('byte order' in line for line in hdr)
            #if not bo_found:
            #    self.add_byteorder()
                
        #try:
        envi_img = envi.open(self.hdr, self.dat)
        #except envi.MissingEnviHeaderParameter("byte order")

        img_data = envi_img.load()
        xspacing = np.asarray(envi.read_envi_header(self.hdr)['pixel size'], dtype=float)[0]
        yspacing = np.asarray(envi.read_envi_header(self.hdr)['pixel size'], dtype=float)[1]
        wavenum = np.asarray(envi.read_envi_header(self.hdr)['wavelength'], dtype=float)
        
        rows = np.shape(img_data)[0]
        columns = np.shape(img_data)[1]
            
        for i in range(rows):
            for j in range(columns): 
                spectrum = np.column_stack((wavenum, img_data[i,j,:].flatten()))
                #self.print_message(self.message, 'Saving spectrum {} of {}.'.format(loading.progress['value']+1, rows*columns))
                x = i * xspacing
                y = j * yspacing
                fname = 'X{} Y{}.CSV'.format(str(np.round(x, 6)), str(np.round(y, 6)))
                np.savetxt((self.targetdir + '/' + fname), spectrum, delimiter=',')

    #def add_byteorder(self):
    #    endianness = sys.byteorder
    #    curr_bo = 0 if endianness is 'little' else 1
    #    bo_window = QAskByteOrderWindow(self, 'Error. Byte order not found.', curr_bo)
    #    if bo_window.dresult == 'OK':
    #        bo = bo_window.byte_order
    #        hdr = open(self.hdr, 'a+')
    #        hdr.write('byte order = {}\n'.format(bo))
    #        hdr.close()

class QAskByteOrderWindow(QTclPopupWindow):
    def __init__(self, parent, title, byte_order, is_modal=True):
        self.byte_order = byte_order
        self.dresult = "NONE"
        super().__init__(parent, title, is_modal)

    def loaded(self):
        pass

    def make_gui(self, title):
        self.setwintitle(title)

        row = 0
        self.makelabel(lcol=0, lrow=row, padx=(5,5), pady=(5,5), cspan=2, caption='Were the ENVI files CREATED on Windows or MacOS/Linux?')

        row += 1
        self.makeradio(caption='Windows', variable=self.byte_order, value=0, erow=row, ecol=0, padx=(5,5), pady=(5,5))
        self.makeradio(caption='MacOS/Linux', variable=self.byte_order, value=1, erow=row, ecol=1, padx=(5,5), pady=(5,5))

        self.add_std_buttons(okcol=1, cancelcol=0)