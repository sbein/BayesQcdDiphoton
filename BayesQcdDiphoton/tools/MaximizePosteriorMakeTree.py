#Welcome to the industrial age of Sam's rebalance and smear code. You're going to have a lot of fun!
import os,sys
from ROOT import *
from array import array
from glob import glob
from utils import *
import numpy as np
#from ra2blibs import *
import time

###stuff that would be nice in a config file:
met4skim = 120
mhtjetetacut = 5.0 # also needs be be changed in UsefulJet.h
lhdHardMetJetPtCut = 15.0
AnHardMetJetPtCut = 30.0
rebalancedMetCut = 150
cleanrecluster = False
useMediumPho = False

debugmode = False
sayalot = False
nametag = {'Nom':'', 'Up': 'JerUp'}

##load in UsefulJet class, which the rebalance and smear code uses
gROOT.ProcessLine(open('src/UsefulJet.cc').read())
exec('from ROOT import *')
gROOT.ProcessLine(open('src/BayesRandS.cc').read())
exec('from ROOT import *')


##read in command line arguments
defaultInfile_ = "Summer16v3.GJets_DR-0p4_HT"
#T2qqGG.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=1,help="analyzer script to batch")
parser.add_argument("-printevery", "--printevery", type=int, default=100,help="short run")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile_,help="file")
parser.add_argument("-bootstrap", "--bootstrap", type=str, default='0',help="boot strapping (0,1of5,2of5,3of5,...)")
parser.add_argument("-jersf", "--JerUpDown", type=str, default='Nom',help="JER scale factor (JerNom, JerUp, ...)")
parser.add_argument("-forcetemplates", "--forcetemplates", type=str, default='',help="you can use this to override the template choice")
parser.add_argument("-quickrun", "--quickrun", type=bool, default=False,help="short run")
parser.add_argument("-debugmode", "--debugmode", type=bool, default=False,help="short run")
parser.add_argument("-sayalot", "--sayalot", type=bool, default=False,help="short run")
parser.add_argument("-extended", "--extended", type=int, default=1,help="short run")
args = parser.parse_args()
extended = args.extended
fnamekeyword = args.fnamekeyword
inputFiles = glob(fnamekeyword)
bootstrap = args.bootstrap
JerUpDown = args.JerUpDown
forcetemplates = args.forcetemplates
verbosity = args.verbosity
printevery = args.printevery
debugmode = args.debugmode
printevery = args.printevery
quickrun = args.quickrun
sayalot = args.sayalot


llhdHardMetThresh = 15
mktree = True

#stuff for Matt's BDT
reader = TMVA.Reader()
_Ngoodjets_ = array('f',[0])
_ST_ = array('f',[0])
_MHT_ = array('f',[0])
_dPhi_GG_ = array('f',[0])
_Photons0Et_ = array('f',[0])
_Photons1Et_ = array('f',[0])
_Pt_jets_ = array('f',[0])
_Pt_GG_ = array('f',[0])
_jet_ST_ = array('f',[0])
_min_d_phi_ = array('f',[0])
_dPhi_GGHardMET_ = array('f',[0])
reader.AddVariable("Ngoodjets",_Ngoodjets_)      
reader.AddVariable("ST",_ST_)          
reader.AddVariable("Pt_jets",_Pt_jets_)
reader.AddVariable("dPhi_GG",_dPhi_GG_)
reader.AddVariable("Photons[0].Et()",_Photons0Et_)
reader.AddVariable("Photons[1].Et()",_Photons1Et_)
reader.AddVariable("HardMET",_MHT_)
reader.AddVariable("Pt_GG",_Pt_GG_)
reader.AddVariable("ST_jets",_jet_ST_)
reader.AddVariable("min_dPhi",_min_d_phi_)
reader.AddVariable("dPhi_GGHardMET",_dPhi_GGHardMET_)
#reader.BookMVA("BDT", '/eos/uscms/store/user/mjoyce/SUSY/TMVAClassification_BDT.weights.xml')
reader.BookMVA("BDT", 'usefulthings/TMVAClassification_BDT.weights_oldish.xml')
###

if bootstrap=='0': 
    bootstrapmode = False
    bootupfactor = 1
else: 
    bootstrapmode = True
    from random import randint
    thisbootstrap, nbootstraps = bootstrap.split('of')
    thisbootstrap, nbootstraps = int(thisbootstrap), int(nbootstraps)
    print 'thisbootstrap, nbootstraps', thisbootstrap, nbootstraps
    bootupfactor = nbootstraps


ntupleV = '17'
if 'Summer16' in fnamekeyword or 'Fall17' in fnamekeyword or 'Autumn18' in fnamekeyword:
    isdata = False
else: 
    isdata = True

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

BTag_Cut = BTAG_deepCSV


#################
# Load in chain #
#################
ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/'
fnamefilename = 'usefulthings/filelistDiphoton.txt'
if not 'DoubleEG' in fnamekeyword:
    if 'Summer16v3.QCD_HT' in fnamekeyword or 'Summer16v3.WGJets_MonoPhoton' in fnamekeyword or 'Run20' in fnamekeyword: 
        fnamefilename = 'usefulthings/filelistV17.txt'
fnamefile = open(fnamefilename)
lines = fnamefile.readlines()
shortfname = fnamekeyword.strip()
print 'going to check for ', shortfname
fnamefile.close()
c = TChain('TreeMaker2/PreSelection')
filelist = []
for line in lines:
    if not shortfname in line: continue
    fname = line.strip()
    if 'Summer16v3.QCD_HT' in fnamekeyword or 'Run20' in fnamekeyword or 'Summer16v3.WGJets_MonoPhoton' in fnamekeyword: fname = ra2bspace+fname
    fname = fname.replace('/eos/uscms/','root://cmsxrootd.fnal.gov//')
    if 'WGJets' in fnamekeyword: fname = fname.replace('root://cmsxrootd.fnal.gov///store/group/lpcsusyhad','root://hepxrd01.colorado.edu:1094//store/user/aperloff')
    print 'adding', fname
    c.Add(fname)
    filelist.append(fname)
    if quickrun: break
n2process = c.GetEntries()
nentries = c.GetEntries()
if quickrun: 
    n2process = min(30000,n2process)
    


print 'will analyze', n2process, 'events'
c.Show(0)



if ('Summer16' in fnamekeyword or 'Run2016' in fnamekeyword): 
    templateFileName = 'usefulthings/ResponseFunctionsMC16AllFilters'+nametag[JerUpDown]+'_deepCsv.root'
if ('Fall17' in fnamekeyword or 'Run2017' in fnamekeyword): 
    templateFileName = 'usefulthings/ResponseFunctionsMC17'+nametag[JerUpDown]+'_deepCsv.root'
if ('Autumn18' in fnamekeyword or 'Run2018' in fnamekeyword): 
    templateFileName = 'usefulthings/ResponseFunctionsMC18'+nametag[JerUpDown]+'_deepCsv.root'
if not forcetemplates=='': templateFileName = forcetemplates

print 'using templates from',templateFileName
ftemplate = TFile(templateFileName)
ftemplate.ls()
hPtTemplate = ftemplate.Get('hPtTemplate')
templatePtAxis = hPtTemplate.GetXaxis()
hEtaTemplate = ftemplate.Get('hEtaTemplate')
templateEtaAxis = hEtaTemplate.GetXaxis()

hHtTemplate = ftemplate.Get('hHtTemplate')
templateHtAxis = hHtTemplate.GetXaxis()
'''#option for using FullSim-based prior
priorFileName = templateFileName
priorFileName = 'usefulthings/ResponseFunctionsMC17AllFilters_deepCsv.root'
fprior = TFile(priorFileName)
hHtTemplate = fprior.Get('hHtTemplate')
templateHtAxis = hHtTemplate.GetXaxis()
'''

##Create output file
infileID = fnamekeyword.split('/')[-1].replace('.root','')+'_part'+str(extended)
newname = 'posterior-'+infileID+'.root'
fnew = TFile(newname, 'recreate')
print 'creating', newname


if mktree:
    print 'cloning tree'
    fnew.mkdir('TreeMaker2')
    fnew.cd('TreeMaker2/')
    tree_out = c.CloneTree(0)
    print 'cloned tree'    
    mDiphoton = np.zeros(1, dtype=float)
    b_mDiphoton = tree_out.Branch('mDiphoton', mDiphoton, 'mDiphoton/D')
    mDiphoton[0] = -11.0
    HardMETPt = np.zeros(1, dtype=float)
    b_HardMETPt = tree_out.Branch('HardMETPt', HardMETPt, 'HardMETPt/D')
    HardMETPt[0] = -11.0
    HardMETPhi = np.zeros(1, dtype=float)
    b_HardMETPhi = tree_out.Branch('HardMETPhi', HardMETPhi, 'HardMETPhi/D')
    HardMETPhi[0] = -11.0    
    NPhotonsLoose = np.zeros(1, dtype=int)
    b_NPhotonsLoose = tree_out.Branch('NPhotonsLoose', NPhotonsLoose, 'NPhotonsLoose/I')
    NPhotonsLoose[0] = -11
    NPhotonsMedium = np.zeros(1, dtype=int)
    b_NPhotonsMedium = tree_out.Branch('NPhotonsMedium', NPhotonsMedium, 'NPhotonsMedium/I')
    NPhotonsMedium[0] = -11

    IsUniqueSeed = np.zeros(1, dtype=int)
    b_IsUniqueSeed = tree_out.Branch('IsUniqueSeed', IsUniqueSeed, 'IsUniqueSeed/I')
    IsUniqueSeed[0] = 1
    
    jetsRandS = ROOT.std.vector('TLorentzVector')()
    b_jetsRandS = tree_out.Branch('JetsRandS', jetsRandS)

    jetsRebalanced = ROOT.std.vector('TLorentzVector')()
    b_jetsRebalanced = tree_out.Branch('JetsRebalanced', jetsRebalanced)

    jetsRebalanced_origIdx = ROOT.std.vector('int')()
    b_jetsRebalanced_origIdx = tree_out.Branch('JetsRebalanced_origIdx', jetsRebalanced_origIdx)    
        
    BTagsDeepCSV = ROOT.std.vector('float')()
    tree_out.Branch('JetsRandS_bJetTagDeepCSVBvsAll', BTagsDeepCSV)

    jetsRandS_origIdx = ROOT.std.vector('int')()
    tree_out.Branch('JetsRandS_origIdx', jetsRandS_origIdx)    

    HTRandS = np.zeros(1, dtype=float)
    HardMETPtRandS = np.zeros(1, dtype=float)
    HardMETPhiRandS = np.zeros(1, dtype=float)
    NJetsRandS = np.zeros(1, dtype=int)
    BTagsRandS = np.zeros(1, dtype=int)
    NSmearsPerEvent = np.zeros(1, dtype=int)
    FitSucceed = np.zeros(1, dtype=int)    
    tree_out.Branch('HTRandS', HTRandS, 'HTRandS/D')
    tree_out.Branch('HardMETPtRandS', HardMETPtRandS, 'HardMETPtRandS/D')
    tree_out.Branch('HardMETPhiRandS', HardMETPhiRandS, 'HardMETPhiRandS/D')
    tree_out.Branch('BTagsRandS', BTagsRandS, 'BTagsRandS/I')
    tree_out.Branch('NJetsRandS', NJetsRandS, 'NJetsRandS/I')
    tree_out.Branch('NSmearsPerEvent', NSmearsPerEvent, 'NSmearsPerEvent/I')
    tree_out.Branch('FitSucceed', FitSucceed, 'FitSucceed/I')    
    
print 'n(entries) =', n2process

hHt = TH1F('hHt','hHt',120,0,2500)
hHt.Sumw2()
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',120,0,2500)
hHtWeighted.Sumw2()
hGenMetGenHardMetRatio = TH1F('hGenMetGenHardMetRatio','hGenMetGenHardMetRatio',50,0,5)
hGenMetGenHardMetRatio.Sumw2()
hPassFit = TH1F('hPassFit','hPassFit',5,0,5)
hPassFit.Sumw2()
hTotFit = TH1F('hTotFit','hTotFit',5,0,5)
hTotFit.Sumw2()


GleanTemplatesFromFile(ftemplate)#, fprior)

acme_objects = vector('UsefulJet')()
recophotons_loose = vector('TLorentzVector')()
recophotons_medium = vector('TLorentzVector')()
recojets_ = vector('UsefulJet')()
recojets = vector('UsefulJet')()
recoelectrons = vector('TLorentzVector')()
recomuons = vector('TLorentzVector')()
genjets_ = vector('TLorentzVector')()

t0 = time.time()
for ientry in range((extended-1)*n2process, extended*n2process):


    if ientry%printevery==0:
        print "processing event", ientry, '/', extended*n2process, 'time', time.time()-t0

    if debugmode:
        if ientry in [298]: continue
    if ientry>nentries: break
    c.GetEntry(ientry)
    IsUniqueSeed[0] = 1

    if isdata: weight = 1
    else: weight = c.CrossSection

    if not passesUniversalSelection(c): continue
    #if not passesHadronicSusySelection(c): continue


    
    acme_objects.clear()
    recophotons_loose.clear()
    recophotons_medium.clear()
        
    #build up the vector of jets using TLorentzVectors; 
    #this is where you have to interface with the input format you're using
    if not (len(c.Photons)>0 or len(c.Electrons)>0 or len(c.Muons)>0): continue

    #idea: use HT to reference prior instead of ST

    for ipho, pho in enumerate(c.Photons):
        if not pho.Pt()>75: continue #trigger is pho 70
        if not bool(c.Photons_fullID[ipho]): continue ##need to BOOL this?
        if not abs(pho.Eta())<2.4: continue
        tlvpho = TLorentzVector()
        tlvpho.SetPtEtaPhiE(pho.Pt(), pho.Eta(), pho.Phi(), pho.E())  
        usefulpho = UsefulJet(tlvpho, 0, 0, -1)
        acme_objects.push_back(usefulpho)
        #if not c.Photons_genMatched[ipho]: continue
        #if bool(c.Photons_nonPrompt[ipho]): continue
        if bool(c.Photons_hasPixelSeed[ipho]): continue         
        recophotons_loose.push_back(tlvpho)
        if abs(pho.Eta())<1.48:   
            if not (c.Photons_hadTowOverEM[ipho]<0.0396  and c.Photons_sigmaIetaIeta[ipho]<0.01022 and c.Photons_pfChargedIsoRhoCorr[ipho]<0.441 and c.Photons_pfNeutralIsoRhoCorr[ipho]<(2.725+0.0148*c.Photons[ipho].Pt()+0.000017*pow(c.Photons[ipho].Pt(),2)) and c.Photons_pfGammaIsoRhoCorr[ipho]<(2.571+0.0047*c.Photons[ipho].Pt())): continue
        if abs(pho.Eta())>=1.48:
            if not (c.Photons_hadTowOverEM[ipho]<0.0219 and c.Photons_sigmaIetaIeta[ipho]<0.03001  and c.Photons_pfChargedIsoRhoCorr[ipho]< 0.442  and c.Photons_pfNeutralIsoRhoCorr[ipho]<(1.715+0.0163*c.Photons[ipho].Pt()+0.000014*pow(c.Photons[ipho].Pt(),2)) and c.Photons_pfGammaIsoRhoCorr[ipho]<(3.863+0.0034*c.Photons[ipho].Pt())): continue
        recophotons_medium.push_back(tlvpho)            
        if sayalot:
            print ientry, 'acme photon', pho.Pt(), pho.Eta(), pho.Phi()
            print 'Photons_genMatched', c.Photons_genMatched[ipho]
            print 'Photons_nonPrompt', bool(c.Photons_nonPrompt[ipho])
            print 'Photons_pfGammaIsoRhoCorr', c.Photons_pfGammaIsoRhoCorr[ipho]

    if useMediumPho: recophotons = recophotons_medium
    else: recophotons = recophotons_loose

    if not len(c.Photons)==recophotons.size():
        #print 'this is important'
        continue

    NPhotonsLoose[0] = len(recophotons_loose)
    NPhotonsMedium[0] = len(recophotons_medium)    
    
    #if not int(recophotons_loose.size())>0: continue    

    recoelectrons.clear()
    for iel, el in enumerate(c.Electrons):
        if not el.Pt()>20: continue
        if not c.Electrons_mediumID[iel]: continue
        if not c.Electrons_passIso[iel]: continue        
        tlvel = TLorentzVector()
        tlvel.SetPtEtaPhiE(el.Pt(), el.Eta(), el.Phi(), el.Pt()*TMath.CosH(el.Eta()))
        if debugmode:
            print ientry, 'acme electron', el.Pt()		
        usefulele = UsefulJet(tlvel, 0, 0, -1)
        acme_objects.push_back(usefulele)		
        if not abs(el.Eta())<2.4: continue		
        recoelectrons.push_back(tlvel)
    #if not len(recoelectrons)==0: continue

    recomuons.clear()
    for imu, mu in enumerate(c.Muons):
        if not mu.Pt()>20: continue
        if not c.Muons_mediumID[imu]: continue
        if not c.Muons_passIso[imu]: continue
        tlvmu = TLorentzVector()
        tlvmu.SetPtEtaPhiE(mu.Pt(), mu.Eta(), mu.Phi(), mu.Pt()*TMath.CosH(mu.Eta()))
        if debugmode:
            print ientry, 'acme muon', mu.Pt()				
        usefulmu = UsefulJet(tlvmu, 0, 0, -1)
        acme_objects.push_back(usefulmu)			
        if not abs(mu.Eta())<2.4: continue		
        recomuons.push_back(tlvmu)		
    #if not len(recomuons)==0: continue        		

    AcmeVector = TLorentzVector()
    AcmeVector.SetPxPyPzE(0,0,0,0)
    for obj in acme_objects: AcmeVector+=obj.tlv		

    _Templates_.AcmeVector = AcmeVector	
    

    #recojets_.clear()
    recojets_.clear()
    for ijet, jet in enumerate(c.Jets):
        if not (jet.Pt()>2 and abs(jet.Eta())<5.0): continue
        recojets_.push_back(UsefulJet(jet, c.Jets_bJetTagDeepCSVBvsAll[ijet], float(int(bool(c.Jets_ID[ijet]))), ijet))

        
        if sayalot and jet.Pt()>AnHardMetJetPtCut:
            print 'ijet original', ijet, 'pt, eta, phi', jet.Pt(), jet.Eta(), jet.Phi(), 'Jets_bJetTagDeepCSVBvsAll', c.Jets_bJetTagDeepCSVBvsAll[ijet], 'Jets_bDiscriminatorCSV', c.Jets_bDiscriminatorCSV[ijet], 'Jets_chargedEmEnergyFraction', c.Jets_chargedEmEnergyFraction[ijet], 'Jets_chargedHadronEnergyFraction', c.Jets_chargedHadronEnergyFraction[ijet], 'Jets_chargedMultiplicity', c.Jets_chargedMultiplicity[ijet], ', Jets_multiplicity', c.Jets_multiplicity[ijet], ', Jets_partonFlavor', c.Jets_partonFlavor[ijet] , ', Jets_photonEnergyFraction', c.Jets_photonEnergyFraction[ijet] , ', Jets_photonMultiplicity', c.Jets_photonMultiplicity[ijet], 'Jets_hadronFlavor', c.Jets_hadronFlavor[ijet], 'Jets_hadronFlavor', c.Jets_hadronFlavor[ijet], 'Jets_ID', bool(c.Jets_ID[ijet])

            
    if is2017: # ecal noise treatment
        recojets.clear()
        for ijet, jet in enumerate(c.Jets):
            if not (jet.Pt()>2 and abs(jet.Eta())<5.0): continue
            if abs(jet.Eta())>2.65 and abs(jet.Eta()) < 3.139 and jet.Pt()/c.Jets_jecFactor[ijet]<50: continue #/c.Jets_jerFactor[ijet]
            recojets.push_back(UsefulJet(jet, c.Jets_bJetTagDeepCSVBvsAll[ijet], jet.Pt()))  


            
    ##declare empty vector of UsefulJets (in c++, std::vector<UsefulJet>):
    recojets.clear()
    nMatchedAcmeOuterPairs = 0
    nMatchedAcmeInnerPairs = 0
    passesJetId = True
    for ijet, jet in enumerate(recojets_):
        if not jet.Pt()>15: continue
        if not abs(jet.Eta())<5: continue
        closestAcme = getClosestObject(acme_objects, jet, 0.1)
        if jet.DeltaR(closestAcme)<0.6:
            nMatchedAcmeOuterPairs+=1
            if jet.DeltaR(closestAcme)<0.3:
                closestAcme.originalIdx = jet.originalIdx                
                nMatchedAcmeInnerPairs+=1
                if sayalot: print 'skipping reco jet with pT, eta', jet.Pt(), jet.Eta(), jet.DeltaR(acme_objects[0].tlv)
                continue
        if jet.Pt()>AnHardMetJetPtCut and jet.JetId()<0.5: 
            passesJetId = False
            print 'failed jet id'
            break
        ujet = UsefulJet(jet.tlv, jet.btagscore, jet.jetId, jet.originalIdx)
        recojets.push_back(ujet)

    if not passesJetId: continue
    
    shouldskipevent = False
    if not nMatchedAcmeOuterPairs==nMatchedAcmeInnerPairs: shouldskipevent = True    
    if not nMatchedAcmeInnerPairs==len(acme_objects): shouldskipevent = True
    if shouldskipevent: 
        print ientry, 'acme mismatch'
        continue
        

    genjets_.clear()
    if not isdata:
        for ijet, jet in enumerate(c.GenJets):
            #if not jet.Pt()>15: continue
            #if not abs(jet.Eta())<5: continue
            ujet = UsefulJet(jet, 0, 0, -1)
            closestAcme = getClosestObject(acme_objects, ujet, 0.1)
            if ujet.DeltaR(closestAcme)<0.1: 
                if sayalot: print 'ueberspringen jet mit pT, eta', tlvjet.Pt(), tlvjet.Eta(), '(',tlvjet.DeltaR(acme_objects[0]),')'
                continue
            genjets_.push_back(ujet.tlv)
    gHt = getHt(genjets_,AnHardMetJetPtCut)
    gHt = gHt
    fillth1(hHt, gHt,1)

    matchedBtagscoreVec = createMatchedBtagscoreVector(genjets_, recojets)
    genjets = CreateUsefulJetVector(genjets_, matchedBtagscoreVec)

    ##a few global objects
    MetVec = TLorentzVector()
    MetVec.SetPtEtaPhiE(c.MET,0,c.METPhi,c.MET)

    #CleanMetVec = TLorentzVector()
    #CleanMetVec.SetPtEtaPhiE(c.METclean,0,c.METPhiclean,c.METclean)
    #redirtiedMetVec = CleanMetVec.Clone()
    #redirtiedMetVec-=AcmeVector 

    ##observed histogram
    tHt = getHt(recojets,AnHardMetJetPtCut)
    tHt = tHt
    #for obj in acme_objects: tHt+=obj.Pt()
    tHardMhtVec = getHardMet(recojets,AnHardMetJetPtCut, mhtjetetacut)
    tHardMetVec = tHardMhtVec.Clone()
    tHardMetVec-=AcmeVector # this still needed because the reco-jets don't contain the acme_objects

    
    tHardMetPt, tHardMetPhi = tHardMetVec.Pt(), tHardMetVec.Phi()
    HardMETPt[0], HardMETPhi[0] = tHardMetPt, tHardMetPhi
    
    #if  not abs(MetVec.Pt()-tHardMetVec.Pt())<60: continue
    
    tHardMhtPt, tHardMhtPhi = tHardMhtVec.Pt(), tHardMhtVec.Phi()
    
    mindphi = 4
    for jet in recojets[:4]: mindphi = min(mindphi, abs(jet.DeltaPhi(tHardMetVec)))

    if tHt>0: tMetSignificance = tHardMetPt/TMath.Sqrt(tHt)
    else: tMetSignificance = 99
    tNJets = countJets(recojets,AnHardMetJetPtCut)
    tBTags = countBJets(recojets,AnHardMetJetPtCut)

    if debugmode:
        if not tHardMetPt>100 and tHardMetPt<met4skim: continue

    fv = [tHt,c.MET,tNJets,tBTags,mindphi, int(recophotons.size()),10]

    if tHardMetPt>met4skim: 
        print ientry, 'fv', fv
        
    fitsucceed = RebalanceJets(recojets)
    rebalancedJets = _Templates_.dynamicJets

                  
    mHt = getHt(rebalancedJets,AnHardMetJetPtCut)
    mHt = mHt
    for obj in acme_objects: mHt+=obj.Pt()
    mHardMetVec = getHardMet(rebalancedJets,AnHardMetJetPtCut, mhtjetetacut)
    mHardMetVec-=AcmeVector # this is now done because the acme_objects were stuck back into the reblanced jets
    mHardMetPt, mHardMetPhi = mHardMetVec.Pt(), mHardMetVec.Phi()
    if mHt>0: mMetSignificance = mHardMetPt/TMath.Sqrt(mHt)
    else: mMetSignificance = 8	

    mNJets = countJets(rebalancedJets,AnHardMetJetPtCut)
    #for obj in acme_objects: 
    #    if obj.Pt()>30 and abs(obj.Eta())<2.4:
    #        mNJets+=1
        
    mBTags = countBJets(rebalancedJets,AnHardMetJetPtCut)###


    fitsucceed = (fitsucceed and mHardMetPt<rebalancedMetCut)# mHardMetPt>min(mHt/2,180):# was 160	

    #redoneMET = redoMET(MetVec,recojets,rebalancedJets)
    #mMetPt,mMetPhi = redoneMET.Pt(), redoneMET.Phi()
    mindphi = 4
    for jet in rebalancedJets[:4]: mindphi = min(mindphi, abs(jet.DeltaPhi(mHardMetVec)))
    fv = [mHt,mHardMetPt,mNJets,mBTags,mindphi, int(recophotons.size()),mMetSignificance]

    fillth1(hTotFit, fv[3], weight)

    if fitsucceed: fillth1(hPassFit, fv[3], weight)

    nsmears = 20*bootupfactor
    if isdata: weight = 1.0 / nsmears
    else: weight = c.puWeight * c.CrossSection / nsmears

    if mktree:
        jetsRandS.clear()
        jetsRandS_origIdx.clear()
        BTagsDeepCSV.clear()
        jetsRebalanced.clear()
        HTRandS[0] = 0
        HardMETPtRandS[0] = 0
        HardMETPhiRandS[0] = 0
        NJetsRandS[0] = 0
        BTagsRandS[0] = 0
        NSmearsPerEvent[0] = 0
    for i in range(nsmears):

        if (not fitsucceed) and IsUniqueSeed[0] == 0: 
            tree_out.Fill()
            break

        RplusSJets = smearJets(rebalancedJets,99+_Templates_.nparams)
        for acme in acme_objects:
            RplusSJets.push_back(acme)        
        rpsHt = getHt(RplusSJets,AnHardMetJetPtCut)
        rpsHt = rpsHt
        #for obj in acme_objects: rpsHt+=obj.Pt()
        rpsHardMetVec = getHardMet(RplusSJets,AnHardMetJetPtCut, mhtjetetacut)
        #rpsHardMetVec-=AcmeVector # this is now done because the acme_objects were stuck back into the R&S jets
        rpsHardMetPt, rpsHardMetPhi = rpsHardMetVec.Pt(), rpsHardMetVec.Phi()
        if rpsHt>0: rpsMetSignificance = rpsHardMetPt/TMath.Sqrt(rpsHt)
        else: rpsMetSignificance = 8			
        rpsNJets = countJets(RplusSJets,AnHardMetJetPtCut)
        rpsBTags = countBJets(RplusSJets,AnHardMetJetPtCut)
        mindphi = 4
        for jet in RplusSJets[:4]: mindphi = min(mindphi, abs(jet.DeltaPhi(rpsHardMetVec)))
        fv = [rpsHt,rpsHardMetPt,rpsNJets,rpsBTags,mindphi, int(recophotons.size()),rpsMetSignificance]
        
        if mktree:
            if fv[1]>met4skim or tHardMetPt>met4skim:
                for ijet, jet in enumerate(RplusSJets):
                    jetsRandS.push_back(jet.tlv)
                    BTagsDeepCSV.push_back(jet.btagscore)
                    jetsRandS_origIdx.push_back(jet.OriginalIdx())
                for ijet, jet in enumerate(rebalancedJets):
                    jetsRebalanced.push_back(jet.tlv)
                    jetsRebalanced_origIdx.push_back(jet.OriginalIdx())
                HTRandS[0] = fv[0]
                HardMETPtRandS[0] = fv[1]
                HardMETPhiRandS[0] = rpsHardMetPhi
                NJetsRandS[0] = fv[2]
                BTagsRandS[0] = fv[3]
                NSmearsPerEvent[0] = nsmears   
                FitSucceed[0] = fitsucceed             
                tree_out.Fill()
                IsUniqueSeed[0] = 0

    if isdata: continue

    continue

    ##gen smearing studies and so forth
    genMetVec = mkmet(c.GenMET, c.GenMETPhi)    
    weight = c.CrossSection

    gHt = getHt(genjets,AnHardMetJetPtCut)
    gHt = gHt
    #for obj in acme_objects: gHt+=obj.Pt()

    gHardMetVec = getHardMet(genjets,AnHardMetJetPtCut, mhtjetetacut)
    tmpgmet = gHardMetVec.Pt()
    gHardMetVec-=AcmeVector
    if sayalot: print 'gen mht after/before', gHardMetVec.Pt()/tmpgmet
    gHardMetPt, gHardMetPhi = gHardMetVec.Pt(), gHardMetVec.Phi()
    if gHt>0: gMetSignificance = gHardMetPt/TMath.Sqrt(gHt)
    else: gMetSignificance = 8	

        
    ###Delphes filter, because I think Delphes is mis-computing its own gen MET
    if gHardMetPt>80 and False: 
        fillth1(hGenMetGenHardMetRatio,abs(gHardMetPt-genMetVec.Pt())/gHardMetPt)
        if abs(gHardMetPt-genMetVec.Pt())/gHardMetPt>0.5: 
            print 'skipping', ientry, gHardMetPt, genMetVec.Pt()
            continue
    ###Delphes

    mindphi = 4
    for jet in genjets[:4]: mindphi = min(mindphi, abs(jet.DeltaPhi(gHardMetVec)))
        
    gNJets = countJets(genjets,AnHardMetJetPtCut)
    gBTags = countBJets(genjets,AnHardMetJetPtCut)

    fv = [gHt,gHardMetPt,gNJets,gBTags,mindphi, int(recophotons.size()),gMetSignificance]	

        
fnew.cd()
fnew.cd('../')
#writeHistoStruct(histoStructDict)
#hGenMetGenHardMetRatio.Write()
hHt.Write()
hHtWeighted.Write()

hPassFit.Write()
hTotFit.Write()
if mktree:
    fnew.cd('TreeMaker2')
    tree_out.Write()
print 'just created', fnew.GetName()
fnew.Close()



