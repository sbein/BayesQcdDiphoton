import ROOT as rt
from array import *
from sms import *
from color import *

class smsPlotABS(object):
    # modelname is the sms name (see sms.py)
    # histo is the 2D xsec map
    # syst0Limits is a list of expected limits [NOMINAL, +1SIGMA, -1SIGMA]
    # syst1Limits is a list of expected limits [NOMINAL, +1SIGMA, -1SIGMA]
    # syst2Limits is a list of expected limits [NOMINAL, +1SIGMA, -1SIGMA]
    # syst3Limits is a list of expected limits [NOMINAL, +1SIGMA, -1SIGMA]
    # label is a label referring to the analysis (e.g. RA1, RA2, RA2b, etc)
    def __init__(self, modelname, histo, syst0Limits, syst1Limits, syst2Limits, syst3Limits, energy, lumi, preliminary, boxes, label):
        self.standardDef(modelname, histo, syst0Limits, syst1Limits, syst2Limits, syst3Limits, energy, lumi, preliminary, boxes)
        self.LABEL = label
        self.c = rt.TCanvas("cABS_%s" %label,"cABS_%s" %label,300,300)
        self.histo = histo

    def standardDef(self, modelname, histo, syst0Limits, syst1Limits, syst2Limits, syst3Limits, energy, lumi, preliminary, boxes):
        # which SMS?
        self.model = sms(modelname)
        self.SYST0 = syst0Limits
        self.SYST1 = syst1Limits
        self.SYST2 = syst2Limits
        self.SYST3 = syst3Limits
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

        self.c.SetLogz()
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
        #graphWhite.Draw("FSAME")
        #graphWhite.Draw("LSAME")
        self.c.graphWhite = graphWhite
        
        # CMS LABEL
        textCMS = rt.TLatex(0.16,0.975,"CMS %s" %(self.preliminary.replace("_"," ")))
        textCMS.SetNDC()
        textCMS.SetTextAlign(13)
        textCMS.SetTextFont(62)
        textCMS.SetTextSize(0.043)
        textCMS.Draw()
        if self.lumi >= 1.0e6:
            textCMS1 = rt.TLatex(0.59,0.98,"%.0f ab^{-1} (%s TeV)" %(float(self.lumi)/1000000., self.energy))
        else:
            textCMS1 = rt.TLatex(0.59,0.98,"%.1f fb^{-1} (%s TeV)" %(float(self.lumi)/1000., self.energy))
        textCMS1.SetNDC()
        textCMS1.SetTextAlign(13)
        textCMS1.SetTextFont(42)
        textCMS1.SetTextSize(0.038)
        textCMS1.Draw()
        self.c.textCMS = textCMS
        self.c.textCMS1 = textCMS1
        # MODEL LABEL
        ##  textModelLabel2 = rt.TLatex(0.52,0.725,"NLO+NLL exclusion")
        #textModelLabel= rt.TLatex(0.185,0.90,"%s" %self.model.label)
        #textModelLabel= rt.TLatex(0.54,0.89,"%s" %self.model.label)
        textModelLabel= rt.TLatex(0.195,0.89,"%s" %self.model.label)
        textModelLabel.SetNDC()
        textModelLabel.SetTextAlign(13)
        textModelLabel.SetTextFont(42)
        textModelLabel.SetTextSize(0.032)
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
        #textBoxesLabel= rt.TLatex(0.54,0.73,"%s" %self.boxes.replace("_"," "))
        textBoxesLabel= rt.TLatex(0.195,0.79,"%s" %self.boxes.replace("_"," "))
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
        
        LSyst0 = rt.TGraph(2)
        LSyst0.SetName("LSyst0")
        LSyst0.SetTitle("LSyst0")
        LSyst0.SetLineColor(color(self.SYST0['colorLine']))
        LSyst0.SetLineStyle(7)
        LSyst0.SetLineWidth(3)
        LSyst0.SetMarkerStyle(20)
        LSyst0.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-0.70*yRange/100*10)
        LSyst0.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-0.70*yRange/100*10)
        
        LSyst0P = rt.TGraph(2)
        LSyst0P.SetName("LSyst0P")
        LSyst0P.SetTitle("LSyst0P")
        LSyst0P.SetLineColor(color(self.SYST0['colorLine']))
        LSyst0P.SetLineStyle(1)
        LSyst0P.SetLineWidth(2)
        LSyst0P.SetMarkerStyle(20)
        LSyst0P.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-0.55*yRange/100*10)
        LSyst0P.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-0.55*yRange/100*10)
        
        LSyst0M = rt.TGraph(2)
        LSyst0M.SetName("LSyst0M")
        LSyst0M.SetTitle("LSyst0M")
        LSyst0M.SetLineColor(color(self.SYST0['colorLine']))
        LSyst0M.SetLineStyle(1)
        LSyst0M.SetLineWidth(2)
        LSyst0M.SetMarkerStyle(20)
        LSyst0M.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-0.85*yRange/100*10)
        LSyst0M.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-0.85*yRange/100*10)

        textSyst0 = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-0.85*yRange/100*10, "Run 2 limit @ 35.9 fb^{-1}")
        textSyst0.SetTextFont(42)
        textSyst0.SetTextSize(0.032)
        #textSyst0.Draw()
        self.c.textSyst0 = textSyst0

        LSyst1 = rt.TGraph(2)
        LSyst1.SetName("LSyst1")
        LSyst1.SetTitle("LSyst1")
        LSyst1.SetLineColor(color(self.SYST1['colorLine']))
        LSyst1.SetLineStyle(1)
        LSyst1.SetLineWidth(3)
        LSyst1.SetMarkerStyle(20)
        LSyst1.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.35*yRange/100*10)
        LSyst1.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.35*yRange/100*10)
        
        LSyst1P = rt.TGraph(2)
        LSyst1P.SetName("LSyst1P")
        LSyst1P.SetTitle("LSyst1P")
        LSyst1P.SetLineColor(color(self.SYST1['colorLine']))
        LSyst1P.SetLineStyle(1)
        LSyst1P.SetLineWidth(2)
        LSyst1P.SetMarkerStyle(20)
        LSyst1P.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.20*yRange/100*10)
        LSyst1P.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.20*yRange/100*10)
        
        LSyst1M = rt.TGraph(2)
        LSyst1M.SetName("LSyst1M")
        LSyst1M.SetTitle("LSyst1M")
        LSyst1M.SetLineColor(color(self.SYST1['colorLine']))
        LSyst1M.SetLineStyle(1)
        LSyst1M.SetLineWidth(2)
        LSyst1M.SetMarkerStyle(20)
        LSyst1M.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.50*yRange/100*10)
        LSyst1M.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.50*yRange/100*10)
        
        textSyst1 = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-1.50*yRange/100*10, "with Run 2 syst. uncert.")
        textSyst1.SetTextFont(42)
        textSyst1.SetTextSize(0.032)
        #textSyst1.Draw()
        self.c.textSyst1 = textSyst1

        LSyst2P = rt.TGraph(2)
        LSyst2P.SetName("LSyst2P")
        LSyst2P.SetTitle("LSyst2P")
        LSyst2P.SetLineColor(color(self.SYST2['colorLine']))
        LSyst2P.SetLineStyle(1)
        LSyst2P.SetLineWidth(2)  
        LSyst2P.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.85*yRange/100*10)
        LSyst2P.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.85*yRange/100*10)
        
        LSyst2 = rt.TGraph(2)
        LSyst2.SetName("LSyst2")
        LSyst2.SetTitle("LSyst2")
        LSyst2.SetLineColor(color(self.SYST2['colorLine']))
        LSyst2.SetLineStyle(1)
        LSyst2.SetLineWidth(3)
        LSyst2.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        LSyst2.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.00*yRange/100*10)
        
        LSyst2M = rt.TGraph(2)
        LSyst2M.SetName("LSyst2M")
        LSyst2M.SetTitle("LSyst2M")
        LSyst2M.SetLineColor(color(self.SYST2['colorLine']))
        LSyst2M.SetLineStyle(1)
        LSyst2M.SetLineWidth(2)  
        LSyst2M.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.15*yRange/100*10)
        LSyst2M.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.15*yRange/100*10)

        textSyst2 = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10, "with YR18 syst. uncert.")
        textSyst2.SetTextFont(42)
        textSyst2.SetTextSize(0.032)
        #textSyst2.Draw()
        self.c.textSyst2 = textSyst2

        LSyst3P = rt.TGraph(2)
        LSyst3P.SetName("LSyst3P")
        LSyst3P.SetTitle("LSyst3P")
        LSyst3P.SetLineColor(color(self.SYST3['colorLine']))
        LSyst3P.SetLineStyle(1)
        LSyst3P.SetLineWidth(2)  
        LSyst3P.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.50*yRange/100*10)
        LSyst3P.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.50*yRange/100*10)
        
        LSyst3 = rt.TGraph(2)
        LSyst3.SetName("LSyst3")
        LSyst3.SetTitle("LSyst3")
        LSyst3.SetLineColor(color(self.SYST3['colorLine']))
        LSyst3.SetLineStyle(1)
        LSyst3.SetLineWidth(3)
        LSyst3.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.65*yRange/100*10)
        LSyst3.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.65*yRange/100*10)
        
        LSyst3M = rt.TGraph(2)
        LSyst3M.SetName("LSyst3M")
        LSyst3M.SetTitle("LSyst3M")
        LSyst3M.SetLineColor(color(self.SYST3['colorLine']))
        LSyst3M.SetLineStyle(1)
        LSyst3M.SetLineWidth(2)  
        LSyst3M.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.80*yRange/100*10)
        LSyst3M.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.80*yRange/100*10)
         
        textSyst3 = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.80*yRange/100*10, "with Stat. uncert. only")
        textSyst3.SetTextFont(42)
        textSyst3.SetTextSize(0.032)
        #textSyst3.Draw()
        self.c.textSyst3 = textSyst3

        #LSyst0.Draw("LSAME")
        ##LSyst0M.Draw("LSAME")
        ##LSyst0P.Draw("LSAME")
        #LSyst1.Draw("LSAME")
        ##LSyst1M.Draw("LSAME")
        ##LSyst1P.Draw("LSAME")
        #LSyst2.Draw("LSAME")
        ##LSyst2M.Draw("LSAME")
        ##LSyst2P.Draw("LSAME")
        #LSyst3.Draw("LSAME")
        ##LSyst3M.Draw("LSAME")
        ##LSyst3P.Draw("LSAME")
        
        self.c.LSyst0 = LSyst0
        self.c.LSyst0M = LSyst0M
        self.c.LSyst0P = LSyst0P
        self.c.LSyst1 = LSyst1
        self.c.LSyst1M = LSyst1M
        self.c.LSyst1P = LSyst1P
        self.c.LSyst2 = LSyst2
        self.c.LSyst2M = LSyst2M
        self.c.LSyst2P = LSyst2P
        self.c.LSyst3 = LSyst3
        self.c.LSyst3M = LSyst3M
        self.c.LSyst3P = LSyst3P

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
        # syst0
        self.SYST0['nominal'].SetLineColor(color(self.SYST0['colorLine']))
        self.SYST0['nominal'].SetLineStyle(7)
        self.SYST0['nominal'].SetLineWidth(3)
        # syst0 + 1sigma
        self.SYST0['plus'].SetLineColor(color(self.SYST0['colorLine']))
        self.SYST0['plus'].SetLineStyle(1)
        self.SYST0['plus'].SetLineWidth(2)        
        # syst0 - 1sigma
        self.SYST0['minus'].SetLineColor(color(self.SYST0['colorLine']))
        self.SYST0['minus'].SetLineStyle(1)
        self.SYST0['minus'].SetLineWidth(2)        
        # syst1
        self.SYST1['nominal'].SetLineColor(color(self.SYST1['colorLine']))
        self.SYST1['nominal'].SetLineStyle(1)
        self.SYST1['nominal'].SetLineWidth(3)
        # syst1 + 1sigma
        self.SYST1['plus'].SetLineColor(color(self.SYST1['colorLine']))
        self.SYST1['plus'].SetLineStyle(1)
        self.SYST1['plus'].SetLineWidth(2)        
        # syst1 - 1sigma
        self.SYST1['minus'].SetLineColor(color(self.SYST1['colorLine']))
        self.SYST1['minus'].SetLineStyle(1)
        self.SYST1['minus'].SetLineWidth(2)        
        # syst2
        self.SYST2['nominal'].SetLineColor(color(self.SYST2['colorLine']))
        self.SYST2['nominal'].SetLineStyle(1)
        self.SYST2['nominal'].SetLineWidth(3)        
        # syst2 + 1sigma
        self.SYST2['plus'].SetLineColor(color(self.SYST2['colorLine']))
        self.SYST2['plus'].SetLineStyle(1)
        self.SYST2['plus'].SetLineWidth(2)                
        # syst2 - 1sigma
        self.SYST2['minus'].SetLineColor(color(self.SYST2['colorLine']))
        self.SYST2['minus'].SetLineStyle(1)
        self.SYST2['minus'].SetLineWidth(2)                      
        # syst3
        self.SYST3['nominal'].SetLineColor(color(self.SYST3['colorLine']))
        self.SYST3['nominal'].SetLineStyle(1)
        self.SYST3['nominal'].SetLineWidth(3)          
        # syst3 + 1sigma
        self.SYST3['plus'].SetLineColor(color(self.SYST3['colorLine']))
        self.SYST3['plus'].SetLineStyle(1)
        self.SYST3['plus'].SetLineWidth(2)                
        # syst3 - 1sigma
        self.SYST3['minus'].SetLineColor(color(self.SYST3['colorLine']))
        self.SYST3['minus'].SetLineStyle(1)
        self.SYST3['minus'].SetLineWidth(2)
        # DRAW LINES
        #self.SYST3['nominal'].Draw("LSAME")
        ##self.SYST3['plus'].Draw("LSAME")
        ##self.SYST3['minus'].Draw("LSAME")
        #self.SYST2['nominal'].Draw("LSAME")
        ##self.SYST2['plus'].Draw("LSAME")
        ##self.SYST2['minus'].Draw("LSAME")
        #self.SYST1['nominal'].Draw("LSAME")
        ##self.SYST1['plus'].Draw("LSAME")
        ##self.SYST1['minus'].Draw("LSAME")        
        #self.SYST0['nominal'].Draw("LSAME")
        ##self.SYST0['plus'].Draw("LSAME")
        ##self.SYST0['minus'].Draw("LSAME")        

        
