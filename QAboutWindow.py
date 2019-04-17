from QImpWindowBasics import *
from QSettings import *

class QAboutWindow(QTclPopupWindow):
    """About Window
    """

    def loaded(self):
        pass

    def make_gui(self, title):
        self.setwintitle(title)
        #We have to keep a reference of the image due to a bug in tkinter
        #This way we prevent that garbage collection destroys the image before the window
        #is destroyed
        self.myimg = tk.PhotoImage(file=QSettings.home + '\\QUIDDITlogo.gif')
        self.makeimagelabel(img=self.myimg)

        about_msg = 'version {}\n(Laura Speich, 10/2017)\n\nlaura.speich@bristol.ac.uk\n\n'.format(str(QSettings.version))
        
        self.makelabel(lrow=1, caption=about_msg, sticky=tk.NSEW)
        #self.makebutton(2,0, caption="Dismiss", cmd=self.destroy, sticky=tk.NSEW, height=1, width=6, default='active')
