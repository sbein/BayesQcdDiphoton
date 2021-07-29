import os, sys
from ROOT import *
from utils import *
from glob import glob
gROOT.SetBatch(1)
gStyle.SetOptStat(0)

dopred = False

'''
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_skimsv5/*Summer16v3.DYJetsToLL_M-50_HT-2500*.root" NoTau
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_skimsv5/*Run2016B-17Jul2018_ver2-v1.DoubleEG*" &
'''

try: fileskey = sys.argv[1]
except: fileskey = '/eos/uscms//store/user/sbein/RebalanceAndSmear/Run2ProductionV17/*Summer16v3.QCD*.root'


print 'fileskey', fileskey
if 'Run20' in fileskey: isdata = True
else: isdata = False

    
try: SpecialSettings = ''.join(sys.argv[2:])
except: SpecialSettings =  ''

if 'NoTau' in SpecialSettings: taustring = "&& @GenTaus.size()==0"
elif 'WithTau' in SpecialSettings: taustring = "&& @GenTaus.size()>0"
else: taustring = ""

if 'TwoPixelSeeds' in SpecialSettings: pixelseedstring = "&& (Pho1_hasPixelSeed==1 && Pho2_hasPixelSeed==1)"
else: pixelseedstring = "&& (Pho1_hasPixelSeed==0 && Pho2_hasPixelSeed==0)"

if 'TwoShowerShapeFail' in SpecialSettings: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta==0 && Pho2_passLooseSigmaIetaIeta==0)"
elif 'OneShowerShapeFail' in SpecialSettings: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta + Pho2_passLooseSigmaIetaIeta==1)"
elif 'FirstShowerShapeFail' in SpecialSettings: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta==0 && Pho2_passLooseSigmaIetaIeta==1)"
elif 'SecondShowerShapeFail' in SpecialSettings: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta==1 && Pho2_passLooseSigmaIetaIeta==0)"
elif 'AgnosticShowerShape' in SpecialSettings: showershapestring = ''
else: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta + Pho2_passLooseSigmaIetaIeta==2)"

print 'SpecialSettings:', SpecialSettings, showershapestring
#exit(0)


universalconstraint = ' abs(HardMetMinusMet)<100 && mva_Photons1Et>80 && mva_Ngoodjets>1 && (abs(analysisPhotons[0].Eta())<1.5 || abs(analysisPhotons[1].Eta())<1.5)'+taustring + showershapestring
universalconstraint += taustring
universalconstraint += pixelseedstring


fins = glob(fileskey)
if not isdata:
    ccounter = TChain('tcounter')
    for fname in fins: ccounter.Add(fname.replace('/eos/uscms/','root://cmseos.fnal.gov//'))
    nev_total = ccounter.GetEntries()
    print 'nevents in total =', nev_total
    
chain = TChain('TreeMaker2/PreSelection')
print 'fileskey', fileskey
for fname in fins: chain.Add(fname.replace('/eos/uscms/','root://cmseos.fnal.gov//'))
chain.Show(0)
print 'nevents in skim =', chain.GetEntries()

#chain.SetBranchStatus('NJets', 1)
#chain.SetBranchStatus('HT', 1)
#chain.SetBranchStatus('BTags', 1)
#chain.SetBranchStatus('Jets', 1)

if isdata: evtweight = '1'
else: evtweight = 'CrossSection/'+str(nev_total)



promptname = 'Photons_nonPrompt'
#promptname = 'Photons_genMatched'
WP = 'Medium/2'
WP = 'Loose'



plotBundle = {}


#2d plots
'''
#plotBundle['TwoPho_EtaVsPhi'] = ['Photons[0].Eta():Photons[0].Phi()>>hadc(320,-3.2,3.2,320,-3.2,3.2)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_Pho1EtaVsPhi'] = ['Photons[0].Eta():Photons[0].Phi()>>hadc(160,-3.2,3.2,160,-3.2,3.2)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_Jet1EtaVsPhi'] = ['JetsAUX[0].Eta():JetsAUX[0].Phi()>>hadc(160,-3.2,3.2,160,-3.2,3.2)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPho_Jet2EtaVsPhi'] = ['JetsAUX[1].Eta():JetsAUX[1].Phi()>>hadc(160,-3.2,3.2,160,-3.2,3.2)','HardMETPt>130 && NPhotons>=2',False]
plotBundle['TwoPhoHighMet_Jet1EtaVsPhi'] = ['JetsAUX[0].Eta():JetsAUX[0].Phi()>>hadc(160,-3.2,3.2,160,-3.2,3.2)','HardMETPt>250 && NPhotons>=2',False]
plotBundle['TwoPhoHighMet_Jet2EtaVsPhi'] = ['JetsAUX[1].Eta():JetsAUX[1].Phi()>>hadc(160,-3.2,3.2,160,-3.2,3.2)','HardMETPt>250 && NPhotons>=2',False]
plotBundle['TwoPho_HardMETPhi'] = ['HardMETPhi>>hadc(32,0,3.2)','HardMETPt>130 && NPhotons>=2',False]
'''

#SR plots
if False and not ('SR' in SpecialSettings or 'Agnostic' in SpecialSettings):
    plotBundle['TwoPho_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_HardMet'] = ['min(HardMETPt,499)>>hadchadc(74,130,500)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_massGG'] = ['mass_GG>>hadc(80,0,400)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_Pho1Pt'] = ['mva_Photons0Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_Pho2Pt'] = ['mva_Photons1Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_mva_Pt_GG'] = ['mva_Pt_GG>>hadc(10,0,750)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_mva_ST_jets'] = ['mva_ST_jets>>hadc(16,0,800)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_mva_BDT'] = ['mva_BDT>>hadc(12,-1.2,1.2)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_mva_dPhi_GGHardMET'] = ['mva_dPhi_GGHardMET>>hadc(18,-3.6,3.6)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_mva_DPhi_GG'] = ['mva_dPhi_GG>>hadc(18,-3.6,3.6)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_mva_ST'] = ['mva_ST>>hadc(10,100,2300)','HardMETPt>130 && NPhotons>=2',False]
    
    plotBundle['TwoPhoHighMet_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>300 && NPhotons>=2',False]
    plotBundle['TwoPhoHighMet_massGG'] = ['mass_GG>>hadc(80,0,400)','HardMETPt>300 && NPhotons>=2',False]
    plotBundle['TwoPhoHighMet_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>300 && NPhotons>=2',False]
    plotBundle['TwoPhoHighMet_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(16,0,3.2)','HardMETPt>300 && NPhotons>=2',False]
    plotBundle['TwoPhoHighMet0b_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>300 && NPhotons>=2 && BTagsAUX==0',False]
    plotBundle['TwoPhoHighMet0b_massGG'] = ['mass_GG>>hadc(80,0,400)','HardMETPt>300 && NPhotons>=2 && BTagsAUX==0',False]
    plotBundle['TwoPhoHighMet0b_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>300 && NPhotons>=2 && BTagsAUX==0',False]
    plotBundle['TwoPhoHighMet0b_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(16,0,3.2)','HardMETPt>300 && NPhotons>=2 && BTagsAUX==0',False]
    plotBundle['TwoPhoOnZ_HardMet'] = ['min(HardMETPt,499)>>hadc(20,120,620)','HardMETPt>130 && NPhotons>=2 && abs(mass_GG-91)<10',False]
    plotBundle['TwoPhoOnZ_BTags'] = ['BTagsAUX>>hadc(6,0,6)','HardMETPt>130 && NPhotons>=2 && abs(mass_GG-91)<10',False]    
    plotBundle['TwoPhoOnZ_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>130 && NPhotons>=2 && abs(mass_GG-91)<10',False]
    plotBundle['TwoPhoOnZLDP_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>130 && NPhotons>=2 && abs(mass_GG-91)<10  && mva_min_dPhi<0.5',False]
    plotBundle['TwoPhoOnZLDP_BTags'] = ['BTagsAUX>>hadc(6,0,6)','HardMETPt>130 && NPhotons>=2 && abs(mass_GG-91)<10  && mva_min_dPhi<0.5',False]    
    plotBundle['TwoPhoOffZ_HardMet'] = ['min(HardMETPt,499)>>hadc(20,120,620)','HardMETPt>130 && NPhotons>=2 && abs(mass_GG-91)>10',False]
    plotBundle['TwoPhoOffZ_BTags'] = ['BTagsAUX>>hadc(6,0,6)','HardMETPt>130 && NPhotons>=2 && abs(mass_GG-91)>10',False]    
    plotBundle['TwoPhoOffZ_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>130 && NPhotons>=2 && abs(mass_GG-91)>10',False]

if 'SR' in SpecialSettings:
    plotBundle['SignalRegionTwoPho_HardMet'] = ['min(HardMETPt,499)>>hadc(74,130,500)','HardMETPt>130 && NPhotons>=2 && mva_BDT>-0.26',False]
    plotBundle['TwoPho_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>130 && NPhotons>=2',False]


#plotBundle['TwoPhoFailsieieta2_SigmaIetaIeta1'] = ['Photons_sigmaIetaIeta[0]>>hadc(20,0,0.1)','HardMETPt>130 && NPhotons>=2 && Pho2_passLooseSigmaIetaIeta==0',False]
#plotBundle['TwoPhoFailsieieta1_SigmaIetaIeta2'] = ['Photons_sigmaIetaIeta[1]>>hadc(20,0,0.1)','HardMETPt>130 && NPhotons>=2 && Pho1_passLooseSigmaIetaIeta==0',False]

plotBundle['TwoPhoLDP_SigmaIetaIeta1'] = ['Photons_sigmaIetaIeta[0]>>hadc(20,0,0.1)','HardMETPt>130 && NPhotons>=2  && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_SigmaIetaIeta2'] = ['Photons_sigmaIetaIeta[1]>>hadc(20,0,0.1)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]


#LDP plots
plotBundle['TwoPhoLDP_HardMet'] = ['min(HardMETPt,499)>>hadchadc(74,130,500)','NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(16,0,3.2)','HardMETPt>130 && NPhotons>=2',False]##this appears twice
plotBundle['TwoPhoLDP_massGG'] = ['mass_GG>>hadc(20,0,400)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_Pho1Pt'] = ['mva_Photons0Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_Pho2Pt'] = ['mva_Photons1Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_mva_Pt_GG'] = ['mva_Pt_GG>>hadc(10,0,750)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_mva_ST_jets'] = ['mva_ST_jets>>hadc(16,0,800)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_mva_BDT'] = ['mva_BDT>>hadc(24,-1.2,1.2)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_mva_dPhi_GGHardMET'] = ['mva_dPhi_GGHardMET>>hadc(18,-3.6,3.6)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_mva_DPhi_GG'] = ['mva_dPhi_GG>>hadc(18,-3.6,3.6)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
plotBundle['TwoPhoLDP_mva_ST'] = ['mva_ST>>hadc(10,100,2300)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
#plotBundle['TwoPhoLDP_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
#plotBundle['TwoPhoLDP_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]


if 'SR' in SpecialSettings and True:
    plotBundle['TwoPhoLowBDT_HardMet'] = ['HardMETPt>>hadchadc(74,130,500)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.26',False]
    plotBundle['TwoPhoLowBDT_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>130  && NPhotons>=2 && mva_BDT<-0.26',False]
    plotBundle['TwoPhoLowBDT_massGG'] = ['mass_GG>>hadc(80,0,400)','HardMETPt>130  && NPhotons>=2 && mva_BDT<-0.26',False]
    plotBundle['TwoPhoLowBDT_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_BDT<-0.26',False]
    plotBundle['TwoPhoLowBDT_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_BDT<-0.26',False]    
    plotBundle['TwoPhoLowBDT_Pho1Pt'] = ['mva_Photons0Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.26',False]
    plotBundle['TwoPhoLowBDT_Pho2Pt'] = ['mva_Photons1Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.26',False]
    plotBundle['TwoPhoLowBDT_mva_Pt_GG'] = ['mva_Pt_GG>>hadc(10,0,750)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.26',False]
    plotBundle['TwoPhoLowBDT_mva_ST_jets'] = ['mva_ST_jets>>hadc(16,0,800)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.26',False]
    plotBundle['TwoPhoLowBDT_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(16,0,3.2)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.26',False]
    

if 'Summer' in fileskey and False:
    plotBundle['TwoPhoHDP_HardMet'] = ['HardMETPt>>hadc(74,130,500)','NPhotons>=2 && mva_min_dPhi>0.3',False]
    plotBundle['TwoPhoHDP_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>130  && NPhotons>=2 && mva_min_dPhi>0.3',False]
    plotBundle['TwoPhoHDP_massGG'] = ['mass_GG>>hadc(80,0,400)','HardMETPt>130  && NPhotons>=2 && mva_min_dPhi>0.3',False]
    plotBundle['TwoPhoHDP_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_min_dPhi>0.3',False]
    plotBundle['TwoPhoHDP_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_min_dPhi>0.3',False]
    plotBundle['TwoPhoHDP_mva_BDT'] = ['mva_BDT>>hadc(12,-1.2,1.2)','HardMETPt>130  && NPhotons>=2 && mva_min_dPhi>0.3',False]
    plotBundle['TwoPhoHDP_dPhi_GGHardMET'] = ['mva_dPhi_GGHardMET>>hadc(18,-3.6,3.6)','HardMETPt>130  && NPhotons>=2 && mva_min_dPhi>0.3',False]    

    plotBundle['TwoPho_HardMet'] = ['HardMETPt>>hadc(20,120,520)','NPhotons>=2',False]
    plotBundle['TwoPho_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>130  && NPhotons>=2',False]
    plotBundle['TwoPho_massGG'] = ['mass_GG>>hadc(80,0,400)','HardMETPt>130  && NPhotons>=2',False]
    plotBundle['TwoPho_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2',False]
    plotBundle['TwoPho_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2',False]
    plotBundle['TwoPho_mva_BDT'] = ['mva_BDT>>hadc(12,-1.2,1.2)','HardMETPt>130  && NPhotons>=2',False]    

    plotBundle['TwoPho_mva_dPhi_GGHardMET'] = ['mva_dPhi_GGHardMET>>hadc(18,-3.6,3.6)','HardMETPt>130 && NPhotons>=2',False]
    plotBundle['TwoPho_mva_DPhi_GG'] = ['mva_dPhi_GG>>hadc(18,-3.6,3.6)','HardMETPt>130 && NPhotons>=2',False]    
    plotBundle['BasleineTwoPho_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(18,-0.2,3.4)','HardMETPt>130 && NPhotons>=2',False]    

    


print 'fileskey', fileskey
infilekey = fileskey.split('/')[-1].replace('*','').replace('.root','')
newfilename = 'output/mediumchunks/weightedHists_'+infilekey+'_'+SpecialSettings+'.root'
if 'T5' in infilekey or 'T6' in infilekey: newfilename = newfilename.replace('mediumchunks','signals')

    
fnew = TFile(newfilename, 'recreate')
print 'will make file', fnew.GetName()
c1 = mkcanvas()
c2 = mkcanvas('c2')

for key in plotBundle:
    drawarg, constraint, blinding = plotBundle[key]
    obsweight = evtweight+'*('+constraint + ' && '+ universalconstraint + ' && IsRandS==0)'
    #puWeight
    print 'drawing', drawarg, ', with constraint:', obsweight
    chain.Draw(drawarg,obsweight, 'e')
    hobs = chain.GetHistogram().Clone(key+'_obs')
    if not ('Vs' in key): hobs.GetYaxis().SetRangeUser(0.01,10000*hobs.GetMaximum())

    c1.cd()

    drawarg = drawarg
    randsconstraint = constraint
    methweight = evtweight+'/NSmearsPerEvent*('+ randsconstraint + ' && '+universalconstraint+ ' && IsRandS==1 && rebalancedHardMet<120)'
    #puWeight
    print 'drawing', drawarg, ', with constraint:', methweight
    chain.Draw(drawarg, methweight, 'e')
    hrands = chain.GetHistogram().Clone(key+'_rands') 
    if blinding and 'Run20' in fileskey: hobs = hrands.Clone(key+'_obs')
    if not ('Vs' in drawarg): hrands.GetYaxis().SetRangeUser(0.01,10000*hrands.GetMaximum())
    if 'ZGG' in fileskey: histoStyler(hrands, kViolet+1)
    else: histoStyler(hrands, kAzure-8)
    hrands.SetFillColor(hrands.GetLineColor())
    hrands.SetFillStyle(1001)

    leg = mklegend(x1=.45, y1=.57, x2=.95, y2=.74, color=kWhite)
    if 'ZGG' in fileskey: hobs.SetTitle('Summer16 ZGG')
    else: hobs.SetTitle('observed')
    hobs.GetXaxis().SetTitle(key.split('_')[-1])
    hrands.GetXaxis().SetTitle(key.split('_')[-1])
    hrands.SetTitle('rebalance and smeared')
    if dopred: 
        hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,hobs,[hrands],datamc='MC',lumi='n/a', title = '', LinearScale=False, fractionthing='observed / method')
        c1.Update()
        c1.Write('c_'+key)
        c1.Print('pdfs/Closure/'+key+'.pdf')        
    hrands.Write('h'+hrands.GetName())
    hobs.Write('h'+hobs.GetName())
    print sys.argv





print 'just created', fnew.GetName()
fnew.Close()

