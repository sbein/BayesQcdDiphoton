import sys
from inputFile import *
from smsPlot4SIG import *
from smsPlotCONT import *
from smsPlotBrazil import *

if __name__ == '__main__':
    rt.gROOT.SetBatch()

    # read input arguments
    filename = sys.argv[1]
    modelname = "SIG-HL-"+sys.argv[1].split("/")[-1].split("_")[0]
    analysisLabel = sys.argv[1].split("/")[-1].split("_")[1]
    outputname = sys.argv[2]

    # read the config file
    fileIN = inputFile(filename)
    fileIN.HISTOGRAM['histogram'].Print('v')
    
    # classic temperature histogram
    sigPlot = smsPlotSIG(modelname, fileIN.HISTOGRAM, fileIN.SIG1, fileIN.SIG2, fileIN.SIG3, fileIN.SIG4, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, fileIN.BOXES, "")
    sigPlot.Draw()
    sigPlot.Save("%sSIG" %outputname)

    # only lines
    #contPlot = smsPlotCONT(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.EXPECTED2, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, fileIN.BOXES, "")
    #contPlot.Draw()
    #contPlot.Save("%sCONT" %outputname)

    # brazilian flag (show only 1 sigma)
    #brazilPlot = smsPlotBrazil(modelname, fileIN.HISTOGRAM, fileIN.OBSERVED, fileIN.EXPECTED, fileIN.EXPECTED2, fileIN.ENERGY, fileIN.LUMI, fileIN.PRELIMINARY, fileIN.BOXES, "")
    #brazilPlot.Draw()
    #brazilPlot.Save("%sBAND" %outputname)
