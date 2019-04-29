import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

STDRELIEF = tk.FLAT
STDBG = '#ececec'

class QTclWindowBasics:
    """basic methods for popup and main windows
    """

    def makelabel(self, parent=None, lrow=0, lcol=0, cspan=1, rspan=1, caption='', sticky=tk.NE, **options):
        p = self if parent == None else parent

        label = tk.Label(p, text=caption)
        label.grid(row=lrow, column=lcol, columnspan=cspan, rowspan=rspan, sticky=sticky)
        return label

    def makeimagelabel(self, parent=None, lrow=0, lcol=0, cspan=1, rspan=1, img=None, caption=None, **options):
        p = self if parent == None else parent
        if caption != None:
            label = tk.Label(p, text=caption, image=img, compound = tk.BOTTOM)
        else:
            label = tk.Label(p, image=img)

        label.grid(row=lrow, column=lcol, columnspan=cspan, rowspan=rspan)

        return label

    def maketext(self, parent=None, lcol=0, lrow=0, erow=0, ecol=1, cspan=1, rspan=1, caption='', width=None, padx=(0,0), pady=(0,0), **options):
        """create a multiple single line text widget with a label/caption in another column
        """
        p = self if parent == None else parent
        tk.Label(p, text=caption).grid(row=lrow, column=lcol, columnspan=cspan, rowspan=rspan, sticky=tk.N + tk.E)
        entry = tk.Text(p, **options)
        if width:
            entry.config(width=width)
    
        entry.grid(row=erow, column=ecol, sticky=tk.W, padx=padx, pady=pady)
        return entry

    def makeentry(self, parent=None, lcol=0, lrow=0, erow=0, ecol=1, caption='', width=None, **options):
        """create a single line text entry widget with a label"""
        p = self if parent == None else parent
        tk.Label(p, text=caption).grid(row=lrow, column=lcol, sticky=tk.E)
        entry = tk.Entry(p, relief=STDRELIEF, **options)
        if width:
            entry.config(width=width)
    
        entry.grid(row=erow, column=ecol, sticky=tk.W)
        return entry

    def make_entrypair(self, parent=None, lrow=0, lcol=0, e1row=0, e1col=1, e2row=0, e2col=2, caption='', var1=None, var2=None, padx=(2,2), pady=(2,2), ewidth=None, **options):
        """Create two single line text entry widgets with a label
        """
        p = self if parent == None else parent

        l = self.makelabel(p, lrow=lrow, lcol=lcol, caption=caption, sticky=tk.E, padx=(padx[0],0), pady=pady)

        e1 = tk.Entry(p, relief=STDRELIEF, textvariable=var1, **options)
        e2 = tk.Entry(p, relief=STDRELIEF, textvariable=var2, **options)
        if ewidth:
            e1.config(width=ewidth)
            e2.config(width=ewidth)

        e1.grid(row=e1row, column=e1col, sticky=tk.EW, padx=(2,2), pady=pady)
        e2.grid(row=e2row, column=e2col, sticky=tk.EW, padx=(2,padx[1]), pady=pady)

        return e1, e2

    def make_double_entrypair(self, parent=None, lrow=0, lcol=0, e1row=0, e1col=1, e2row=0, e2col=2, caption='', var1=None, var2=None, padx=(2,2), pady=(2,2), ewidth=None, **options):
        """Create two single line text entry widgets with a label
        """
        p = self if parent == None else parent

        l = self.makelabel(p, lrow=lrow, lcol=lcol, caption=caption, sticky=tk.E, padx=(padx[0],0), pady=pady)

        e1 = ValidateDoubleEntry(p, relief=STDRELIEF, textvariable=var1, **options)
        e2 = ValidateDoubleEntry(p, relief=STDRELIEF, textvariable=var2, **options)

        if ewidth:
            e1.config(width=ewidth)
            e2.config(width=ewidth)

        e1.grid(row=e1row, column=e1col, sticky=tk.EW, padx=(2,2), pady=pady)
        e2.grid(row=e2row, column=e2col, sticky=tk.EW, padx=(2,padx[1]), pady=pady)

        return e1, e2

    def make_double_entry(self, parent=None, lcol=0, lrow=0, erow=0, ecol=1, caption='', width=None, padx=(2,2), pady=(2,2), **options):
        """create a single line text for a number entry widget with a label
        """
        p = self if parent == None else parent
        tk.Label(p, text=caption).grid(row=lrow, column=lcol, sticky=tk.E)
        entry = ValidateDoubleEntry(p, relief=STDRELIEF, **options)
        if width:
            entry.config(width=width)
    
        entry.grid(row=erow, column=ecol, sticky=tk.W, padx=padx, pady=pady)
        return entry

    def make_int_entry(self, parent=None, lcol=0, lrow=0, erow=0, ecol=1, caption='', width=None, **options):
        """create a single line text for number entry widget with a label
        """
        p = self if parent == None else parent
        tk.Label(p, text=caption).grid(row=lrow, column=lcol, sticky=tk.E)
        entry = ValidateIntegerEntry(p, relief=STDRELIEF, **options)
        if width:
            entry.config(width=width)
    
        entry.grid(row=erow, column=ecol, sticky=tk.W)
        return entry

    def set_entry_text(self, entry, text):
        """Set text in text entry to a given text"""
        entry.delete(0, tk.END)
        entry.insert(tk.END, text)

    def makecheck(self, parent=None, ecol=0, erow=0, rspan=1, cspan=1, caption='', sticky=tk.W, padx=(0,0), pady=(0,0), **options):
        """create a checkbox with a label"""
        p = self if parent == None else parent
        cb = tk.Checkbutton(p, text=caption, **options)
        cb.grid(row=erow, column=ecol, rowspan=rspan, columnspan=cspan, sticky=sticky, padx=padx, pady=pady)
        return cb

    def makeradio(self, parent=None, ecol=0, erow=0, cspan=1, rspan=2, caption='RadioButton',
                    width=None, sticky=tk.W, padx=(0,0), pady=(0,0), variable=None, value=0):
        p = self if parent == None else parent
        rb = tk.Radiobutton(p, text=caption, variable=variable, value=value)
        rb.grid(row=erow, column=ecol, padx=padx, pady=pady, sticky=sticky)
        return rb


    def makebutton(self, parent=None, erow=0, ecol=0, cspan=1, rspan=1, caption='Button', 
                   width=None, cmd=None, sticky=tk.W, padx=(0,0), pady=(0,0),**options):
        """create a button widget"""
        p = self if parent == None else parent
        bu = tk.Button(p,
                        text=caption,
                        width=width,
                        command=cmd,
                        **options)
        
        bu.grid(row=erow, 
            column=ecol, 
            columnspan=cspan, 
            rowspan=rspan, 
            sticky=sticky,
            padx = padx,
            pady = pady)

        return bu

    def makecanvas(self, parent=None, erow=0, ecol=0, rspan=1, cspan=1, sticky=tk.NSEW, **options):
        """create a canvas widget"""
        p = self if parent == None else parent
        ca = tk.Canvas(p, **options)
        ca.grid(row=erow, column=ecol,
                columnspan=cspan, rowspan=rspan, sticky=sticky)

        return ca
    
    def make_mplcanvas(self, parent=None, fig=None, erow=0, ecol=0, rspan=1, cspan=1, sticky=tk.NSEW, **options):
        p = self if parent == None else parent
        canvas = FigureCanvasTkAgg(fig, master=p, **options)
        mpl_canvas = canvas.get_tk_widget()
        mpl_canvas.grid(row=erow, column=ecol, columnspan=cspan, rowspan=rspan, sticky=sticky)
        
        return canvas

    def makelist(self, parent=None, lcol=0, lrow=0, erow=0, ecol=1, caption='', width=None,
                 scrollvert=True, scrollhor=False,
                 **options):
        """create a list widget in the current window
        """
        
        p = self if parent == None else parent
        tk.Label(p, text=caption).grid(row=lrow, column=lcol, sticky=tk.N + tk.E)
        
        if scrollvert == True:
            yScroll = tk.Scrollbar(p, orient=tk.VERTICAL)
            yScroll.grid(row=erow, column=ecol+1, sticky=tk.N+tk.S)
            
        if scrollhor == True:
            xScroll = tk.Scrollbar(p, orient=tk.HORIZONTAL)
            xScroll.grid(row=erow+1, column=ecol, sticky=tk.E+tk.W)

        lst = tk.Listbox(p, **options)
        lst.grid(row=erow, column=ecol)
        
        if scrollvert == True:
            lst.config(yscrollcommand=yScroll.set)
            yScroll['command'] = lst.yview

        if scrollhor == True:
            lst.config(xscrollcommand=xScroll.set)
            xScroll['command'] = lst.xview

        if width:
            lst.config(width=width)

        return lst
    def make_frame(self, parent=None, ecol=0, erow=0, cspan=2, rspan=1, sticky=tk.NSEW, relief=tk.GROOVE, padx=(0,0), pady=(0,0), **options):
        p = self if parent == None else parent
        fr = tk.Frame(p, relief=relief, **options)
        fr.grid(row=erow, column=ecol,
                columnspan=cspan, rowspan=rspan, sticky=sticky,
                padx=padx, pady=pady)
        return fr

    def make_label_frame(self, parent=None, caption="Frame", lcol=0, lrow=0, cspan=1, rspan=1,relief=tk.GROOVE, sticky=tk.NSEW, padx=(0,0), pady=(0,0), **options):
        p = self if parent == None else parent
        lf = tk.LabelFrame(p, relief=relief, text=caption, **options)
        lf.grid(row=lrow, column=lcol,
                columnspan=cspan, rowspan=rspan, sticky=sticky,
                padx=padx, pady=pady)
                
        return lf

    def getvar(self, defval):
        """gets a new tkinter variable to be used for binding to entry widgets
        """
        t = type(defval)

        if t == str:
            answ = tk.StringVar()
            answ.set(defval)
        elif t == int:
            answ = tk.IntVar()
            answ.set(defval)
        elif t == float:
            answ = tk.DoubleVar()
            answ.set(defval)
        else:
            answ = tk.StringVar()

        return answ


class ValidateDoubleEntry():
    """Special entry widget for editing of double numbers
    """
    def __init__(self, parent, **options):
        validate_number_cmd = parent.register(self.validate_number)
        self.entry = tk.Entry(parent,
                               validate='all',
                               validatecommand=(validate_number_cmd, '%d', '%i', '%S'),
                               **options)
    
    def config(self, **options):
        self.entry.config(**options)

    def grid(self, **options):
        self.entry.grid(**options)

    def validate_number(self, d, i, s):
        if s == '':
            return True

        if s.isdigit() or s=='.' or (i=='0' and s=='-'):
            return True

        return False
    
    def delete(self, start, end):
        self.entry.delete(start, end)

    def bind(self, event, command):
        self.entry.bind(event, command)


class ValidateIntegerEntry():
    """special entry type widget for editing integer values
    """
    def __init__(self, parent, **options):
        validate_number_cmd = parent.register(self.validate_number)
        self.entry = tk.Entry(parent,
                               validate='all',
                               validatecommand=(validate_number_cmd, '%d', '%i', '%S'),
                               **options)
    
    def config(self, **options):
        self.entry.config(**options)

    def grid(self, **options):
        self.entry.grid(**options)

    def validate_number(self, d, i, s):
        if s == '':
            return True

        if s.isdigit() or (i=='0' and s=='-'):
            return True

        return False
