class QCanvasHelperBase:
    """class to help with populating the canvas
    """
    def __init__(self, canvas):
        self.canv = canvas
        self.current = 0
        self.maxidx = 0
    
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
        for ax in fig.get_axes():
            fig.delaxes(ax)


        fig.suptitle("QUIDDIT")