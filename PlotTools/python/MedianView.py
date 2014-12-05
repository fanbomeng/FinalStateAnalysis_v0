import rootpy.plotting.views as views
import math
def quad(*xs):
    return math.sqrt(sum(x * x for x in xs))

class MedianView(object):
    ''' Takes high and low, returns median assigning half the diff as error. '''
    def __init__(self, highv=None, lowv=None, centv=None, maxdiff=None):
        self.highv = highv
        self.lowv  = lowv
        self.centv = views.ScaleView( views.SumView(lowv, self.highv) , 0.5) if not centv else centv

    @staticmethod
    def apply_view(central_hist, high_hist, low_hist=None):
        ret_hist = central_hist.Clone()
        for bin in range(1, ret_hist.GetNbinsX() + 1):
            error = quad(
                central_hist.GetBinError(bin),
                abs(high_hist.GetBinContent(bin) - central_hist.GetBinContent(bin))
            ) if high_hist else \
            quad(
                central_hist.GetBinError(bin),
                abs(central_hist.GetBinContent(bin) - low_hist.GetBinContent(bin))
            ) 
            
            ret_hist.SetBinError(bin, error)
        return ret_hist
        
    @staticmethod
    def apply_view_maxDiff(central_hist, high_hist, low_hist):
        ret_hist = central_hist.Clone()
        for bin in range(1, ret_hist.GetNbinsX() + 1):
            errorup = quad(
                central_hist.GetBinError(bin),
                abs(high_hist.GetBinContent(bin) - central_hist.GetBinContent(bin))
            ) 
            errordw = quad(
                central_hist.GetBinError(bin),
                abs(central_hist.GetBinContent(bin) - low_hist.GetBinContent(bin))
            ) 
            error = errorup if errorup > errordw else errordw
            ret_hist.SetBinError(bin, error)
        return ret_hist
        

    def Get(self, path):
        central_hist = self.centv.Get(path)
        high_hist    = self.highv.Get(path) if self.highv else None
        low_hist     = self.lowv.Get(path)  if self.lowv  else None

        return self.apply_view(central_hist, high_hist, low_hist)

    def Get(self, path, maxdiff=False):
        central_hist = self.centv.Get(path)
        high_hist    = self.highv.Get(path) if self.highv else None
        low_hist     = self.lowv.Get(path)  if self.lowv  else None
        if maxdiff == True and low_hist!=None :
            return self.apply_view_maxDiff(central_hist, high_hist, low_hist)
        else:
            return self.apply_view(central_hist, high_hist, low_hist)

            
