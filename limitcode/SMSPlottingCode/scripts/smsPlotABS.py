import ROOT as rt
from array import *
from sms import *
from color import *

samsyoffset = 0.018
samsyoffset = 0.038

class smsPlotABS(object):
    # modelname is the sms name (see sms.py)
    # histo is the 2D xsec map
    # obsLimits is a list of opbserved limits [NOMINAL, +1SIGMA, -1SIGMA]
    # expLimits is a list of expected limits [NOMINAL, +1SIGMA, -1SIGMA]
    # expLimits2 is a list of expected limits [NOMINAL, +2SIGMA, -2SIGMA]
    # label is a label referring to the analysis (e.g. RA1, RA2, RA2b, etc)

    def __init__(self, modelname, histo, obsLimits, expLimits, expLimits2, energy, lumi, preliminary, boxes, label):
        self.standardDef(modelname, histo, obsLimits, expLimits, expLimits2, energy, lumi, preliminary, boxes)
        self.LABEL = label
        self.c = rt.TCanvas("cABS_%s" %label,"cABS_%s" %label,300,300)
        self.histo = histo

    def standardDef(self, modelname, histo, obsLimits, expLimits, expLimits2, energy, lumi, preliminary, boxes):
        # which SMS?
        self.model = sms(modelname)
        print "model:", self.model.modelname, self.model.label, self.model.Xmin, self.model.Xmax, self.model.Zmin, self.model.Zmax
        self.OBS = obsLimits
        self.EXP = expLimits
        self.EXP2 = expLimits2
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
        #self.c.SetTickx(1)
        #self.c.SetTicky(1)

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
        graphWhite.SetPoint(2,self.model.Xmax, self.model.Ymax*0.787)
        graphWhite.SetPoint(3,self.model.Xmin, self.model.Ymax*0.787)
        graphWhite.SetPoint(4,self.model.Xmin, self.model.Ymax)
        graphWhite.Draw("FSAME")
        graphWhite.Draw("LSAME")
        self.c.graphWhite = graphWhite

        # CMS LABEL
        if "Simulation" in self.preliminary:
            textCMS = rt.TLatex(0.15,0.97,"CMS %s" %(self.preliminary.replace("_"," ")))
        else:
            textCMS = rt.TLatex(0.15,0.97,"CMS #scale[0.8]{#font[52]{%s}}" %(self.preliminary.replace("_"," ")))
        textCMS.SetNDC()
        textCMS.SetTextAlign(13)
        textCMS.SetTextFont(62)
        textCMS.SetTextSize(0.05)
        textCMS.Draw()
        if float(self.lumi) > 1000000.:
            textCMS1 = rt.TLatex(0.57,0.97,"%.0f ab^{-1} (%s TeV)" %(float(self.lumi)/1000000., self.energy))
        else:
            textCMS1 = rt.TLatex(0.57,0.97,"%.1f fb^{-1} (%s TeV)" %(float(self.lumi)/1000., self.energy))
        textCMS1.SetNDC()
        textCMS1.SetTextAlign(13)
        textCMS1.SetTextFont(42)
        textCMS1.SetTextSize(0.038)
        textCMS1.Draw()
        self.c.textCMS = textCMS
        self.c.textCMS1 = textCMS1
        # MODEL LABEL        
        textModelLabel= rt.TLatex(0.185,0.88+samsyoffset,"%s" %self.model.label)
        #textModelLabel= rt.TLatex(0.16,0.90,"%s" %self.model.label)
        #textModelLabel= rt.TLatex(0.16,0.915,"%s" %self.model.label)
        textModelLabel.SetNDC()
        textModelLabel.SetTextAlign(13)
        textModelLabel.SetTextFont(42)
        textModelLabel.SetTextSize(0.036)
        textModelLabel.Draw()
        self.c.textModelLabel = textModelLabel
        
        #textModelLabel2 = rt.TLatex(0.56,0.88,"NLO+NLL exclusion")
        #textModelLabel2 = rt.TLatex(0.52,0.725,"NLO+NLL exclusion")
        textModelLabel2 = rt.TLatex(0.51,0.885+samsyoffset,"NLO+NLL exclusion")##this is drawn
        textModelLabel2.SetNDC()
        textModelLabel2.SetTextAlign(13)
        textModelLabel2.SetTextFont(42)
        textModelLabel2.SetTextSize(0.036)
        ####SB####textModelLabel2.Draw()
        self.c.textModelLabel2 = textModelLabel2
        # MASS LABEL
        textMassLabel= rt.TLatex(0.575,0.82+samsyoffset+.01,"%s"%self.model.masslabel)
        textMassLabel.SetNDC()
        textMassLabel.SetTextAlign(13)
        textMassLabel.SetTextFont(42)
        textMassLabel.SetTextSize(0.036)
        textMassLabel.Draw()
        self.c.textNLONLL = textMassLabel
        # BOXES LABEL
        textBoxesLabel= rt.TLatex(0.18,0.73+samsyoffset,"%s" %self.boxes.replace("_"," "))
        textBoxesLabel.SetNDC()
        textBoxesLabel.SetTextAlign(13)
        textBoxesLabel.SetTextFont(52)
        textBoxesLabel.SetTextSize(0.036)
        #textBoxesLabel.Draw()
        self.c.textBoxesLabel = textBoxesLabel

    def Save(self,label):
        # save the output
        self.c.SaveAs("%s.pdf" %label)
        self.c.SaveAs("%s.png" %label)
        self.c.SaveAs("%s.C" %label)
        
    def DrawLegend(self):
        xRange = self.model.Xmax-self.model.Xmin
        yRange = self.model.Ymax-self.model.Ymin
        
        LObs = rt.TGraph(2)
        LObs.SetName("LObs")
        LObs.SetTitle("LObs")
        try:
            LObs.SetLineColor(color(self.OBS['colorLine']))
        except TypeError:
            LObs.SetLineColor(rt.kBlack)
        LObs.SetLineStyle(1)
        LObs.SetLineWidth(4)
        LObs.SetMarkerStyle(20)
        LObs.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.35*yRange/100*10+4000*samsyoffset)
        LObs.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.35*yRange/100*10+4000*samsyoffset)
        
        LObsP = rt.TGraph(2)
        LObsP.SetName("LObsP")
        LObsP.SetTitle("LObsP")
        try:
            LObsP.SetLineColor(color(self.OBS['colorLine']))
        except TypeError:
            LObsP.SetLineColor(rt.kBlack)
        LObsP.SetLineStyle(1)
        LObsP.SetLineWidth(2)
        LObsP.SetMarkerStyle(20)
        LObsP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.20*yRange/100*10+4000*samsyoffset)
        LObsP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.20*yRange/100*10+4000*samsyoffset)
        
        LObsM = rt.TGraph(2)
        LObsM.SetName("LObsM")
        LObsM.SetTitle("LObsM")
        try:
            LObsM.SetLineColor(color(self.OBS['colorLine']))
        except TypeError:
            LObsP.SetLineColor(rt.kBlack)
        LObsM.SetLineStyle(1)
        LObsM.SetLineWidth(2)
        LObsM.SetMarkerStyle(20)
        LObsM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.50*yRange/100*10+4000*samsyoffset)
        LObsM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.50*yRange/100*10+4000*samsyoffset)
        
        
        textObs = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-1.50*yRange/100*10+4000*samsyoffset, "Observed #pm 1 #sigma_{theory}")
        textObs.SetTextFont(42)
        textObs.SetTextSize(0.040)
        textObs.Draw()
        self.c.textObs = textObs

        LExpP = rt.TGraph(2)
        LExpP.SetName("LExpP")
        LExpP.SetTitle("LExpP")
        LExpP.SetLineColor(color(self.EXP['colorLine']))
        LExpP.SetLineStyle(7)
        LExpP.SetLineWidth(2)  
        LExpP.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.85*yRange/100*10+4000*samsyoffset)
        LExpP.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.85*yRange/100*10+4000*samsyoffset)
        
        LExp = rt.TGraph(2)
        LExp.SetName("LExp")
        LExp.SetTitle("LExp")
        LExp.SetLineColor(color(self.EXP['colorLine']))
        LExp.SetLineStyle(7)
        LExp.SetLineWidth(4)
        LExp.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.00*yRange/100*10+4000*samsyoffset)
        LExp.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.00*yRange/100*10+4000*samsyoffset)
        
        LExpM = rt.TGraph(2)
        LExpM.SetName("LExpM")
        LExpM.SetTitle("LExpM")
        LExpM.SetLineColor(color(self.EXP['colorLine']))
        LExpM.SetLineStyle(7)
        LExpM.SetLineWidth(2)  
        LExpM.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.15*yRange/100*10+4000*samsyoffset)
        LExpM.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.15*yRange/100*10+4000*samsyoffset)

        LExpP2 = rt.TGraph(2)
        LExpP2.SetName("LExpP2")
        LExpP2.SetTitle("LExpP2")
        LExpP2.SetLineColor(color(self.EXP2['colorLine']))
        LExpP2.SetLineStyle(7)
        LExpP2.SetLineWidth(2)  
        LExpP2.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-1.75*yRange/100*10+4000*samsyoffset)
        LExpP2.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-1.75*yRange/100*10+4000*samsyoffset)

        LExpM2 = rt.TGraph(2)
        LExpM2.SetName("LExpM")
        LExpM2.SetTitle("LExpM")
        LExpM2.SetLineColor(color(self.EXP2['colorLine']))
        LExpM2.SetLineStyle(7)
        LExpM2.SetLineWidth(2)  
        LExpM2.SetPoint(0,self.model.Xmin+3*xRange/100, self.model.Ymax-2.25*yRange/100*10+4000*samsyoffset)
        LExpM2.SetPoint(1,self.model.Xmin+10*xRange/100, self.model.Ymax-2.25*yRange/100*10+4000*samsyoffset)
        
        #textExp = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10, "Expected #pm 1, #pm 2 #sigma_{experiment}")
        textExp = rt.TLatex(self.model.Xmin+11*xRange/100, self.model.Ymax-2.15*yRange/100*10+4000*samsyoffset, "Expected #pm 1 #sigma_{experiment}")
        textExp.SetTextFont(42)
        textExp.SetTextSize(0.040)
        textExp.Draw()
        self.c.textExp = textExp

        LObs.Draw("LSAME")
        LObsM.Draw("LSAME")
        LObsP.Draw("LSAME")
        LExp.Draw("LSAME")
        #LExpM2.Draw("LSAME")
        #LExpP2.Draw("LSAME")
        LExpM.Draw("LSAME")
        LExpP.Draw("LSAME")
        
        self.c.LObs = LObs
        self.c.LObsM = LObsM
        self.c.LObsP = LObsP
        self.c.LExp = LExp
        self.c.LExpM = LExpM
        self.c.LExpP = LExpP
        #self.c.LExpM2 = LExpM2
        #self.c.LExpP2 = LExpP2

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
        # observed
        try:
            self.OBS['nominal'].SetLineColor(color(self.OBS['colorLine']))
            self.OBS['nominal'].SetLineStyle(1)
            self.OBS['nominal'].SetLineWidth(4)
            # observed + 1sigma
            self.OBS['plus'].SetLineColor(color(self.OBS['colorLine']))
            self.OBS['plus'].SetLineStyle(1)
            self.OBS['plus'].SetLineWidth(2)        
            # observed - 1sigma
            self.OBS['minus'].SetLineColor(color(self.OBS['colorLine']))
            self.OBS['minus'].SetLineStyle(1)
            self.OBS['minus'].SetLineWidth(2)        
        except TypeError: # if no observed limit
            pass
        # expected + 2sigma
        #self.EXP2['plus2'].SetLineColor(color(self.EXP2['colorLine']))
        #self.EXP2['plus2'].SetLineStyle(7)
        #self.EXP2['plus2'].SetLineWidth(2)                
        # expected + 1sigma
        self.EXP['plus'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['plus'].SetLineStyle(7)
        self.EXP['plus'].SetLineWidth(2)                
        # expected
        self.EXP['nominal'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['nominal'].SetLineStyle(7)
        self.EXP['nominal'].SetLineWidth(4)        
        # expected - 2sigma
        #self.EXP2['minus2'].SetLineColor(color(self.EXP2['colorLine']))
        #self.EXP2['minus2'].SetLineStyle(7)
        #self.EXP2['minus2'].SetLineWidth(2)          
        # expected - 1sigma
        self.EXP['minus'].SetLineColor(color(self.EXP['colorLine']))
        self.EXP['minus'].SetLineStyle(7)
        self.EXP['minus'].SetLineWidth(2)                      
        # DRAW LINES
        self.EXP['nominal'].Draw("LSAME")
        #self.EXP2['plus2'].Draw("LSAME")
        #self.EXP2['minus2'].Draw("LSAME")
        self.EXP['plus'].Draw("LSAME")
        self.EXP['minus'].Draw("LSAME")
        try:
            self.OBS['nominal'].Draw("LSAME")
            self.OBS['plus'].Draw("LSAME")
            self.OBS['minus'].Draw("LSAME")        
        except TypeError: # if no observed limit
            pass

