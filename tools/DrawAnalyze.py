
import os, sys
from ROOT import *
from utils import *
gROOT.SetBatch(1)
gStyle.SetOptStat(0)

dopred = False
doelveto = False##leave off because it's bubkik

#fullId = True
fullId = False

tryolder = False
BaseOnSavedGit = False

if BaseOnSavedGit: tryolder = True #switch this on by default
'''
python tools/DrawAnalyze.py Summer16v3.DYJetsToLL_M-50_HT-2500 NoTau
python tools/DrawAnalyze.py Run2016B-17Jul2018_ver2-v1.DoubleEG &

 analysisPhotons = (vector<TLorentzVector>*)0x801a3d0
 analysisPhotons_passWp = (vector<int>*)0x80331c0
 analysisPhotons_passWpNminus3 = (vector<int>*)0x8043140
 analysisPhotons_passWpInvertPsv = (vector<int>*)0x80530c0
 analysisPhotons_passWpInvertSieie = (vector<int>*)0x8063040
 analysisPhotons_passWpInvertHoe = (vector<int>*)0x8072fd0
 analysisPhotons_passWpInvertSieieAndHoe = (vector<int>*)0x8082f50
 analysisPhotons_hoe = (vector<double>*)0x8092ee0
 analysisPhotons_sieie = (vector<double>*)0x80a2e60
 analysisPhotons_hasPixelSeed = (vector<int>*)0x80b2de0
 analysisPhotons_isGenPho = (vector<int>*)0x80c2d60
 analysisPhotons_isGenEle = (vector<int>*)0x80d2ce0
 analysisPhotons_isGenMu = (vector<int>*)0x80e2c60
 analysisPhotons_isGenTau = (vector<int>*)0x80f2be0
 analysisPhotons_isGenNone = (vector<int>*)0x8102b60
 analysisPhotons_minDrGenEle = (vector<double>*)0x8112ae0
 analysisPhotons_minDrRecEle = (vector<double>*)0x8122a60
 
 #getting my head on right
 python tools/DrawAnalyze.py posterior-Summer16v3.GJets_DR-0p4_HT-600ToInf_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_102_RA2AnalysisTree_part1.root  SR
'''

try: fileskey = sys.argv[1].split('/')[-1]
except: fileskey = 'DYJetsToLL_M-50_HT-2500'


if 'T5' in fileskey or 'T6' in fileskey: dosignals = True
else: dosignals = False

#eosls /store/group/lpcsusyphotons/TreeMakerRandS_signalskimsv8 > usefulthings/filelistDiphotonSignalSkims.txt
if dosignals: eosdir = '/store/group/lpcsusyphotons/TreeMakerRandS_signalskimsv8'
else: 
    if doelveto: eosdir = '/store/group/lpcsusyphotons/Skims_medPhotonElVetoV10'
    else: eosdir = '/store/group/lpcsusyphotons/Skims_medPhotonNoElVetoV10'
    if tryolder: eosdir = '/store/group/lpcsusyphotons/Skims_loosePhotonV8'
    if BaseOnSavedGit: eosdir = '/store/group/lpcsusyphotons/Skims_Git18Apr2022'
    if fullId: eosdir = '/store/group/lpcsusyphotons/Skims_loosePhotonV10bFullId'
    
'''
eosls /store/group/lpcsusyphotons/Skims_medPhotonElVetoV10/ > usefulthings/filelistDiphotonSkimsV10.txt
eosls /store/group/lpcsusyphotons/Skims_medPhotonNoElVetoV10/ > usefulthings/filelistDiphotonSkimsV10NoElVeto.txt
eosls /store/group/lpcsusyphotons/Skims_loosePhotonV10bFullId > usefulthings/filelistDiphoton_loosePhotonV10bFullId.txt
'''


print ('fileskey', fileskey)
if 'Run20' in fileskey: isdata = True
else: isdata = False


isdata = True

try: SpecialSettings = ''.join(sys.argv[2:])
except: SpecialSettings =  ''

if 'NoTau' in SpecialSettings: taustring = "&& @GenTaus.size()==0"
elif 'WithTau' in SpecialSettings: taustring = "&& @GenTaus.size()>0"
else: taustring = ""

if 'TwoPixelSeeds' in SpecialSettings: pixelseedstring = "&& (analysisPhotons_hasPixelSeed[0]==1 && analysisPhotons_hasPixelSeed[1]==1)"
else: 
    if tryolder: pixelseedstring = "&& (Pho1_hasPixelSeed==0 && Pho2_hasPixelSeed==0)"
    else: pixelseedstring = "&& (analysisPhotons_hasPixelSeed[0]==0 && analysisPhotons_hasPixelSeed[1]==0)"

if 'TwoShowerShapeFail' in SpecialSettings: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta==0 && Pho2_passLooseSigmaIetaIeta==0)"
elif 'OneShowerShapeFail' in SpecialSettings: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta + Pho2_passLooseSigmaIetaIeta==1)"
elif 'FirstShowerShapeFail' in SpecialSettings: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta==0 && Pho2_passLooseSigmaIetaIeta==1)"
elif 'SecondShowerShapeFail' in SpecialSettings: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta==1 && Pho2_passLooseSigmaIetaIeta==0)"
elif 'AgnosticShowerShape' in SpecialSettings: showershapestring = ''
else: 
    if tryolder: showershapestring = "&& (Pho1_passLooseSigmaIetaIeta + Pho2_passLooseSigmaIetaIeta==2)"
    else: showershapestring = "&& (analysisPhotons_passWp[0]==1 && analysisPhotons_passWp[1]==1)"

print ('SpecialSettings:', SpecialSettings, showershapestring)
#exit(0)


universalconstraint = ' abs(HardMetMinusMet)<100 && mva_Photons1Et>80 && mva_Ngoodjets>1 && (abs(analysisPhotons[0].Eta())<1.5 || abs(analysisPhotons[1].Eta())<1.5)'+ showershapestring
universalconstraint += taustring
universalconstraint += pixelseedstring

print (dosignals)

if dosignals: filefile = open('usefulthings/filelistDiphotonSignalSkims.txt')
else: 
    if doelveto: filefile = open('usefulthings/filelistDiphotonSkimsV10.txt')
    else: filefile = open('usefulthings/filelistDiphotonSkimsV10NoElVeto.txt')
    if tryolder: filefile = open('usefulthings/filelistDiphotonSkimsv8.txt')
    if fullId: filefile = open('usefulthings/filelistDiphoton_loosePhotonV10bFullId.txt')
    
fins = filefile.readlines()
    
if not isdata:
    ccounter = TChain('tcounter')
    for fname in fins:
        if not fileskey in fname: continue
        thing2add = 'root://cmseos.fnal.gov/'+eosdir+'/'+fname.strip()
        print ('trying to add to ccounter', thing2add.strip())
        ccounter.Add(thing2add)
    nev_total = ccounter.GetEntries()
    print ('nevents in total =', nev_total)

    
chain = TChain('TreeMaker2/PreSelection')
print ('fileskey', fileskey)
for fname in fins:
    if not fileskey in fname: continue
    thing2add = 'root://cmseos.fnal.gov/'+eosdir+'/'+fname.strip()
    print ('trying to add to chain', thing2add)
    chain.Add(thing2add)
chain.Show(0)
print ('nevents in skim =', chain.GetEntries())


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
if not ('SR' in SpecialSettings or 'Agnostic' in SpecialSettings):
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
'''
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
'''

#plotBundle['TwoPhoLDP_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]
#plotBundle['TwoPhoLDP_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130 && NPhotons>=2 && mva_min_dPhi<0.5',False]


if 'SR' in SpecialSettings and True:
    plotBundle['TwoPhoLowBDT_HardMet'] = ['min(499,HardMETPt)>>hadchadc(74,130,500)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.13',False]
    plotBundle['TwoPhoLowBDT_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>130  && NPhotons>=2 && mva_BDT<-0.13',False]
    plotBundle['TwoPhoLowBDT_massGG'] = ['mass_GG>>hadc(80,0,400)','HardMETPt>130  && NPhotons>=2 && mva_BDT<-0.13',False]
    #plotBundle['TwoPhoLowBDT_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_BDT<-0.13',False]
    #plotBundle['TwoPhoLowBDT_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_BDT<-0.13',False]    
    #plotBundle['TwoPhoLowBDT_Pho1Pt'] = ['mva_Photons0Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.13',False]
    #plotBundle['TwoPhoLowBDT_Pho2Pt'] = ['mva_Photons1Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.13',False]
    #plotBundle['TwoPhoLowBDT_mva_Pt_GG'] = ['mva_Pt_GG>>hadc(10,0,750)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.13',False]
    #plotBundle['TwoPhoLowBDT_mva_ST_jets'] = ['mva_ST_jets>>hadc(16,0,800)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.13',False]
    #plotBundle['TwoPhoLowBDT_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(16,0,3.2)','HardMETPt>130 && NPhotons>=2 && mva_BDT<-0.13',False]

    plotBundle['TwoPhoMidBDT_HardMet'] = ['min(499,HardMETPt)>>hadchadc(74,130,500)','HardMETPt>130 && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]
    plotBundle['TwoPhoMidBDT_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>130  && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]
    plotBundle['TwoPhoMidBDT_massGG'] = ['mass_GG>>hadc(80,0,400)','HardMETPt>130  && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoMidBDT_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoMidBDT_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]    
    #plotBundle['TwoPhoMidBDT_Pho1Pt'] = ['mva_Photons0Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoMidBDT_Pho2Pt'] = ['mva_Photons1Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoMidBDT_mva_Pt_GG'] = ['mva_Pt_GG>>hadc(10,0,750)','HardMETPt>130 && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoMidBDT_mva_ST_jets'] = ['mva_ST_jets>>hadc(16,0,800)','HardMETPt>130 && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoMidBDT_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(16,0,3.2)','HardMETPt>130 && NPhotons>=2 && mva_BDT>=-0.13 && mva_BDT<0.03',False]

    plotBundle['TwoPhoHighBDT_HardMet'] = ['min(499,HardMETPt)>>hadchadc(74,130,500)','HardMETPt>130 && NPhotons>=2 && mva_BDT>0.03',False]
    plotBundle['TwoPhoHighBDT_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>130  && NPhotons>=2 && mva_BDT>0.03',False]
    plotBundle['TwoPhoHighBDT_massGG'] = ['mass_GG>>hadc(80,0,400)','HardMETPt>130  && NPhotons>=2 && mva_BDT>0.03',False]
    #plotBundle['TwoPhoHighBDT_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_BDT>0.03 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoHighBDT_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>130  && NPhotons>=2 && mva_BDT>0.03 && mva_BDT<0.03',False]    
    #plotBundle['TwoPhoHighBDT_Pho1Pt'] = ['mva_Photons0Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_BDT>0.03 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoHighBDT_Pho2Pt'] = ['mva_Photons1Et>>hadc(10,50,1050)','HardMETPt>130 && NPhotons>=2 && mva_BDT>0.03 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoHighBDT_mva_Pt_GG'] = ['mva_Pt_GG>>hadc(10,0,750)','HardMETPt>130 && NPhotons>=2 && mva_BDT>0.03 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoHighBDT_mva_ST_jets'] = ['mva_ST_jets>>hadc(16,0,800)','HardMETPt>130 && NPhotons>=2 && mva_BDT>0.03 && mva_BDT<0.03',False]
    #plotBundle['TwoPhoHighBDT_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(16,0,3.2)','HardMETPt>130 && NPhotons>=2 && mva_BDT>0.03 && mva_BDT<0.03',False]      
    

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

plotBundle = {}
plotBundle['TwoPho_MinMt'] = ['min(MinMt,499)>>hadchadc(74,130,500)','HardMETPt>130 && NPhotons>=2',False]


print ('fileskey', fileskey)
infilekey = fileskey.split('/')[-1].replace('*','').replace('.root','')
newfilename = 'output/mediumchunks/weightedHists_'+infilekey+'_'+SpecialSettings+'.root'
if 'T5' in infilekey or 'T6' in infilekey: newfilename = newfilename.replace('mediumchunks','signals')

if tryolder: newfilename = newfilename.replace('.root','_older.root')
if BaseOnSavedGit: newfilename = newfilename.replace('.root','SavedGit.root')
if fullId: newfilename = newfilename.replace('.root','_fullId.root')


    
fnew = TFile(newfilename, 'recreate')
print ('will make file', fnew.GetName())
c1 = mkcanvas()
c2 = mkcanvas('c2')

for key in plotBundle:
    drawarg, constraint, blinding = plotBundle[key]
    obsweight = evtweight+'*('+constraint + ' && '+ universalconstraint + ' && IsRandS==0)'
    #puWeight
    print ('drawing', drawarg, ', with constraint:', obsweight)
    chain.Draw(drawarg,obsweight, 'e')
    hobs = chain.GetHistogram().Clone(key+'_obs')
    if not ('Vs' in key): hobs.GetYaxis().SetRangeUser(0.01,10000*hobs.GetMaximum())

    c1.cd()

    drawarg = drawarg
    randsconstraint = constraint
    methweight = evtweight+'/NSmearsPerEvent*('+ randsconstraint + ' && '+universalconstraint+ ' && IsRandS==1 && rebalancedHardMet<120)'
    #puWeight
    print ('drawing', drawarg, ', with constraint:', methweight)
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
    hobs.Write('h'+hobs.GetName())        
    hrands.GetXaxis().SetTitle(key.split('_')[-1])
    hrands.SetTitle('rebalance and smeared')
    hrands.Write('h'+hrands.GetName())
    
    if dopred: 
        hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,hobs,[hrands],datamc='MC',lumi='n/a', title = '', LinearScale=False, fractionthing='observed / method')
        c1.Update()
        c1.Write('c_'+key)
        c1.Print('pdfs/Closure/'+key+'.pdf')        
    print (sys.argv)





print ('just created', fnew.GetName())
fnew.Close()

