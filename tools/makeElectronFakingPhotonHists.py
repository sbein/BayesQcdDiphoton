
#Welcome to the industrial age of Sam's rebalance and smear code. You're going to have a lot of fun!
import os,sys
from ROOT import *
from array import array
from glob import glob
from utils import *
import numpy as np
import time

'''
python tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.WJetsToLNu_Tune  --genmatch True --quickrun True
python tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.TTJets_Tune  --genmatch True --quickrun True

nohup python tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.WJetsToLNu_Tune  --genmatch True > outW.txt &
nohup python tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.TTJets_Tune  --genmatch True  > outTT.txt &


ls /eos/uscms/store/group/lpcsusyphotons/TreeMaker/EfgImplements/
eosls /store/group/lpcsusyphotons/EfgImplements/ |grep Summer16
rm $EOS/store//group/lpcsusyphotons/EfgImplements/*
python tools/submitjobs.py --analyzer tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.WJetsToLNu --genmatch True --directoryout EfgImplements
python tools/submitjobs.py --analyzer tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.TTJets --genmatch True --directoryout EfgImplements
python tools/submitjobs.py --analyzer tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.DYJetsToLL_M-50 --genmatch True --directoryout EfgImplements
python tools/submitjobs.py --analyzer tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.WJetsToLNu --genmatch False --directoryout EfgImplements
python tools/submitjobs.py --analyzer tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.TTJets --genmatch False --directoryout EfgImplements
python tools/submitjobs.py --analyzer tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.DYJetsToLL_M-50 --genmatch False --directoryout EfgImplements

hadd -f efgoutput/efg-Summer16v3.WJetsToLNu_GenMatchTrue.root /eos/uscms/store/group/lpcsusyphotons/EfgImplements/efg-Summer16v3.WJetsToLNu*GenMatchTrue*.root
hadd -f efgoutput/efg-Summer16v3.TTJets_GenMatchTrue.root /eos/uscms/store/group/lpcsusyphotons/EfgImplements/efg-Summer16v3.TTJets*GenMatchTrue*.root
hadd -f efgoutput/efg-Summer16v3.DYJetsToLL_M-50_GenMatchTrue.root /eos/uscms/store/group/lpcsusyphotons/EfgImplements/efg-Summer16v3.DYJetsToLL_M-50*GenMatchTrue*.root
hadd -f efgoutput/efg-Summer16v3.WJetsToLNu_GenMatchFalse.root /eos/uscms/store/group/lpcsusyphotons/EfgImplements/efg-Summer16v3.WJetsToLNu*GenMatchFalse*.root
hadd -f efgoutput/efg-Summer16v3.TTJets_GenMatchFalse.root /eos/uscms/store/group/lpcsusyphotons/EfgImplements/efg-Summer16v3.TTJets*GenMatchFalse*.root
hadd -f efgoutput/efg-Summer16v3.DYJetsToLL_M-50_GenMatchFalse.root /eos/uscms/store/group/lpcsusyphotons/EfgImplements/efg-Summer16v3.DYJetsToLL_M-50*GenMatchFalse*.root

python tools/efgClosurePlotter.py

python tools/efgClosurePlotter.py GenMatchTrue
python tools/efgClosurePlotter.py GenMatchFalse
python tools/whiphtml.py "/uscms_data/d3/sbein/Diphoton/18Jan2019/CMSSW_10_1_0/src/BayesQcdDiphoton/pngs/GenMatchTrue/*.png"
python tools/whiphtml.py "/uscms_data/d3/sbein/Diphoton/18Jan2019/CMSSW_10_1_0/src/BayesQcdDiphoton/pngs/GenMatchFalse/*.png"
scp -r pngs/ ${DESY}:/afs/desy.de/user/b/beinsam/www/Diphoton/May2022

'''

gROOT.ProcessLine(open('src/UsefulJet.cc').read())
exec('from ROOT import *')

##read in command line arguments
defaultInfile_ = "Summer16v3.GJets_DR-0p4_HT"
#T2qqGG.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=1,help="analyzer script to batch")
parser.add_argument("-printevery", "--printevery", type=int, default=10000,help="short run")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile_,help="file")
parser.add_argument("-quickrun", "--quickrun", type=bool, default=False,help="short run")
parser.add_argument("-genmatch", "--genmatch", type=str, default='False',help="short run")
parser.add_argument("-debugmode", "--debugmode", type=bool, default=False,help="short run")
parser.add_argument("-directoryout", "--directoryout", type=bool, default=False,help="only used in submitjobs.py")
parser.add_argument("-extended", "--extended", type=int, default=1,help="short run")
args = parser.parse_args()
fnamekeyword = args.fnamekeyword
inputFiles = glob(fnamekeyword)
verbosity = args.verbosity
printevery = args.printevery
debugmode = args.debugmode
quickrun = args.quickrun
genmatch = bool(args.genmatch=='True')
extended = args.extended
debugmode = False

if 'Run20' in fnamekeyword: isdata = True
else: isdata = False

is2017 = False
is2016 = False
is2018 = False

if 'Run2016' in fnamekeyword or 'Summer16' in fnamekeyword: 
    BTAG_deepCSV = 0.6324
    is2016 = True
if 'Run2017' in fnamekeyword or 'Fall17' in fnamekeyword: 
    BTAG_deepCSV = 0.4941
    is2017 = True
if 'Run2018' in fnamekeyword or 'Autumn18' in fnamekeyword: 
    BTAG_deepCSV = 0.4184#0.4941####
    is2018 = True


inf = 999999
if 'TTJets_TuneC' in fnamekeyword:  madranges = [(0,600)]
elif 'TTJets_HT' in fnamekeyword: madranges = [(600,inf)]
elif 'WJetsToLNu_TuneC' in fnamekeyword: madranges = [(0, 100)]
elif 'WJetsToLNu_HT' in fnamekeyword: madranges = [(100, inf)]
elif 'DYJetsToLL_M-50_TuneC' in fnamekeyword: madranges = [(0, 100)]
elif 'DYJetsToLL_M-50_HT' in fnamekeyword: madranges = [(100, inf)]
else: madranges = [(0, inf)]

if 'Fast' in fnamekeyword or 'pMSSM' in fnamekeyword: isfast = True
else: isfast = False
issignal = abs('Fast' in fnamekeyword)




regionCuts = {}
varlist_                               = ['HardMet', 'NPhotons','NEGammas', 'Pho1Pt', 'Pho1Eta',  'Pho2Pt',  'Pho2Eta', 'NJets', 'BTags']
regionCuts['SinglePhotonLowPtLowMet']  = [(0,inf),    (1,1),     (0,0),      (30,inf), (-inf,inf), (-inf,inf),(-inf,inf),(0,inf), (0,inf)]

nphoidx = varlist_.index('NPhotons')
negidx = varlist_.index('NEGammas')
regionkeys = regionCuts.keys()
for key in regionkeys:
    newkey = key+'HasPixelSeed'
    newlist2 = list(regionCuts[key])
    newlist2[nphoidx] = (regionCuts[key][nphoidx][0]-1, regionCuts[key][nphoidx][1]-1)
    newlist2[negidx] = (regionCuts[key][negidx][0]+1, regionCuts[key][negidx][1]+1)    
    regionCuts[newkey] = newlist2
        
        
ncuts = 5
def selectionFeatureVector(fvector, regionkey='', omitcuts=''):
    if not fvector[0]>=fvector[1]: return False
    iomits = []
    for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
    for i, feature in enumerate(fvector):
        if i>=ncuts: continue
        if i in iomits: continue
        if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]):
            return False
    return True
    
    
thebinning = binning
indexVar = {}
for ivar, var in enumerate(varlist_): indexVar[var] = ivar
histoStructDict = {}
for region in regionCuts:
    for var in varlist_:
        histname = region+'_'+var
        histoStructDict[histname] = mkHistoStruct(histname, thebinning)
        print 'histname', histname
print 'histoStructDict', histoStructDict.keys()

fweights = TFile('usefulthings/efg_Summer2016.root')
fweights.ls()
hweightBarrel = fweights.Get('htf_dyjets_Barrel')
hweightEndcap = fweights.Get('htf_dyjets_Endcap')
xax = hweightBarrel.GetXaxis()


#################
# Load in chain #
#################        root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/
'''
ls -1 -d /eos/uscms//store/group/lpcsusyPhotons/TreeMaker/*.root > usefulthings/filelistDiphoton.txt
python tools/globthemfiles.py
'''
fnamefilename = 'usefulthings/filelistDiphoton.txt'
print 'as file list, using', fnamefilename
fnamefile = open(fnamefilename)
lines = fnamefile.readlines()
shortfname = fnamekeyword.split('/')[-1].strip().replace('*','')
print 'going to check for ', shortfname
fnamefile.close()
c = TChain('TreeMaker2/PreSelection')
filelist = []
iadded = 0
for line in lines:
    if not shortfname in line: continue
    fname = line.strip()
    if '/eos/uscms/' in fname:
        fname = fname.replace('/eos/uscms/','root://cmsxrootd.fnal.gov//')
    else:
        fname = fname.replace('/store/','root://cmseos.fnal.gov//store/')
    print 'adding', fname
    iadded+=1
    c.Add(fname)
    filelist.append(fname)
    if quickrun and iadded>1: break
n2process = c.GetEntries()
nentries = c.GetEntries()


print 'will analyze', n2process, 'events'
c.Show(0)

##Create output file
infileID = fnamekeyword.split('/')[-1].replace('.root','')+'_part'+str(extended)
newname = 'efg-'+infileID+'_GenMatch'+str(genmatch)+'.root'
if issignal: 
    newname = newname.split('_')[0]+'_m'+str(par1)+'d'+str(par2)+'_time'+str(round(time.time()%100000,2))+'.root'

fnew = TFile(newname, 'recreate')
print 'creating', newname

###--Get Scale Factor hist---------------
PhotonSF2016_file = TFile('usefulthings/Fall17V2_2016_Loose_photons.root')
PhotonSF2016_hist = PhotonSF2016_file.Get('EGamma_SF2D')


print 'n(entries) =', n2process
tcounter = TTree('tcounter','tcounter')
hHt = TH1F('hHt','hHt',120,0,2500)
hHt.Sumw2()
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',120,0,2500)
hHtWeighted.Sumw2()
hfilterfails = TH1F('hfilterfails','hfilterfails',14,-14,0)


hGenElPtBarrel = TH1F('hGenElPtBarrel','hGenElPtBarrel',20,0,400)
histoStyler(hGenElPtBarrel, kGreen+1)
hGenElPtPhoMatchedBarrel = TH1F('hGenElPtPhoMatchedBarrel','hGenElPtPhoMatchedBarrel',20,0,400)
histoStyler(hGenElPtPhoMatchedBarrel, kOrange)
hGenElPtEleMatchedBarrel = TH1F('hGenElPtEleMatchedBarrel','hGenElPtEleMatchedBarrel',20,0,400)
histoStyler(hGenElPtEleMatchedBarrel, kTeal-4)
hGenElPtEleMatchedBarrel_weighted = TH1F('hGenElPtEleMatchedBarrel_weighted','hGenElPtEleMatchedBarrel_weighted',20,0,400)
histoStyler(hGenElPtEleMatchedBarrel_weighted, kTeal-4)

hGenElPtEndcap = TH1F('hGenElPtEndcap','hGenElPtEndcap',20,0,400)
histoStyler(hGenElPtEndcap, kGreen+1)
hGenElPtPhoMatchedEndcap = TH1F('hGenElPtPhoMatchedEndcap','hGenElPtPhoMatchedEndcap',20,0,400)
histoStyler(hGenElPtPhoMatchedEndcap, kOrange)
hGenElPtEleMatchedEndcap = TH1F('hGenElPtEleMatchedEndcap','hGenElPtEleMatchedEndcap',20,0,400)
histoStyler(hGenElPtEleMatchedEndcap, kTeal-4)
hGenElPtEleMatchedEndcap_weighted = TH1F('hGenElPtEleMatchedEndcap_weighted','hGenElPtEleMatchedEndcap_weighted',20,0,400)
histoStyler(hGenElPtEleMatchedEndcap_weighted, kTeal-4)

#reco histograms, data and method
hLeadPhoPtTruth = TH1F('hLeadPhoPtTruth','hLeadPhoPtTruth',20,0,400); histoStyler(hLeadPhoPtTruth, kViolet)
hLeadPhoPtMethod = TH1F('hLeadPhoPtMethod','hLeadPhoPtMethod',20,0,400); histoStyler(hLeadPhoPtMethod, kAzure+1)
hLeadPhoEtaTruth = TH1F('hLeadPhoEtaTruth','hLeadPhoEtaTruth',20,-3,3); histoStyler(hLeadPhoEtaTruth, kViolet)
hLeadPhoEtaMethod = TH1F('hLeadPhoEtaMethod','hLeadPhoEtaMethod',20,-3,3); histoStyler(hLeadPhoEtaMethod, kAzure+1)
hTrailPhoPtTruth = TH1F('hTrailPhoPtTruth','hTrailPhoPtTruth',20,0,400); histoStyler(hTrailPhoPtTruth, kViolet)
hTrailPhoPtMethod = TH1F('hTrailPhoPtMethod','hTrailPhoPtMethod',20,0,400); histoStyler(hTrailPhoPtMethod, kAzure+1)
hTrailPhoEtaTruth = TH1F('hTrailPhoEtaTruth','hTrailPhoEtaTruth',20,-3,3); histoStyler(hTrailPhoEtaTruth, kViolet)
hTrailPhoEtaMethod = TH1F('hTrailPhoEtaMethod','hTrailPhoEtaMethod',20,-3,3); histoStyler(hTrailPhoEtaMethod, kAzure+1)
hMetTruth = TH1F('hMetTruth','hMetTruth',20,0,400); histoStyler(hMetTruth, kViolet)
hMetMethod = TH1F('hMetMethod','hMetMethod',20,0,400); histoStyler(hMetMethod, kAzure+1)
hHardMetTruth = TH1F('hHardMetTruth','hHardMetTruth',20,0,400); histoStyler(hHardMetTruth, kViolet)
hHardMetMethod = TH1F('hHardMetMethod','hHardMetMethod',20,0,400); histoStyler(hHardMetMethod, kAzure+1)
hNJetsTruth = TH1F('hNJetsTruth','hNJetsTruth',10,0,10); histoStyler(hNJetsTruth, kViolet)
hNJetsMethod = TH1F('hNJetsMethod','hNJetsMethod',10,0,10); histoStyler(hNJetsMethod, kAzure+1)
hBTagsTruth = TH1F('hBTagsTruth','hBTagsTruth',4,0,4); histoStyler(hBTagsTruth, kViolet)
hBTagsMethod = TH1F('hBTagsMethod','hBTagsMethod',4,0,4); histoStyler(hBTagsMethod, kAzure+1)


acme_objects = vector('TLorentzVector')()
recophotons = vector('TLorentzVector')()
recoelectrons = vector('TLorentzVector')()
recoegammas = vector('TLorentzVector')()
recojets_ = vector('TLorentzVector')()
recojets = vector('TLorentzVector')()
recomuons = vector('TLorentzVector')()

t0 = time.time()
for ientry in range((extended-1)*n2process, extended*n2process):
    if ientry%printevery==0:
        print "processing event", ientry, '/', extended*n2process, 'time', time.time()-t0
    if debugmode:
        if not ientry in [102850]: continue
    if ientry>nentries: break
    c.GetEntry(ientry)
    tcounter.Fill()
    if isdata:  
        weight = 1.0
    else:  
        weight = c.CrossSection
        isValidHtRange = False
        for madrange in madranges:
            if (c.madHT>=madrange[0] and c.madHT<madrange[1]):
                isValidHtRange = True
                break 
        if not isValidHtRange: continue
    if isfast: 
        if not passesUniversalSelectionFast(c): continue
    else:
        if passesUniversalSelection(c)<0: continue
    
    recophotons.clear()
    recoelectrons.clear()  
    recoegammas.clear()  
    acme_objects.clear()
    
    if not (len(c.Photons)>0 or len(c.Electrons)>0 or len(c.Muons)>0): continue
    
    npasspixelseed = 0
    for iPho, Pho in enumerate(c.Photons):
        if not Pho.Pt()>30: continue #trigger is Pho 70
        if not abs(Pho.Eta())<2.4: continue        
        if not bool(c.Photons_fullID[iPho]): continue 
        tlvPho = TLorentzVector()
        tlvPho.SetPtEtaPhiE(Pho.Pt(), Pho.Eta(), Pho.Phi(), Pho.E())
        recoegammas.push_back(tlvPho)
        if int(bool(c.Photons_hasPixelSeed[iPho])): recoelectrons.push_back(tlvPho)
        else: recophotons.push_back(tlvPho)
    
    if not (len(recoegammas))>0: continue #require two egamma objects
    
    
    recojets_.clear()
    for ijet, jet in enumerate(c.Jets):
        if not (jet.Pt()>2 and abs(jet.Eta())<5.0): continue
        jettlv = TLorentzVector(jet.Px(),jet.Py(),jet.Pz(), jet.E())
        recojets_.push_back(jettlv)
    
    if is2017: # ecal noise treatment
        recojets_.clear()
        for ijet, jet in enumerate(c.Jets):
            if not (jet.Pt()>2 and abs(jet.Eta())<5.0): continue
            if abs(jet.Eta())>2.65 and abs(jet.Eta()) < 3.139 and jet.Pt()/c.Jets_jecFactor[ijet]<50: continue #/c.Jets_jerFactor[ijet]
            jettlv = TLorentzVector(jet.Px(),jet.Py(),jet.Pz(), jet.E())
            recojets_.push_back(jettlv)
            
    recojets.clear()
    nMatchedAcmeOuterPairs = 0
    nMatchedAcmeInnerPairs = 0
    passesJetId = True
    for ijet, jet in enumerate(recojets_):
        if not jet.Pt()>15: continue
        if not abs(jet.Eta())<5: continue
        closestAcme = getClosestObject(acme_objects, jet, 0.1)
        if jet.DeltaR(closestAcme)<0.5:
            nMatchedAcmeOuterPairs+=1
            if jet.DeltaR(closestAcme)<0.4:
                nMatchedAcmeInnerPairs+=1
                continue
        recojets.push_back(jet)
    
    if not passesJetId: 
        print ientry, 'failed jet ID'
        continue 
    
    shouldskipevent = False
    if not nMatchedAcmeOuterPairs==nMatchedAcmeInnerPairs: 
        shouldskipevent = True    
    if not nMatchedAcmeInnerPairs==len(acme_objects): 
        shouldskipevent = True
    if shouldskipevent: 
        continue
        
    genelectrons = []

    for igp, gp in enumerate(c.GenParticles):
        if not abs(c.GenParticles_PdgId[igp])==11: continue
        if not gp.Pt()>10: continue
        gptlv = TLorentzVector(gp.Px(),gp.Py(), gp.Pz(), gp.E())
        genelectrons.append(gptlv)
        
    #first the gen-matching analysis, where histograms are also used to derive the gen-based transfer factors 
    ngenmatches = 0
    for gene in genelectrons:
        eta = abs(gene.Eta())
        if eta<1.45: fillth1(hGenElPtBarrel, gene.Pt())
        else: fillth1(hGenElPtEndcap, gene.Pt())
        for pho in recophotons:
            dr = pho.DeltaR(gene)
            if dr<0.03: 
                if eta<1.45: fillth1(hGenElPtPhoMatchedBarrel, gene.Pt())
                else: fillth1(hGenElPtPhoMatchedEndcap, gene.Pt())
                ngenmatches+=1
                break
        for ele in recoelectrons:
            dr = ele.DeltaR(gene)
            if dr<0.03: 
                if eta<1.45: 
                    fillth1(hGenElPtEleMatchedBarrel, gene.Pt())
                    fillth1(hGenElPtEleMatchedBarrel_weighted, gene.Pt(), hweightBarrel.GetBinContent(min(xax.GetNbins(), xax.FindBin(gene.Pt()))))
                else: 
                    fillth1(hGenElPtEleMatchedEndcap, gene.Pt())
                    fillth1(hGenElPtEleMatchedEndcap_weighted, gene.Pt(),hweightEndcap.GetBinContent(min(xax.GetNbins(), xax.FindBin(gene.Pt()))))
                break                
        
    if not len(genelectrons)>0: continue # this code is intended to be a closure test for backgrounds in which there is a real electron
    if genmatch and ngenmatches==0: continue ####this ensures we're looking at efg backgrounds
    #now the reco analysis    
    if not (len(recophotons))>0: continue #require at least one photon
    

    MetVec = TLorentzVector()
    MetVec.SetPtEtaPhiE(c.MET,0,c.METPhi,c.MET)
    tHardMetVec = TLorentzVector()
    tHardMetVec.SetPtEtaPhiE(c.MHT,0,c.MHTPhi,c.MHT)
    tHardMetPt, tHardMetPhi = tHardMetVec.Pt(), tHardMetVec.Phi()
    njets = c.NJets
    btags = c.BTags
    
    pt1, pt2, eta1, eta2 = -11,-11,-11,-11
    if len(recoegammas)>0: 
    	pt1 = recoegammas[0].Pt()
    	eta1 = recoegammas[0].Eta()
    if len(recoegammas)>1: 
    	pt2 = recoegammas[1].Pt()
    	eta2 = recoegammas[1].Eta()
    fv = [MetVec.Pt(), len(recophotons), len(recoegammas), pt1, eta1, pt2, eta2, njets, btags]


    for regionkey in regionCuts:
        for ivar, varname in enumerate(varlist_):
            if selectionFeatureVector(fv,regionkey,varname):
                fillth1(histoStructDict[regionkey+'_'+varname].Observed, fv[ivar], c.CrossSection)
                        
                            
    
    if len(recophotons)>1:
        fillth1(hLeadPhoPtTruth, recoegammas[0].Pt())
        fillth1(hLeadPhoEtaTruth, recoegammas[0].Eta())
        fillth1(hTrailPhoPtTruth, recoegammas[1].Pt())
        fillth1(hTrailPhoEtaTruth, recoegammas[1].Eta())
        fillth1(hMetTruth, MetVec.Pt())
        fillth1(hHardMetTruth, tHardMetPt)
        fillth1(hNJetsTruth, njets )
        fillth1(hBTagsTruth, btags)   
    elif len(recoelectrons)>0:
        if recoelectrons[0].Pt()<recoegammas[0].Pt()-0.01: 
            pt4prediction = recoegammas[1].Pt()
            if abs(recoegammas[1].Eta())<1.45: tf = hweightBarrel.GetBinContent(min(xax.GetNbins(), xax.FindBin(pt4prediction)))
            else: tf = hweightEndcap.GetBinContent(min(xax.GetNbins(), xax.FindBin(pt4prediction)))
        else: 
            pt4prediction = recoegammas[0].Pt()
            if abs(recoegammas[0].Eta())<1.45: tf = hweightBarrel.GetBinContent(min(xax.GetNbins(), xax.FindBin(pt4prediction)))
            else: tf = hweightEndcap.GetBinContent(min(xax.GetNbins(), xax.FindBin(pt4prediction)))        
            
     
        fillth1(hLeadPhoPtMethod, recoegammas[0].Pt(), tf)
        fillth1(hLeadPhoEtaMethod, recoegammas[0].Eta(), tf) 
        fillth1(hTrailPhoPtMethod, recoegammas[1].Pt(), tf)
        fillth1(hTrailPhoEtaMethod, recoegammas[1].Eta(), tf) 
        fillth1(hMetMethod,  MetVec.Pt(), tf) 
        fillth1(hHardMetMethod, tHardMetPt, tf) 
        fillth1(hNJetsMethod, njets, tf) 
        fillth1(hBTagsMethod, btags, tf) 
    
    


fnew.cd()
fnew.cd('../')
hHt.Write()
hHtWeighted.Write()
hGenElPtBarrel.Write()
hGenElPtPhoMatchedBarrel.Write()
hGenElPtEleMatchedBarrel.Write()
hGenElPtEleMatchedBarrel_weighted.Write()
hGenElPtEndcap.Write()
hGenElPtPhoMatchedEndcap.Write()
hGenElPtEleMatchedEndcap_weighted.Write()

hLeadPhoPtTruth.Write()
hLeadPhoPtMethod.Write()
hLeadPhoEtaTruth.Write()
hLeadPhoEtaMethod.Write()
hTrailPhoPtTruth.Write()
hTrailPhoPtMethod.Write()
hTrailPhoEtaTruth.Write()
hTrailPhoEtaMethod.Write()
hMetTruth.Write()
hMetMethod.Write()
hHardMetTruth.Write()
hHardMetMethod.Write()
hNJetsTruth.Write()
hNJetsMethod.Write()
hBTagsTruth.Write()
hBTagsMethod.Write()


writeHistoStruct(histoStructDict, 'ObservedElectronEfgMethod')

hfilterfails.Write()
tcounter.Write()


print 'just created', fnew.GetName()
fnew.Close()



'''
tree->GetBranch("xxx")->SetName("yyy");
tree->GetLeaf("xxx")->SetTitle("yyy");
'''


