
from ROOT import *
from utils import *
gStyle.SetOptStat(0)
import os, sys
#porpoise: talke in outputs of finalplotmaker.py and make one mega prediction.
linscale = False

tl2 = TLatex()


snuffoutmiddlelow = False
poolAllCats = False

try: year = sys.argv[1]
except: year = '2016'

'''
python tools/concatenateForInterpretation.py 2016
python tools/concatenateForInterpretation.py 2017
python tools/concatenateForInterpretation.py 2018
'''

if year=='2016':
    lumi = 35.9 # 2016 
if year=='2017':
    lumi = 41.52
if year=='2018':
    lumi = 54.52

datamc = 'data'
datamc = 'mc'
if year=='2016': datamc='data'

flow = TFile('plots_'+year+'_'+datamc+'_phopho_BDTLow.root')
fmid = TFile('plots_'+year+'_'+datamc+'_phopho_BDTMid.root')
fhigh = TFile('plots_'+year+'_'+datamc+'_phopho_BDTHigh.root')
fhigh.ls()
thekeys = flow.GetListOfKeys()

metlabels = ['E_{T}^{miss}#in[130,150) GeV','E_{T}^{miss}#in[150,185) GeV','E_{T}^{miss}#in[185,250] GeV','E_{T}^{miss}>250 GeV']

#130,150,185,250,500

fnew = TFile('master'+year+snuffoutmiddlelow*('_snuffmidlow')+poolAllCats*('_poolTheCats')+'.root','recreate')

files = [flow, fmid, fhigh]
if datamc=='data': haux = flow.Get('e faking #gamma').Clone('hSkeleton')
else: haux = flow.Get('t#bar{t}+jets').Clone('hSkeleton')
xax = haux.GetXaxis()
nbins = xax.GetNbins()
NBins = len(files)*nbins
hmasters = []
hsignals = []

cGold = mkcanvas('cmaster')

leg = mklegend(x1=.15, y1=.53, x2=.48, y2=.8, color=kWhite)
for ikey, key in enumerate(thekeys):
    
    name = key.GetName()
    #if 'T6' in name or 'T5' in name: continue
    print 'name....', name
    if 'c_'==name[:2]: continue
    hMaster = TH1F(name,name,NBins,1,NBins+1)
    xaxmaster = hMaster.GetXaxis()
    for ifile, thefile in enumerate(files):
        fname = thefile.GetName()
        print 'listing'
        thefile.ls()
        print name
        hist = thefile.Get(name)
        print 'the hist', hist, thefile, 'the name', name
        hist.SetDirectory(0)        
        if ifile==0:
            histoStyler(hMaster, hist.GetLineColor())
            xaxmaster.SetLabelOffset(1.5*xaxmaster.GetLabelOffset())            
            hMaster.SetFillStyle(1001)
            hMaster.SetFillColor(hMaster.GetLineColor())            
            xax_ = hist.GetXaxis()
        
        for ibin in range(1,xax_.GetNbins()+1):
            if poolAllCats: ourbin = (len(files)-1)*nbins+ibin
            else: ourbin = ifile*nbins+ibin
            print 'it is', hMaster
            hMaster.SetBinContent(ourbin, hist.GetBinContent(ibin)+hMaster.GetBinContent(ourbin))
            hMaster.SetBinError(ourbin, TMath.Sqrt(hist.GetBinError(ibin)**2++hMaster.GetBinError(ourbin)**2))
            xaxmaster.SetBinLabel(ifile*nbins+ibin, metlabels[ibin-1])
            
        if ('Mid' in fname or 'High' in fname) and snuffoutmiddlelow: hMaster.Reset()
    hMaster.SetFillStyle(1001)
    hMaster.Write(name)
    if name[0:2] in ['T5','T6']: hsignals.append(hMaster.Clone())
    else: 
       print 'master!', name
       hmasters.append(hMaster.Clone())

print 'came out with ', len(hmasters), hmasters, 'master hists'
hObserved = hmasters[0].Clone('hobserved')
hObserved.SetTitle('data')
hObserved.SetDirectory(0)
hmasters = hmasters[1:]
#exit(0)
#hObserved.Reset()
histoStyler(hObserved, kBlack)
hratio, hmethodsyst = FabDrawSystyRatio(cGold,leg,hObserved,hmasters,datamc=datamc,lumi=str(lumi), title = '',LinearScale=linscale,fractionthing='observed/method')
hratio.SetLabelSize(1.2*hratio.GetLabelSize())
#hratio.GetXaxis().LabelsOption('v')
hratio.GetYaxis().SetRangeUser(0,2.4)
hratio.GetXaxis().SetLabelOffset(0.03)
hratio.SetNdivisions(20)
hratio.GetXaxis().CenterLabels()
pad1, pad2 = hmethodsyst[-2:]

pad1.cd()
leg2 = mklegend(x1=.43, y1=.59, x2=.89, y2=.78, color=kWhite)
for hsig in hsignals[:3]:
    hsig.SetFillStyle(0)
    hsig.SetLineWidth(3)
    hsig.Draw('same hist')
    leg2.AddEntry(hsig, hsig.GetTitle(), 'l')
leg2.Draw()
line = TLine(5, 0.0001, 5, 15)
line.SetLineStyle(kDashed)
line.SetLineColor(kBlack)
line.SetLineWidth(3)
line.Draw()
line2 = TLine(9, 0.0001, 9, 15)
line2.SetLineStyle(kDashed)
line2.SetLineColor(kBlack)
line2.SetLineWidth(3)
line2.Draw()

tl2.DrawLatex(2.2, .2, 'low-BDT')
tl2.DrawLatex(5.5, .3, 'mid-BDT')
tl2.DrawLatex(9.4, .5, 'high-BDT')

pad2.cd()
pad2.SetBottomMargin(0.32)
line.Draw()
line2.Draw()


hObserved.GetYaxis().SetRangeUser(0.0015,5000)
for h in hmasters:
    h.GetYaxis().SetRangeUser(0.0015, 5000)
cGold.Update()
fnew.cd()
cGold.Write('cMaster')
cGold.Print('master'+year+'.png')
fname = fnew.GetName()
fnew.Close()
print 'just created', fname

exit(0)
