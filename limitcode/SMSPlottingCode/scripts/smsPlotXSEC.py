import ROOT as rt
from array import *
from sms import *
from smsPlotABS import *
import time

# class producing the 2D plot with xsec colors
class smsPlotXSEC(smsPlotABS):

    def __init__(self, modelname, histo, obsLimits, expLimits, expLimits2, energy, lumi, preliminary, boxes, label):
        self.standardDef(modelname, histo, obsLimits, expLimits, expLimits2, energy, lumi, preliminary, boxes)
        self.LABEL = label
        # canvas for the plot
        self.c = rt.TCanvas("cCONT_%s" %label,"cCONT_%s" %label,600,600)
        print histo['histogram'].GetName(), histo['histogram'].GetMinimum(), histo['histogram'].GetMaximum()
        self.histo = histo['histogram']
        # canvas style
        self.setStyle()
        self.setStyleCOLZ()
        self.c.cd()
        self.c.SetLogz(1)
        self.histo.Draw('colz')
        self.c.Print('x.pdf')

    # define the plot canvas
    def setStyleCOLZ(self):
        # set z axis
        self.histo.GetZaxis().SetLabelFont(42)
        self.histo.GetZaxis().SetTitleFont(42)
        self.histo.GetZaxis().SetLabelSize(0.035)
        self.histo.GetZaxis().SetTitleSize(0.035)
        self.histo.SetMinimum(self.model.Zmin)
        self.histo.SetMaximum(self.model.Zmax)

        # define the palette for z axis
        NRGBs = 5
        NCont = 255
        stops = array("d",[0.00, 0.34, 0.61, 0.84, 1.00])
        red= array("d",[0.50, 0.50, 1.00, 1.00, 1.00])
        green = array("d",[ 0.50, 1.00, 1.00, 0.60, 0.50])
        blue = array("d",[1.00, 1.00, 0.50, 0.40, 0.50])
        rt.TColor.CreateGradientColorTable(NRGBs, stops, red, green, blue, NCont)
        rt.gStyle.SetNumberContours(NCont)

        rt.gPad.Update()
        palette = self.histo.GetListOfFunctions().FindObject("palette")
        palette.SetX1NDC(1.-0.18)
        palette.SetY1NDC(0.14)
        palette.SetX2NDC(1.-0.13)
        palette.SetY2NDC(1.-0.08)
        palette.SetLabelFont(42)
        palette.SetLabelSize(0.035)

    def DrawPaletteLabel(self):
        textCOLZ = rt.TLatex(0.98,0.15,"95% C.L. upper limit on cross section [pb]")
        textCOLZ.SetNDC()
        #textCOLZ.SetTextAlign(13)
        textCOLZ.SetTextFont(42)
        textCOLZ.SetTextSize(0.045)
        textCOLZ.SetTextAngle(90)
        textCOLZ.Draw()
        self.c.textCOLZ = textCOLZ

    def Draw(self):
        self.emptyHisto.GetXaxis().SetRangeUser(self.model.Xmin, self.model.Xmax)
        self.emptyHisto.GetYaxis().SetRangeUser(self.model.Ymin, self.model.Ymax)
        self.emptyHisto.Draw()
        #self.c.Print('x.pdf')

        # set x axis
        self.histo.GetXaxis().SetLabelFont(42)
        self.histo.GetXaxis().SetLabelSize(0.04)
        self.histo.GetXaxis().SetNdivisions(self.model.divX,self.model.optX)
        self.histo.GetXaxis().SetTitleFont(42)
        self.histo.GetXaxis().SetTitleSize(0.05)
        self.histo.GetXaxis().SetTitleOffset(1.2)
        self.histo.GetXaxis().SetTitle(self.model.sParticle)
        #self.emptyHisto.GetXaxis().CenterTitle(True)

        # set y axis
        self.histo.GetYaxis().SetLabelFont(42)
        self.histo.GetYaxis().SetLabelSize(0.04)
        self.histo.GetYaxis().SetNdivisions(self.model.divY,self.model.optY)
        self.histo.GetYaxis().SetTitleFont(42)
        self.histo.GetYaxis().SetTitleSize(0.05)
        self.histo.GetYaxis().SetTitleOffset(1.6)
        self.histo.GetYaxis().SetTitle(self.model.LSP)
        #self.emptyHisto.GetYaxis().CenterTitle(True)

        self.histo.Draw("COLZ")
        self.DrawDiagonal()
        self.DrawLines()
        try:
            if self.model.diagXtop and self.model.diagYtop and self.model.fillXtop and self.model.fillYtop: self.DrawDiagonalTop()
        except:
            pass
        self.DrawText()
        self.DrawLegend()
        self.DrawPaletteLabel()
