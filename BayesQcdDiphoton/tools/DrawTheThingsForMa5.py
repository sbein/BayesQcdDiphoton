from ROOT import *
from utils import *


'''with a grid proxy:
xrdfs root://hepxrd01.colorado.edu:1094/ ls /store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/scan/
'''

#xrdfs root://hepxrd01.colorado.edu:1094/ ls /store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/scan/T1bbbb_mMother-1500_mLSP-100_MC2016_fast.root



base = 'root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/'
#files = ['scan/T1bbbb_mMother-1800_mLSP-200_MC2016_fast.root', 'T1bbbb_mMother-1800_mLSP-200_MC2017_fast.root', 'T1bbbb_mMother-1800_mLSP-200_MC2018_fast.root']

files = ['scan/T1bbbb_mMother-1500_mLSP-100_MC2016_fast.root','Summer16v3/SMS-T1bbbb_mGluino-1500_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8//1_RA2AnalysisTree.root']

plots = {}
plots['HT'] = ['HT>>hadc(30,0,3000)','NLeptons==0']

thefiles = []
thehists = []
arg = 'hist'
extrathingy = '>>hadc(4,0,4)'
for fname in files:
    thefiles.append(TFile.Open(base+fname))
    thefiles[-1].ls()
    if 'scan' in fname: t = thefiles[-1].Get('tree')
    else: t = thefiles[-1].Get('TreeMaker2/PreSelection')
    print 'entries...', t.GetEntries()
    t.Draw("TMath::Min(3,BTags)"+extrathingy,"MHT>300",arg)
    thehists.append(t.GetHistogram().Clone(fname.split('/')[-1]))
    #extrathingy = ""
    #arg = 'same hist'
    pause()

thehists.reverse()
arg = 'hist'
color = kBlue
for hist in thehists:
    histoStyler(hist, color)
    hist.Scale(1.0/hist.Integral())
    hist.Draw(arg)
    arg = 'hist same'
    color = kRed
    
c1.Update()
c1.SetLogy()
pause()
    
