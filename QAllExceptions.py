# In this module we collect all axceptions specially designet for quiddit
class TclWinBaseUsageException(BaseException):
    """Exception for not allowed usage or errors in Tcl's basic window functions
    """
    def __init__(self, arg):
        self.args = arg
