
import os, sys
from ROOT import *
from utils import *
gROOT.SetBatch(1)
gStyle.SetOptStat(0)
lumi = 36
dopred = False

'''
eosls /store/group/lpcsusyphotons/TreeMakerRandS_skimsv9/ > usefulthings/filelistDiphotonSkims.txt
python tools/DrawAnalyzeObjectStacks.py Summer16v3.DYJetsToLL_M-50_HT-2500 NoTau
python tools/DrawAnalyzeObjectStacks.py Run2016B-17Jul2018_ver2-v1.DoubleEG &
'''

try: fileskey = sys.argv[1].split('/')[-1]
except: fileskey = 'DYJetsToLL_M-50_HT-2500'


if 'T5' in fileskey or 'T6' in fileskey: dosignals = True
else: dosignals = False

#eosls /store/group/lpcsusyphotons/TreeMakerRandS_signalskimsv8 > usefulthings/filelistDiphotonSignalSkims.txt
if dosignals: eosdir = '/store/group/lpcsusyphotons/TreeMakerRandS_signalskimsv8'
else: eosdir = '/store/group/lpcsusyphotons/TreeMakerRandS_skimsv9'


print 'fileskey', fileskey
if 'Run20' in fileskey: isdata = True
else: isdata = False


universalconstraint = ' abs(HardMetMinusMet)<100 && mva_Photons1Et>80 && mva_Ngoodjets>1 | (abs(analysisPhotons[0].Eta())<1.5 && abs(analysisPhotons[1].Eta())<1.5) && IsRandS==0 && analysisPhotons_passWp[0]==1 && analysisPhotons_passWp[1]==1'

print dosignals

if dosignals: filefile = open('usefulthings/filelistDiphotonSignalSkimsv9.txt')
else: filefile = open('usefulthings/filelistDiphotonSkims.txt')
fins = filefile.readlines()
    
if not isdata:
    ccounter = TChain('tcounter')
    for fname in fins:
        if not fileskey in fname: continue
        thing2add = 'root://cmseos.fnal.gov/'+eosdir+'/'+fname.strip()
        print 'trying to add to ccounter', thing2add.strip()
        ccounter.Add(thing2add)
    nev_total = ccounter.GetEntries()
    print 'nevents in total =', nev_total

    
chain = TChain('TreeMaker2/PreSelection')
print 'fileskey', fileskey
for fname in fins:
    if not fileskey in fname: continue
    thing2add = 'root://cmseos.fnal.gov/'+eosdir+'/'+fname.strip()
    print 'trying to add to chain', thing2add
    chain.Add(thing2add)
chain.Show(0)
print 'nevents in skim =', chain.GetEntries()


#chain.SetBranchStatus('NJets', 1)
#chain.SetBranchStatus('HT', 1)
#chain.SetBranchStatus('BTags', 1)
#chain.SetBranchStatus('Jets', 1)

if isdata: evtweight = '1'
else: evtweight = 'CrossSection/'+str(nev_total)


plotBundle = {}




#plotBundle['SignalRegionTwoPho_HardMet'] = ['min(HardMETPt,499)>>hadc(74,130,500)','HardMETPt>130 && NPhotons>=2 && mva_BDT>-0.26',False]
#plotBundle['TwoPho_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_LeadPhotonPt'] = ['min(analysisPhotons[0].Pt(),559)>>hadc(24,60,560)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_TrailPhotonPt'] = ['min(analysisPhotons[1].Pt(),559)>>hadc(24,60,560)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_LeadPhotonEta'] = ['analysisPhotons[0].Eta()>>hadc(24,-2.4,2.4)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_TrailPhotonEta'] = ['analysisPhotons[1].Eta()>>hadc(24,-2.4,2.4)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_LeadPhotonSieie'] = ['min(analysisPhotons_sieie[0],0.0199)>>hadc(24,0,0.02)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_TrailPhotonSieie'] = ['min(analysisPhotons_sieie[1],0.0199)>>hadc(24,0,0.02)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_LeadPhotonHoe'] = ['min(analysisPhotons_hoe[0],0.099)>>hadc(24,0,0.05)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_TrailPhotonHoe'] = ['min(analysisPhotons_hoe[1],0.099)>>hadc(24,0,0.05)','HardMETPt>130 && NPhotons>=2',False]

plotBundle['TwoPho_HardMet'] = ['HardMETPt>>hadc(20,120,520)','NPhotons>=2',False]
plotBundle['TwoPho_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>130  && NPhotons>=2',False]
plotBundle['TwoPho_massGG'] = ['mass_GG>>hadc(20,0,400)','HardMETPt>130  && NPhotons>=2',False]
plotBundle['TwoPho_mva_BDT'] = ['mva_BDT>>hadc(20,-1.2,1.2)','HardMETPt>130  && NPhotons>=2',False]    

plotBundle['TwoPho_mva_dPhi_GGHardMET'] = ['mva_dPhi_GGHardMET>>hadc(18,0,3.2)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_mva_DPhi_GG'] = ['mva_dPhi_GG>>hadc(18,0,3.2)','HardMETPt>130 && NPhotons>=2',False]    
plotBundle['BasleineTwoPho_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(18,0,3.2)','HardMETPt>130 && NPhotons>=2',False]    
    
    
    
categories = {}
categories['#geq 1 #gamma is #mu'] = ['(analysisPhotons_isGenMu[0]==1 || analysisPhotons_isGenMu[1]==1)', kViolet]
categories['#gamma/#gamma'] = ['(analysisPhotons_isGenPho[0]==1 && analysisPhotons_isGenPho[1]==1)', kOrange]
categories['#gamma/e'] = ['((analysisPhotons_isGenPho[0]==1 && analysisPhotons_isGenEle[1]==1) || (analysisPhotons_isGenPho[1]==1 && analysisPhotons_isGenEle[0]==1))',kTeal-5]
categories['#gamma/jet'] = ['((analysisPhotons_isGenPho[0]==1 && analysisPhotons_isGenNone[1]==1) || (analysisPhotons_isGenNone[1]==1 && analysisPhotons_isGenPho[0]==1))', kBlue+1]
categories['e/jet'] = ['((analysisPhotons_isGenEle[0]==1 && analysisPhotons_isGenNone[1]==1) || (analysisPhotons_isGenEle[1]==1 && analysisPhotons_isGenNone[0]==1))', kViolet+1]
categories['e/e'] = ['(analysisPhotons_isGenEle[0]==1 && analysisPhotons_isGenEle[1]==1)', kGray+2]
categories['jet/jet'] = ['(analysisPhotons_isGenNone[0]==1 && analysisPhotons_isGenNone[1]==1)',kGray]


thakeys = ['e/jet','jet/jet','e/e','#gamma/#gamma','#gamma/jet','#gamma/e'] 
#thakeys.reverse()
#categories['#geq 1 #gamma is #mu'] = ['analysisPhotons_isGenMu[0]==1 || analysisPhotons_isGenMu[1]==1 ']
#categories['#geq 1 #gamma is #mu'] = ['analysisPhotons_isGenMu[0]==1 || analysisPhotons_isGenMu[1]==1 ']



print 'fileskey', fileskey
infilekey = fileskey.split('/')[-1].replace('*','').replace('.root','')
newfilename = 'output/mediumchunks/componentHists_'+infilekey+'.root'
if 'T5' in infilekey or 'T6' in infilekey: newfilename = newfilename.replace('mediumchunks','signals')

    
fnew = TFile(newfilename, 'recreate')
print 'will make file', fnew.GetName()
c1 = mkcanvas()
c2 = mkcanvas('c2')

for key in plotBundle:
    drawarg, constraint, blinding = plotBundle[key]
    obsweight = evtweight+'*('+constraint + ' && '+ universalconstraint + ')'
    #puWeight
    print 'drawing', drawarg, ', with constraint:', obsweight
    chain.Draw(drawarg,obsweight, 'e')
    hobs = chain.GetHistogram().Clone(key+'_obs')
    hobs.Scale(lumi*1000)
    c1.cd()
    hcomponents = []
    for ic, component in enumerate(thakeys):
        
        catconst, color = categories[component]
        drawarg = drawarg
        cobsweight = evtweight+'*('+constraint +' && ' + catconst + ' && '+ universalconstraint + ')'
        chain.Draw(drawarg, cobsweight, 'e')
        hcomp = chain.GetHistogram().Clone(key+'_'+component) 
        histoStyler(hcomp, color)
        hcomp.SetFillStyle(1001)
        hcomp.SetFillColor(hcomp.GetLineColor())
        hcomp.SetTitle(component)
        hcomp.Scale(lumi*1000)
        hcomponents.append(hcomp)

    leg = mklegend(x1=.71, y1=.3, x2=.98, y2=.8, color=kWhite)
    hobs.SetTitle('MC (WG)')
    hobs.GetXaxis().SetTitle(key.split('TwoPho_')[-1].split('mva_')[-1])
    hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,hobs,hcomponents,datamc='MC',lumi=str(lumi), title = '', LinearScale=False, fractionthing='total / component')
    if not ('Vs' in key): 
    	hobs.GetYaxis().SetRangeUser(0.01,100*hobs.GetMaximum())
    	for h in hcomponents: h.GetYaxis().SetRangeUser(0.001,10*hobs.GetMaximum())
    c1.Update()
    c1.Write('c_'+key)
    c1.Print('pdfs/Components/'+key+'.png')        



print 'just created', fnew.GetName()
fnew.Close()

