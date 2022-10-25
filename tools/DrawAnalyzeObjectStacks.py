
import os, sys
from ROOT import *
from utils import *
gROOT.SetBatch(1)
gStyle.SetOptStat(0)
lumi = 36
dopred = False
wp = 'Medium'
wp = 'Loose'

'''
eosls /store/group/lpcsusyphotons/Skims_medPhotonElVetoV10/ > usefulthings/filelistDiphotonSkims.txt
eosls /store/group/lpcsusyphotons/Skims_loosePhotonV10FullId/ > usefulthings/filelistDiphotonSkims.txt

python tools/DrawAnalyzeObjectStacks.py Run2016B-17Jul2018_ver2-v1.DoubleEG &
python tools/DrawAnalyzeObjectStacks.py Summer16v3.WGJets_MonoPhoton_PtG-130
'''

try: fileskey = sys.argv[1].split('/')[-1]
except: fileskey = 'DYJetsToLL_M-50_HT-2500'


if 'T5' in fileskey or 'T6' in fileskey: dosignals = True
else: dosignals = False

#eosls /store/group/lpcsusyphotons/TreeMakerRandS_signalskimsv8 > usefulthings/filelistDiphotonSignalSkims.txt
if dosignals: eosdir = '/store/group/lpcsusyphotons/Skims_loosePhotonSignalsV8'
else: eosdir = '/store/group/lpcsusyphotons/Skims_loosePhotonV10FullId/'


print 'fileskey', fileskey
if 'Run20' in fileskey: isdata = True
else: isdata = False


universalconstraint = 'HardMETPt>130  && NPhotons>=2 && abs(HardMetMinusMet)<100 && mva_Photons1Et>80 && mva_Ngoodjets>1 && (abs(analysisPhotons[0].Eta())<1.5 || abs(analysisPhotons[1].Eta())<1.5) && analysisPhotons_minDrRecEle[0]>0.1 && analysisPhotons_minDrRecEle[1]>0.1 && NMuons==0 && IsRandS==0'

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


variables = {}
variables['LeadPhotonPt']  = 'min(analysisPhotons[0].Pt(),559)>>hadc(24,60,560)'
variables['TrailPhotonPt']  = 'min(analysisPhotons[1].Pt(),559)>>hadc(24,60,560)'
variables['LeadPhotonEta']  = 'analysisPhotons[0].Eta()>>hadc(24,-2.4,2.4)'
variables['TrailPhotonEta']  = 'analysisPhotons[1].Eta()>>hadc(24,-2.4,2.4)'
variables['LeadPhotonSieie']  = 'min(analysisPhotons_sieie[0],0.0199)>>hadc(24,0,0.02)'
variables['TrailPhotonSieie']  = 'min(analysisPhotons_sieie[1],0.0199)>>hadc(24,0,0.02)'
variables['LeadPhotonHoe']  = 'min(analysisPhotons_hoe[0],0.099)>>hadc(24,0,0.05)'
variables['TrailPhotonHoe']  = 'min(analysisPhotons_hoe[1],0.099)>>hadc(24,0,0.05)'
variables['HardMet']  = 'HardMETPt>>hadc(20,120,520)'
#variables['LeadPhotonNonPrompt']  = 'Photons_nonPrompt[0]>>hadc(2,0,2)'
#variables['TrailPhotonNonPrompt']  = 'Photons_nonPrompt[1]>>hadc(2,0,2)'
variables['NGenMuons']  = '@GenMuons.size()>>hadc(3,0,3)'
variables['NGenElectrons']  = '@GenElectrons.size()>>hadc(3,0,3)'
variables['NRecMuons']  = '@Muons.size()>>hadc(3,0,3)'
variables['NRecElectrons']  = '@Electrons.size()>>hadc(3,0,3)'
variables['LeadPhotonMinDrGenEle']  = 'min(0.99,analysisPhotons_minDrGenEle[0])>>hadc(20,0,1)'
variables['TrailPhotonMinDrGenEle']  = 'min(0.99,analysisPhotons_minDrGenEle[1])>>hadc(20,0,1)'
variables['LeadPhotonMinDrRecEle']  = 'min(0.99,analysisPhotons_minDrRecEle[0])>>hadc(20,0,1)'
variables['TrailPhotonMinDrRecEle']  = 'min(0.99,analysisPhotons_minDrRecEle[1])>>hadc(20,0,1)'



#variables['NJets']  = 'mva_Ngoodjets>>hadc(12,-2,10)'
#variables['mva_BDT']  = 'mva_BDT>>hadc(20,-1.2,1.2)'

finalStates = {}
finalStates['PassPass'] = 'analysisPhotons_passWp[0]==1 && analysisPhotons_passWp[1]==1 && analysisPhotons_passWpInvertPsv[0]==0 && analysisPhotons_passWpInvertPsv[1]==0'
#finalStates['PassFail'] = '((analysisPhotons_passWp[0]==1 && analysisPhotons_passWp[1]==0) || (analysisPhotons_passWp[0]==0 && analysisPhotons_passWp[1]==1)) && analysisPhotons_passWpInvertPsv[0]==0 && analysisPhotons_passWpInvertPsv[1]==0'
#finalStates['PixNoPix'] = '((analysisPhotons_passWpInvertPsv[0]==1 && analysisPhotons_passWpInvertPsv[1]==0)||(analysisPhotons_passWpInvertPsv[0]==0 && analysisPhotons_passWpInvertPsv[1]==1))'
    
    
plotBundle = {}
for variable in variables:
    for finalState in finalStates:
        plotBundle[finalState+'_'+variable] = [variables[variable], finalStates[finalState], False]

    
categories = {}
categories['#geq 1 #gamma is #mu'] = ['(analysisPhotons_isGenMu[0]==1 || analysisPhotons_isGenMu[1]==1)', kViolet]
categories['#gamma/#gamma'] = ['(analysisPhotons_isGenPho[0]==1 && analysisPhotons_isGenPho[1]==1)', kOrange]
categories['#gamma/e'] = ['((analysisPhotons_isGenPho[0]==1 && analysisPhotons_isGenEle[1]==1) || (analysisPhotons_isGenPho[1]==1 && analysisPhotons_isGenEle[0]==1))',kTeal-5]
categories['#gamma/jet'] = ['((analysisPhotons_isGenPho[0]==1 && analysisPhotons_isGenNone[1]==1) || (analysisPhotons_isGenNone[1]==1 && analysisPhotons_isGenPho[0]==1))', kBlue+1]
categories['e/jet'] = ['((analysisPhotons_isGenEle[0]==1 && analysisPhotons_isGenNone[1]==1) || (analysisPhotons_isGenEle[1]==1 && analysisPhotons_isGenNone[0]==1))', kViolet+1]
categories['e/e'] = ['(analysisPhotons_isGenEle[0]==1 && analysisPhotons_isGenEle[1]==1)', kGray+2]
categories['jet/jet'] = ['(analysisPhotons_isGenNone[0]==1 && analysisPhotons_isGenNone[1]==1)',kGray]
categories['#gamma/#tau'] = ['((analysisPhotons_isGenPho[0]==1 && analysisPhotons_isGenTau[1]==1) || (analysisPhotons_isGenPho[1]==1 && analysisPhotons_isGenTau[0]==1))',kRed+1]


thakeys = ['#gamma/jet','e/jet','jet/jet','e/e','#gamma/#gamma','#gamma/#tau','#gamma/e'] 
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
        cobsweight = evtweight+'*('+constraint + ' && '+ universalconstraint +' && ' + catconst + ')'
        chain.Draw(drawarg, cobsweight, 'e')
        hcomp = chain.GetHistogram().Clone(key+'_'+component) 
        histoStyler(hcomp, color)
        hcomp.SetFillStyle(1001)
        hcomp.SetFillColor(hcomp.GetLineColor())
        hcomp.Scale(lumi*1000)        
        try: 
            frac = hcomp.Integral()/hobs.Integral()
            print component, 'got frac', frac
        except: frac = 0
        hcomp.SetTitle(component+' ('+str(round(frac,3))+')')
        hcomponents.append(hcomp)
    
    leg = mklegend(x1=.71, y1=.3, x2=.98, y2=.8, color=kWhite)
    hobs.SetTitle('MC (WG)')
    hobs.GetXaxis().SetTitle(key.split('PassPass_')[-1].split('PassFail_')[-1].split('PixNoPix_')[-1].split('mva_')[-1])
    hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,hobs,hcomponents,datamc='MC',lumi=str(lumi), title = '', LinearScale=False, fractionthing='total / component')
    if not ('Vs' in key): 
    	hobs.GetYaxis().SetRangeUser(0.01,100*hobs.GetMaximum())
    	for h in hcomponents: h.GetYaxis().SetRangeUser(0.001,10*hobs.GetMaximum())
    c1.Update()
    c1.Write('c_'+key)
    c1.Print('figures/Components'+wp+'/'+key+'.png')
    #c1.Print('pdfs/Components'+wp+'_vetoRecEle/'+key+'.png')



print 'just created', fnew.GetName()
fnew.Close()

