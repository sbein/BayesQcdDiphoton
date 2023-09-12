import ROOT as rt
from array import *
from sms import *
from color import *

class smsPlotABS(object):
    # modelname is the sms name (see sms.py)
    # histo is the 2D xsec map
    # sig1Limits is a list of expected limits [NOMINAL]
    # sig2Limits is a list of expected limits [NOMINAL]
    # sig3Limits is a list of expected limits [NOMINAL]
    # label is a label referring to the analysis (e.g. RA1, RA2, RA2b, etc)

    def __init__(self, modelname, histo, sig1Limits, sig2Limits, sig3Limits, energy, lumi, preliminary, boxes, label):
        self.standardDef(modelname, histo, sig1Limits, sig2Limits, sig3Limits, energy, lumi, preliminary, boxes)
        self.LABEL = label
        self.c = rt.TCanvas("cABS_%s" %label,"cABS_%s" %label,300,300)
        self.histo = histo

    def standardDef(self, modelname, histo, sig1Limits, sig2Limits, sig3Limits, energy, lumi, preliminary, boxes):
        # which SMS?
        self.model = sms(modelname)
        self.SIG1 = sig1Limits
        self.SIG2 = sig2Limits
        self.SIG3 = sig3Limits
        self.lumi = lumi
        self.energy = energy
        self.preliminary = preliminary
        self.boxes = boxes
        # create the reference empty histo
        self.emptyhisto = self.emptyHistogramFromModel()

    def emptyHistogramFromModel(self):
        self.emptyHisto = rt.TH2D("emptyHisto", "", 1, self.model.Xmin, self.model.Xmax, 1, self.model.Ymin, self.model.Ymax)
        
    # define the plot canvas
    def setStyle(self):
        # canvas style
        rt.gStyle.SetOptStat(0)
        rt.gStyle.SetOptTitle(0)

        #self.c.SetLogz()
        self.c.SetTickx(1)
        self.c.SetTicky(1)

        self.c.SetRightMargin(0.19)
        self.c.SetTopMargin(0.08)
        self.c.SetLeftMargin(0.165)
        self.c.SetBottomMargin(0.14)

        # set x axis
        self.emptyHisto.GetXaxis().SetLabelFont(42)
        self.emptyHisto.GetXaxis().SetLabelSize(0.04)
        self.emptyHisto.GetXaxis().SetNdivisions(self.model.divX,self.model.optX)
        self.emptyHisto.GetXaxis().SetTitleFont(42)
        self.emptyHisto.GetXaxis().SetTitleSize(0.05)
        self.emptyHisto.GetXaxis().SetTitleOffset(1.2)
        self.emptyHisto.GetXaxis().SetTitle(self.model.sParticle)
        #self.emptyHisto.GetXaxis().CenterTitle(True)

        # set y axis
        self.emptyHisto.GetYaxis().SetLabelFont(42)
        self.emptyHisto.GetYaxis().SetLabelSize(0.04)
        self.emptyHisto.GetYaxis().SetNdivisions(self.model.divY,self.model.optY)
        self.emptyHisto.GetYaxis().SetTitleFont(42)
        self.emptyHisto.GetYaxis().SetTitleSize(0.05)
        self.emptyHisto.GetYaxis().SetTitleOffset(1.6)
        self.emptyHisto.GetYaxis().SetTitle(self.model.LSP)
        #self.emptyHisto.GetYaxis().CenterTitle(True)
                
    def DrawText(self):
        #redraw axes
        self.c.RedrawAxis()
        # white background
        graphWhite = rt.TGraph(5)
        graphWhite.SetName("white")
        graphWhite.SetTitle("white")
        graphWhite.SetFillColor(rt.kWhite)
        graphWhite.SetFillStyle(1001)
        graphWhite.SetLineColor(rt.kBlack)
        graphWhite.SetLineStyle(1)
        graphWhite.SetLineWidth(3)
        graphWhite.SetPoint(0,self.model.Xmin, self.model.Ymax)
        graphWhite.SetPoint(1,self.model.Xmax, self.model.Ymax)
        graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.7)
        graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.7)
        graphWhite.SetPoint(4,self.model.Xmin, self.model.Ymax)
        graphWhite.Draw("FSAME")
        graphWhite.Draw("LSAME")
        self.c.graphWhite = graphWhite
        
        # CMS LABEL
        if "Simulation" in self.preliminary:
            textCMS = rt.TLatex(0.15,0.98,"CMS %s" %(self.preliminary.replace("_"," ")))
        else:
            textCMS = rt.TLatex(0.15,0.98,"CMS #scale[0.8]{#font[52]{%s}}" %(self.preliminary.replace("_"," ")))
        textCMS.SetNDC()
        textCMS.SetTextAlign(13)
        textCMS.SetTextFont(62)
        textCMS.SetTextSize(0.05)
        textCMS.Draw()
        if self.lumi >= 1.0e6:
            textCMS1 = rt.TLatex(0.57,0.98,"%.0f ab^{-1} (%s TeV)" %(float(self.lumi)/1000000., self.energy))
        else:
            textCMS1 = rt.TLatex(0.57,0.98,"%.1f fb^{-1} (%s TeV)" %(float(self.lumi)/1000., self.energy))
        textCMS1.SetNDC()
        textCMS1.SetTextAlign(13)
        textCMS1.SetTextFont(42)
        textCMS1.SetTextSize(0.038)
        textCMS1.Draw()
        self.c.textCMS = textCMS
        self.c.textCMS1 = textCMS1
        # MODEL LABEL
        textModelLabel= rt.TLatex(0.185,0.90,"%s" %self.model.label)
        #textModelLabel= rt.TLatex(0.16,0.90,"%s" %self.model.label)
        #textModelLabel= rt.TLatex(0.16,0.915,"%s" %self.model.label)
        textModelLabel.SetNDC()
        textModelLabel.SetTextAlign(13)
        textModelLabel.SetTextFont(42)
        textModelLabel.SetTextSize(0.036)
        textModelLabel.Draw()
        self.c.textModelLabel = textModelLabel
        
        #textModelLabel2 = rt.TLatex(0.56,0.88,"NLO+NLL exclusion")
        ##  textModelLabel2 = rt.TLatex(0.52,0.725,"NLO+NLL exclusion")
        ##  textModelLabel2.SetNDC()
        ##  textModelLabel2.SetTextAlign(13)
        ##  textModelLabel2.SetTextFont(42)
        ##  textModelLabel2.SetTextSize(0.036)
        ##  textModelLabel2.Draw()
        ##  self.c.textModelLabel2 = textModelLabel2
        # MASS LABEL
        textMassLabel= rt.TLatex(0.57,0.82,"%s"%self.model.masslabel)
        textMassLabel.SetNDC()
        textMassLabel.SetTextAlign(13)
        textMassLabel.SetTextFont(42)
        textMassLabel.SetTextSize(0.036)
        textMassLabel.Draw()
        self.c.textNLONLL = textMassLabel
        # BOXES LABEL
        textBoxesLabel= rt.TLatex(0.54,0.885,"%s" %self.boxes.replace("_"," "))
        textBoxesLabel.SetNDC()
        textBoxesLabel.SetTextAlign(13)
        textBoxesLabel.SetTextFont(52)
        textBoxesLabel.SetTextSize(0.036)
        textBoxesLabel.Draw()
        self.c.textBoxesLabel = textBoxesLabel

    def Save(self,label):
        # save the output
        self.c.SaveAs("%s.pdf" %label)
        self.c.SaveAs("%s.png" %label)
        self.c.SaveAs("%s.C" %label)
        
    def DrawLegend(self):
        xRange = self.model.Xmax-self.model.Xmin
        yRange = self.model.Ymax-self.model.Ymin
        
        LSig1 = rt.TGraph(2)
        LSig1.SetName("LSig1")
        LSig1.SetTitle("LSig1")
        LSig1.SetLineColor(color(self.SIG1['colorLine']))
        LSig1.SetLineStyle(1)
        LSig1.SetLineWidth(3)
        LSig1.SetMarkerStyle(20)
        LSig1.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.35*yRange/100*10)
        LSig1.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.35*yRange/100*10)
        
        textSig1 = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-1.50*yRange/100*10, "with Run 2 syst. uncert.")
        textSig1.SetTextFont(42)
        textSig1.SetTextSize(0.035)
        textSig1.Draw()
        self.c.textSig1 = textSig1

        LSig2 = rt.TGraph(2)
        LSig2.SetName("LSig2")
        LSig2.SetTitle("LSig2")
        LSig2.SetLineColor(color(self.SIG2['colorLine']))
        LSig2.SetLineStyle(1)
        LSig2.SetLineWidth(3)
        LSig2.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        LSig2.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        
        textSig2 = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10, "with YR18 syst. uncert.")
        textSig2.SetTextFont(42)
        textSig2.SetTextSize(0.035)
        textSig2.Draw()
        self.c.textSig2 = textSig2

        LSig3 = rt.TGraph(2)
        LSig3.SetName("LSig3")
        LSig3.SetTitle("LSig3")
        LSig3.SetLineColor(color(self.SIG3['colorLine']))
        LSig3.SetLineStyle(1)
        LSig3.SetLineWidth(3)
        LSig3.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.65*yRange/100*10)
        LSig3.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.65*yRange/100*10)
        
        textSig3 = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.80*yRange/100*10, "with stat. uncert. only")
        textSig3.SetTextFont(42)
        textSig3.SetTextSize(0.035)
        textSig3.Draw()
        self.c.textSig3 = textSig3

        LSig1.Draw("LSAME")
        LSig2.Draw("LSAME")
        LSig3.Draw("LSAME")
        
        self.c.LSig1 = LSig1
        self.c.LSig2 = LSig2
        self.c.LSig3 = LSig3

    def DrawDiagonal(self):
        diagonal = rt.TGraph(3, self.model.diagX, self.model.diagY)
        diagonal.SetName("diagonal")
        diagonal.SetFillColor(rt.kWhite)
        diagonal.SetLineColor(rt.kGray)
        diagonal.SetLineStyle(2)
        diagonal.Draw("FSAME")
        diagonal.Draw("LSAME")
        self.c.diagonal = diagonal
        
    def DrawDiagonalTop(self):            
        filltop = rt.TGraph(4, self.model.fillXtop, self.model.fillYtop)
        filltop.SetName("filltop")
        filltop.SetFillColor(rt.kWhite)
        filltop.Draw("FSAME")
        
        diagtop = rt.TGraph(3, self.model.diagXtop, self.model.diagYtop)
        diagtop.SetName("diagtop")
        diagtop.SetFillColor(rt.kWhite)
        diagtop.SetLineColor(rt.kGray)
        diagtop.SetLineStyle(2)
        diagtop.Draw("LSAME")
        self.c.filltop = filltop                
        self.c.diagtop = diagtop                
        
    def DrawLines(self):
        # sig1
        self.SIG1['nominal'].SetLineColor(color(self.SIG1['colorLine']))
        self.SIG1['nominal'].SetLineStyle(1)
        self.SIG1['nominal'].SetLineWidth(3)
        # sig2
        self.SIG2['nominal'].SetLineColor(color(self.SIG2['colorLine']))
        self.SIG2['nominal'].SetLineStyle(1)
        self.SIG2['nominal'].SetLineWidth(3)        
        # sig3
        self.SIG3['nominal'].SetLineColor(color(self.SIG3['colorLine']))
        self.SIG3['nominal'].SetLineStyle(1)
        self.SIG3['nominal'].SetLineWidth(3)
        # DRAW LINES
        self.SIG3['nominal'].Draw("LSAME")
        self.SIG2['nominal'].Draw("LSAME")
        self.SIG1['nominal'].Draw("LSAME")

        
