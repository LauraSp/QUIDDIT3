from matplotlib.widgets import Slider

class QCanvasHelperBase:
    """class to help with populating the canvas
    """
    def __init__(self, canvas):
        self.canv = canvas
        self.current = 0
        self.maxidx = 0
        self.texts = []
    
    def display_first(self):
        if self.maxidx >= 1:
            self.current = 0
            self.display_current()
        else:
            raise Exception("no spectra files were added before display_first was used")

    def display_last(self):
        if self.maxidx >= 1:
            self.current = self.maxidx
            self.display_current()
        else:
            raise Exception("no data was added before display_first was used")
    

    def display_next(self):
        if self.current < self.maxidx - 1:
            self.current += 1
        else:
            self.current = 0
        
        self.display_current()

    def display_current(self):
        raise NotImplementedError("override me")

    def get_current_histo_data(self):
        raise NotImplementedError("override me")

    def display_previous(self):
        if self.current > 0:
            self.current -= 1
        else:
            self.current = self.maxidx - 1
        
        self.display_current()

    def clear_plot(self):
        fig = self.canv.figure
        for ax in fig.axes:
            fig.delaxes(ax)

        for txt in self.texts:
            txt.remove()

        self.texts = []

        fig.suptitle("QUIDDIT")


    def create_fig_text(self, fig, xpos, ypos, contents=""):
        """create a new figure text at a given position
        """
        txt = fig.text(xpos, ypos, contents)
        self.texts.append(txt)
        return txt

    def create_slider(self, fig, xpos=0.2, ypos=0.3, width=0.65, height=0.03, axcolor = "lightgoldenrodyellow", caption=None,
                      minvalue=0.0, maxvalue=1.0, initialvalue=0.5,
                      valfmt="{:.2e}",
                      onchange = None,
                      hastenth=False):
        """create a slider object and an additional 10th slider object and also a text to display the value
           set by the positions ob the two sliders
        """
        h = height
        th = 1/3*height
        if(hastenth):
            h = height - th

        axis = fig.add_axes([xpos, ypos, width, h], facecolor=axcolor)
        if hastenth:
            tenthaxis = fig.add_axes([xpos, ypos+h, width, th], facecolor=axcolor)

        slider = Slider(axis, caption, minvalue, maxvalue, valinit=initialvalue, valfmt='')
        if hastenth:
            w10 = abs(slider.valmax - slider.valmin)/10
            tenthslider = Slider(tenthaxis, None, 0.0, w10, valinit=w10/2, valfmt='')
        else:
            tenthslider = None

        text = fig.text(xpos + width + 0.01, ypos, valfmt.format(slider.val))
        self.texts.append(text)

        if onchange!=None:
            slider.on_changed(onchange)
            if hastenth:
                tenthslider.on_changed(onchange)

        if hastenth:
            return slider, text, tenthslider
        else:
            return slider, text

    def create_sym_slider(self, fig, xpos=0.2, ypos=0.3, width=0.65, height=0.03, axcolor = "lightgoldenrodyellow", caption=None,
                      initialvalue=0.5, widthperc=0.1,
                      valfmt="{:.2e}",
                      onchange = None,
                      hastenth=False):
        """Create symmetrical slider"""

        valspan = abs(initialvalue * widthperc/2)

        return self.create_slider(fig, xpos=xpos, ypos=ypos, width=width, height=height, axcolor=axcolor, caption=caption,
                      minvalue=initialvalue-valspan, maxvalue=initialvalue+valspan, initialvalue=initialvalue,
                      valfmt=valfmt,
                      onchange=onchange,
                      hastenth=hastenth)


    def get_disp_value(self, slider, slider10):
        w = slider10.valmax - slider10.valmin
        return slider.val + slider10.val - w/2

