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
met4skim = 80
mhtjetetacut = 5.0 # also needs be be changed in UsefulJet.h
lhdHardMetJetPtCut = 15.0
AnHardMetJetPtCut = 30.0
rebalancedMetCut = 125
useMediumPho = False


sayalot = False
nametag = {'Nom':'', 'Up': 'JerUp'}


mvaversion = 2

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
parser.add_argument("-printevery", "--printevery", type=int, default=1000,help="short run")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile_,help="file")
parser.add_argument("-bootstrap", "--bootstrap", type=str, default='0',help="boot strapping (0,1of5,2of5,3of5,...)")
parser.add_argument("-smears", "--smears", type=int, default=20,help="number smears per event")
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
smears = args.smears
JerUpDown = args.JerUpDown
forcetemplates = args.forcetemplates
verbosity = args.verbosity
printevery = args.printevery
debugmode = args.debugmode
printevery = args.printevery
quickrun = args.quickrun
sayalot = args.sayalot



debugmode = False

llhdHardMetThresh = 15
mktree = True



#stuff for Matt's BDT
reader = TMVA.Reader()
_Ngoodjets_ = array('f',[0])
_ST_ = array('f',[0])
_Pt_jets_ = array('f',[0])
_dPhi_GG_ = array('f',[0])
_Photons0Et_ = array('f',[0])
_Photons1Et_ = array('f',[0])
_HardMET_ = array('f',[0])
_Pt_GG_ = array('f',[0])
_ST_jets_ = array('f',[0])
_min_dPhi_ = array('f',[0])
_dPhi_GGHardMET_ = array('f',[0])
if mvaversion==2:
    prefix = 'mva_'
    reader.AddVariable(prefix+"Ngoodjets",_Ngoodjets_)      
    reader.AddVariable(prefix+"ST",_ST_)          
    reader.AddVariable(prefix+"Pt_jets",_Pt_jets_)
    reader.AddVariable(prefix+"dPhi_GG",_dPhi_GG_)
    reader.AddVariable(prefix+"Photons0Et",_Photons0Et_)
    reader.AddVariable(prefix+"Photons1Et",_Photons1Et_)
    reader.AddVariable(prefix+"HardMET",_HardMET_)
    reader.AddVariable(prefix+"Pt_GG",_Pt_GG_)
    reader.AddVariable(prefix+"ST_jets",_ST_jets_)
    reader.AddVariable(prefix+"min_dPhi",_min_dPhi_)
    reader.AddVariable(prefix+"dPhi_GGHardMET",_dPhi_GGHardMET_)
else:
    prefix = ''
    reader.AddVariable(prefix+"Ngoodjets",_Ngoodjets_)      
    reader.AddVariable(prefix+"ST",_ST_)          
    reader.AddVariable(prefix+"Pt_jets",_Pt_jets_)
    reader.AddVariable(prefix+"dPhi_GG",_dPhi_GG_)
    reader.AddVariable(prefix+"Photons[0].Et()",_Photons0Et_)
    reader.AddVariable(prefix+"Photons[1].Et()",_Photons1Et_)
    reader.AddVariable(prefix+"HardMET",_HardMET_)
    reader.AddVariable(prefix+"Pt_GG",_Pt_GG_)
    reader.AddVariable(prefix+"ST_jets",_ST_jets_)
    reader.AddVariable(prefix+"min_dPhi",_min_dPhi_)
    reader.AddVariable(prefix+"dPhi_GGHardMET",_dPhi_GGHardMET_)        
#reader.BookMVA("BDT", 'usefulthings/TMVAClassification_BDT.weights_MJMay2020.xml')
reader.BookMVA("BDT", 'usefulthings/bdt_RandS_2016-17_HardMETPt90cut_nobarrelcut.xml')
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
#################        root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/
''' ususally did something like this: 
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2*/*/*.root > usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2016/*/*/*.root >> usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2017/*/*/*.root >> usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2018/*/*/*.root >> usefulthings/filelistDiphotonBig.txt
'''

ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/'
fnamefilename = 'usefulthings/filelistDiphoton.txt'
fnamefilename = 'usefulthings/filelistDiphotonBig.txt'
if not 'DoubleEG' in fnamekeyword:
    if 'Summer16v3.QCD_HT' in fnamekeyword or 'Summer16v3.WGJets_MonoPhoton' in fnamekeyword: #or 'Run20' in fnamekeyword
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
    if ('Summer16v3.QCD_HT' in fnamekeyword or 'Summer16v3.WGJets_MonoPhoton' in fnamekeyword): fname = ra2bspace+fname
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
    tree_out.SetBranchStatus('HT',0)
    tree_out.SetBranchStatus('NJets',0)    
    tree_out.SetBranchStatus('BTags',0)
    tree_out.SetBranchStatus('Jets',0)
    tree_out.SetBranchStatus('Jets_bJetTagDeepCSVBvsAll',0)    


    print 'cloned tree'    


    HardMETPt = np.zeros(1, dtype=float)
    tree_out.Branch('HardMETPt', HardMETPt, 'HardMETPt/D')
    HardMETPhi = np.zeros(1, dtype=float)
    tree_out.Branch('HardMETPhi', HardMETPhi, 'HardMETPhi/D')
    MinDPhiHardMetJets = np.zeros(1, dtype=float)
    tree_out.Branch('MinDPhiHardMetJets', MinDPhiHardMetJets, 'MinDPhiHardMetJets/D')
    Pho1_hadTowOverEM = np.zeros(1, dtype=float)    
    tree_out.Branch('Pho1_hadTowOverEM', Pho1_hadTowOverEM, 'Pho1_hadTowOverEM/D')
    Pho2_hadTowOverEM = np.zeros(1, dtype=float)    
    tree_out.Branch('Pho2_hadTowOverEM', Pho2_hadTowOverEM, 'Pho2_hadTowOverEM/D')    
    NPhotonsLoose = np.zeros(1, dtype=int)
    mass_GG = np.zeros(1, dtype=float)
    tree_out.Branch('mass_GG', mass_GG, 'mass_GG/D')    
    tree_out.Branch('NPhotonsLoose', NPhotonsLoose, 'NPhotonsLoose/I')
    NPhotonsMedium = np.zeros(1, dtype=int)
    tree_out.Branch('NPhotonsMedium', NPhotonsMedium, 'NPhotonsMedium/I')


    HardMetMinusMet = np.zeros(1, dtype=float)
    tree_out.Branch('HardMetMinusMet', HardMetMinusMet, 'HardMetMinusMet/D')

    IsUniqueSeed = np.zeros(1, dtype=int)
    tree_out.Branch('IsUniqueSeed', IsUniqueSeed, 'IsUniqueSeed/I')

    JetsAUX = ROOT.std.vector('TLorentzVector')()
    tree_out.Branch('JetsAUX', JetsAUX)

    jetsRebalanced = ROOT.std.vector('TLorentzVector')()
    tree_out.Branch('JetsRebalanced', jetsRebalanced)

    JetsAUX_bJetTagDeepCSVBvsAll = ROOT.std.vector('float')()
    tree_out.Branch('Jets_bJetTagDeepCSVBvsAll', JetsAUX_bJetTagDeepCSVBvsAll)

    HTAUX = np.zeros(1, dtype=float)
    NJetsAUX = np.zeros(1, dtype=int)
    BTagsAUX = np.zeros(1, dtype=int)
    NSmearsPerEvent = np.zeros(1, dtype=int)
    IsRandS = np.zeros(1, dtype=int)
    NOrigJets15 = np.zeros(1, dtype=int)    

    FitSucceed = np.zeros(1, dtype=int)    
    tree_out.Branch('HTAUX', HTAUX, 'HTAUX/D')
    tree_out.Branch('BTagsAUX', BTagsAUX, 'BTagsAUX/I')
    tree_out.Branch('NJetsAUX', NJetsAUX, 'NJetsAUX/I')
    tree_out.Branch('NSmearsPerEvent', NSmearsPerEvent, 'NSmearsPerEvent/I')
    tree_out.Branch('FitSucceed', FitSucceed, 'FitSucceed/I')   
    tree_out.Branch('IsRandS', IsRandS, 'IsRandS/I')  
    tree_out.Branch('NOrigJets15', NOrigJets15, 'NOrigJets15/I')           



    mva_Ngoodjets = np.zeros(1, dtype=float)
    tree_out.Branch('mva_Ngoodjets', mva_Ngoodjets, 'mva_Ngoodjets/D')
    mva_ST = np.zeros(1, dtype=float)
    tree_out.Branch('mva_ST', mva_ST, 'mva_ST/D')    
    mva_Pt_jets = np.zeros(1, dtype=float)
    tree_out.Branch('mva_Pt_jets', mva_Pt_jets, 'mva_Pt_jets/D')
    mva_dPhi_GG = np.zeros(1, dtype=float)
    tree_out.Branch('mva_dPhi_GG', mva_dPhi_GG, 'mva_dPhi_GG/D')
    mva_Photons0Et = np.zeros(1, dtype=float)
    tree_out.Branch('mva_Photons0Et', mva_Photons0Et, 'mva_Photons0Et/D')    
    mva_Photons1Et = np.zeros(1, dtype=float)
    tree_out.Branch('mva_Photons1Et', mva_Photons1Et, 'mva_Photons1Et/D')    
    mva_HardMET = np.zeros(1, dtype=float)
    tree_out.Branch('mva_HardMET', mva_HardMET, 'mva_HardMET/D')
    mva_Pt_GG = np.zeros(1, dtype=float)
    tree_out.Branch('mva_Pt_GG', mva_Pt_GG, 'mva_Pt_GG/D')    
    mva_ST_jets = np.zeros(1, dtype=float)
    tree_out.Branch('mva_ST_jets', mva_ST_jets, 'mva_ST_jets/D')    
    mva_min_dPhi = np.zeros(1, dtype=float)
    tree_out.Branch('mva_min_dPhi', mva_min_dPhi, 'mva_min_dPhi/D')    
    mva_dPhi_GGHardMET = np.zeros(1, dtype=float)
    tree_out.Branch('mva_dPhi_GGHardMET', mva_dPhi_GGHardMET, 'mva_dPhi_GGHardMET/D') 
    mva_BDT = np.zeros(1, dtype=float)
    tree_out.Branch('mva_BDT', mva_BDT, 'mva_BDT/D')



print 'n(entries) =', n2process

hHt = TH1F('hHt','hHt',120,0,2500)
hHt.Sumw2()
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',120,0,2500)
hHtWeighted.Sumw2()
hfilterfails = TH1F('hfilterfails','hfilterfails',14,-14,0)
tcounter = TTree('tcounter','tcounter')

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
        #if not ientry>102000 and ientry < 112850: continue
        if not ientry in [102850]: continue


    if ientry>nentries: break
    c.GetEntry(ientry)
    tcounter.Fill()
    IsUniqueSeed[0] = 1

    if isdata:  weight = 1.0
    else:  weight = c.CrossSection

    if passesUniversalSelection(c)<0: 
        if len(c.Photons)>1: hfilterfails.Fill(passesUniversalSelection(c))
        continue
    elif len(c.Photons)>1: hfilterfails.Fill(0)
    #if not passesHadronicSusySelection(c): continue
    if not len(c.Photons)>1: continue


    acme_objects.clear()
    recophotons_loose.clear()
    recophotons_loose_hoe = []
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
        recophotons_loose_hoe.append(c.Photons_hadTowOverEM[ipho])
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

    if useMediumPho: 
        recophotons = recophotons_medium
        print 'this is going to crash :)'
    else: 
        recophotons = recophotons_loose
        recophotons_hoe = recophotons_loose_hoe

#    if not len(c.Photons)==recophotons.size():
#        print ientry, 'this is important'
#        continue

    if not len(recophotons_loose)>1: continue
    NPhotonsLoose[0] = len(recophotons_loose)
    NPhotonsMedium[0] = len(recophotons_medium)    

    if not int(recophotons.size())>1: continue

    dphiGG = recophotons[0].DeltaPhi(recophotons[1])

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

    recojets_.clear()
    for ijet, jet in enumerate(c.Jets):
        if not (jet.Pt()>2 and abs(jet.Eta())<5.0): continue
        recojets_.push_back(UsefulJet(jet, c.Jets_bJetTagDeepCSVBvsAll[ijet], float(int(bool(c.Jets_ID[ijet]))), ijet))



    if is2017: # ecal noise treatment
        recojets_.clear()
        for ijet, jet in enumerate(c.Jets):
            if not (jet.Pt()>2 and abs(jet.Eta())<5.0): continue
            if abs(jet.Eta())>2.65 and abs(jet.Eta()) < 3.139 and jet.Pt()/c.Jets_jecFactor[ijet]<50: continue #/c.Jets_jerFactor[ijet]
            recojets_.push_back(UsefulJet(jet, c.Jets_bJetTagDeepCSVBvsAll[ijet], jet.Pt()))  


    ##declare empty vector of UsefulJets (in c++, std::vector<UsefulJet>):
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
            if jet.DeltaR(closestAcme)<0.3:
                nMatchedAcmeInnerPairs+=1
                if sayalot: print 'skipping reco jet with pT, eta', jet.Pt(), jet.Eta(), jet.DeltaR(acme_objects[0].tlv)
                continue
        if jet.Pt()>AnHardMetJetPtCut and jet.JetId()<0.5: 
            passesJetId = False
            break
        ujet = UsefulJet(jet.tlv, jet.btagscore, jet.jetId, jet.originalIdx)
        recojets.push_back(ujet)

    if not passesJetId: 
        print 'failed jet ID'
        continue

    shouldskipevent = False
    if not nMatchedAcmeOuterPairs==nMatchedAcmeInnerPairs: 
        shouldskipevent = True    
    if not nMatchedAcmeInnerPairs==len(acme_objects): 
        shouldskipevent = True
    if shouldskipevent: 
        print ientry, 'acme mismatch'
        continue

    print 'but we prevail sometimes'
    if not isdata:
        genjets_.clear()
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
        matchedBtagscoreVec = createMatchedBtagscoreVector(genjets_, recojets)
        genjets = CreateUsefulJetVector(genjets_, matchedBtagscoreVec)    

    fillth1(hHt, c.HT,1)

    ##a few global objects
    MetVec = TLorentzVector()
    MetVec.SetPtEtaPhiE(c.MET,0,c.METPhi,c.MET)

    #CleanMetVec = TLorentzVector()
    #CleanMetVec.SetPtEtaPhiE(c.METclean,0,c.METPhiclean,c.METclean)
    #redirtiedMetVec = CleanMetVec.Clone()
    #redirtiedMetVec-=AcmeVector 

    ##observed histogram
    tHt = getHt(recojets,AnHardMetJetPtCut)
    tSt = tHt
    for obj in acme_objects: tSt+=obj.Pt()
    tHardMhtVec = getHardMet(recojets,AnHardMetJetPtCut, mhtjetetacut)
    tHardMetVec = tHardMhtVec.Clone()
    tHardMetVec-=AcmeVector # this still needed because the reco-jets don't contain the acme_objects

    

    tHardMetPt, tHardMetPhi = tHardMetVec.Pt(), tHardMetVec.Phi()
    HardMETPt[0], HardMETPhi[0] = tHardMetPt, tHardMetPhi

    tjets_pt = tHardMhtVec.Clone()
    tjets_pt*=-1

    mass_GG[0] = (recophotons[0]+recophotons[1]).M()        
    Pho1_hadTowOverEM[0], Pho2_hadTowOverEM[0] = recophotons_hoe[0], recophotons_hoe[1]

    #if  not abs(MetVec.Pt()-tHardMetVec.Pt())<60: continue
    HardMetMinusMet[0] = MetVec.Pt()-tHardMetVec.Pt()

    if tHt>0: tMetSignificance = tHardMetPt/TMath.Sqrt(tHt)
    else: tMetSignificance = 99
    ##tNJets = countJets(recojets,AnHardMetJetPtCut)##these moved below to pick up the acmes again
    ##tBTags = countBJets(recojets,AnHardMetJetPtCut)


    fitsucceed = RebalanceJets(recojets)
    rebalancedJets = _Templates_.dynamicJets


    mHt = getHt(rebalancedJets,AnHardMetJetPtCut)
    mSt = mHt
    for obj in acme_objects: 
        mSt+=obj.Pt()
        recojets.push_back(obj)##

    sortThatThang(recojets)

    NOrigJets15[0] = len(recojets)    

    tNJets = countJets(recojets,AnHardMetJetPtCut)##these moved to the earliest moment possible
    tBTags = countBJets(recojets,AnHardMetJetPtCut)##these moved to the earliest moment possible
    tmindphi = 4##these moved to the earliest moment possible
    for jet in recojets[:4]: 
        if jet.Pt()>30:
            tmindphi = min(tmindphi, abs(jet.tlv.DeltaPhi(tHardMetVec)))    ##these moved to the earliest moment possible

    mHardMetVec = getHardMet(rebalancedJets,AnHardMetJetPtCut, mhtjetetacut)

    mHardMetVec-=AcmeVector # this is now done because the acme_objects were not stuck back into the reblanced jets
    mHardMetPt, mHardMetPhi = mHardMetVec.Pt(), mHardMetVec.Phi()
    if mHt>0: mMetSignificance = mHardMetPt/TMath.Sqrt(mHt)
    else: mMetSignificance = 8	

    mBTags = countBJets(rebalancedJets,AnHardMetJetPtCut)###

    fitsucceed = (fitsucceed and mHardMetPt<rebalancedMetCut)# mHardMetPt>min(mHt/2,180):# was 160	

    #redoneMET = redoMET(MetVec,recojets,rebalancedJets)
    #mMetPt,mMetPhi = redoneMET.Pt(), redoneMET.Phi()
    mindphi_m = 4
    for jet in rebalancedJets[:4]: 
        if jet.Pt()>30:
            mindphi_m = min(mindphi_m, abs(jet.tlv.DeltaPhi(mHardMetVec)))

    fillth1(hTotFit, mBTags, weight)

    if fitsucceed: fillth1(hPassFit, mBTags, weight)

    for ijet, jet in enumerate(rebalancedJets):
        jetsRebalanced.push_back(jet.tlv)

    nsmears = smears*bootupfactor
    print 'got nsmears', nsmears
    if isdata: weight = 1.0/nsmears
    else: weight = c.puWeight * c.CrossSection / nsmears

    if debugmode:
        print 'MET, MHT, HardMet', c.MET, c.MHT, tHardMetVec.Pt()
        print 'recojets:'
        for ijet, jet in enumerate(recojets):
            print ientry, ijet, jet.Pt()
        print 'acmes:'  
        for iobj, obj in enumerate(acme_objects):      
            print iobj, obj, obj.Pt()
        print ientry, 'tHardMetVec.DeltaPhi(recophotons[0]+recophotons[1])', tHardMetVec.DeltaPhi(recophotons[0]+recophotons[1])

    if mktree and tHardMetPt>met4skim:

            IsRandS[0] = 0 
            JetsAUX.clear()
            JetsAUX_bJetTagDeepCSVBvsAll.clear()
            for ijet, jet in enumerate(c.Jets):
                JetsAUX.push_back(jet)
                JetsAUX_bJetTagDeepCSVBvsAll.push_back(c.Jets_bJetTagDeepCSVBvsAll[ijet])

            HTAUX[0] = c.HT
            NJetsAUX[0] = c.NJets
            BTagsAUX[0] = c.BTags

            HardMETPt[0] = tHardMetPt
            HardMETPhi[0] = tHardMetPhi
            MinDPhiHardMetJets[0] = tmindphi
            NSmearsPerEvent[0] = nsmears
            mva_Ngoodjets[0] = tNJets - NPhotonsLoose[0]#
            mva_ST[0] = tSt##
            mva_Pt_jets[0] = tjets_pt.Pt()#
            mva_dPhi_GG[0] = dphiGG#
            mva_Photons0Et[0] = recophotons[0].Pt()#
            mva_Photons1Et[0] = recophotons[1].Pt()#
            mva_HardMET[0] = tHardMetVec.Pt()
            mva_Pt_GG[0] = (recophotons[0]+recophotons[1]).Pt()#
            mva_ST_jets[0] = tHt#
            mva_min_dPhi[0] = tmindphi#
            mva_dPhi_GGHardMET[0] = tHardMetVec.DeltaPhi(recophotons[0]+recophotons[1])#
            _Ngoodjets_[0] = mva_Ngoodjets[0]
            _ST_[0] = mva_ST[0]
            _Pt_jets_[0] = mva_Pt_jets[0]
            _dPhi_GG_[0] = mva_dPhi_GG[0]
            _Photons0Et_[0] = mva_Photons0Et[0]
            _Photons1Et_[0] = mva_Photons1Et[0]
            _HardMET_[0] = mva_HardMET[0]
            _Pt_GG_[0] = mva_Pt_GG[0]
            _ST_jets_[0] = mva_ST_jets[0]
            _min_dPhi_[0] = mva_min_dPhi[0]
            _dPhi_GGHardMET_[0] = mva_dPhi_GGHardMET[0]
            mva_BDT[0] = reader.EvaluateMVA("BDT")
            tree_out.Fill()            
            IsUniqueSeed[0] = 0            



    for i in range(nsmears):

        if (not fitsucceed): break

        RplusSJets = smearJets(rebalancedJets,99+_Templates_.nparams)
        rpsHt = getHt(RplusSJets,AnHardMetJetPtCut)
        rpsSt = rpsHt
        for obj in acme_objects: rpsSt+=obj.Pt()

        rps_jets_pt = getHardMet(RplusSJets,AnHardMetJetPtCut, mhtjetetacut)
        rps_jets_pt*=-1

        for acme in acme_objects: RplusSJets.push_back(acme)

        sortThatThang(RplusSJets)
        if len(RplusSJets)>3:
            print ientry, RplusSJets[0].Pt(),RplusSJets[1].Pt(),RplusSJets[2].Pt(),RplusSJets[3].Pt()
            print 'nparams was', _Templates_.nparams

        rpsHardMetVec = getHardMet(RplusSJets,AnHardMetJetPtCut, mhtjetetacut)
        #rpsHardMetVec-=AcmeVector # this is now done because the acme_objects were stuck back into the R&S jets
        rpsHardMetPt, rpsHardMetPhi = rpsHardMetVec.Pt(), rpsHardMetVec.Phi()
        if rpsHt>0: rpsMetSignificance = rpsHardMetPt/TMath.Sqrt(rpsHt)
        else: rpsMetSignificance = 8			
        rpsNJets = countJets(RplusSJets,AnHardMetJetPtCut)
        rpsBTags = countBJets(RplusSJets,AnHardMetJetPtCut)
        rpsmindphi = 4
        for jet in RplusSJets[:4]: 
            if jet.Pt()>30:
                rpsmindphi = min(rpsmindphi, abs(jet.tlv.DeltaPhi(rpsHardMetVec)))

        if mktree:
            if rpsHardMetPt>met4skim:

                if IsUniqueSeed[0]==1:

                    JetsAUX.clear()
                    JetsAUX_bJetTagDeepCSVBvsAll.clear()
                    for ijet, jet in enumerate(c.Jets):
                        JetsAUX.push_back(jet)
                        JetsAUX_bJetTagDeepCSVBvsAll.push_back(c.Jets_bJetTagDeepCSVBvsAll[ijet])                    
                    #do things like they're not RandS
                    IsRandS[0] = 0 
                    HTAUX[0] = c.HT
                    HardMETPt[0] = tHardMetPt
                    HardMETPhi[0] = tHardMetPhi
                    MinDPhiHardMetJets[0] = tmindphi
                    NJetsAUX[0] = c.NJets
                    BTagsAUX[0] = c.BTags
                    NSmearsPerEvent[0] = nsmears
                    mva_Ngoodjets[0] = tNJets - NPhotonsLoose[0]#
                    mva_ST[0] = tSt##
                    mva_Pt_jets[0] = tjets_pt.Pt()#
                    mva_dPhi_GG[0] = dphiGG#
                    mva_Photons0Et[0] = recophotons[0].Pt()#
                    mva_Photons1Et[0] = recophotons[1].Pt()#
                    mva_HardMET[0] = tHardMetVec.Pt()
                    mva_Pt_GG[0] = (recophotons[0]+recophotons[1]).Pt()#
                    mva_ST_jets[0] = tHt#
                    mva_min_dPhi[0] = tmindphi#
                    mva_dPhi_GGHardMET[0] = tHardMetVec.DeltaPhi(recophotons[0]+recophotons[1])#

                    _Ngoodjets_[0] = mva_Ngoodjets[0]
                    _ST_[0] = mva_ST[0]
                    _Pt_jets_[0] = mva_Pt_jets[0]
                    _dPhi_GG_[0] = mva_dPhi_GG[0]
                    _Photons0Et_[0] = mva_Photons0Et[0]
                    _Photons1Et_[0] = mva_Photons1Et[0]
                    _HardMET_[0] = mva_HardMET[0]
                    _Pt_GG_[0] = mva_Pt_GG[0]
                    _ST_jets_[0] = mva_ST_jets[0]
                    _min_dPhi_[0] = mva_min_dPhi[0]
                    _dPhi_GGHardMET_[0] = mva_dPhi_GGHardMET[0]
                    mva_BDT[0] = reader.EvaluateMVA("BDT")
                    print 'got bdt', mva_BDT[0], mva_HardMET[0]
                    tree_out.Fill()
                    IsUniqueSeed[0] = 0

                if True:

                    JetsAUX.clear()
                    JetsAUX_bJetTagDeepCSVBvsAll.clear()
                    for ijet, jet in enumerate(RplusSJets):
                        JetsAUX.push_back(jet.tlv)
                        JetsAUX_bJetTagDeepCSVBvsAll.push_back(jet.btagscore) 

                    #do things like they are RandS
                    IsRandS[0] = 1 

                    HTAUX[0] = rpsHt
                    NJetsAUX[0] = rpsNJets
                    BTagsAUX[0] = rpsBTags

                    HardMETPt[0] = rpsHardMetPt
                    HardMETPhi[0] = rpsHardMetPhi
                    MinDPhiHardMetJets[0] = rpsmindphi
                    NSmearsPerEvent[0] = nsmears
                    FitSucceed[0] = fitsucceed     
                    mva_Ngoodjets[0] = rpsNJets  - NPhotonsLoose[0]
                    mva_ST[0] = rpsSt
                    mva_Pt_jets[0] = rps_jets_pt.Pt()
                    mva_dPhi_GG[0] = dphiGG
                    mva_Photons0Et[0] = recophotons[0].Pt()
                    mva_Photons1Et[0] = recophotons[1].Pt()
                    mva_HardMET[0] = rpsHardMetPt
                    mva_Pt_GG[0] = (recophotons[0]+recophotons[1]).Pt()
                    mva_ST_jets[0] = rpsHt
                    mva_min_dPhi[0] = rpsmindphi
                    mva_dPhi_GGHardMET[0] = rpsHardMetVec.DeltaPhi(recophotons[0]+recophotons[1])

                    _Ngoodjets_[0] = mva_Ngoodjets[0]
                    _ST_[0] = mva_ST[0]
                    _Pt_jets_[0] = mva_Pt_jets[0]
                    _dPhi_GG_[0] = mva_dPhi_GG[0]
                    _Photons0Et_[0] = mva_Photons0Et[0]
                    _Photons1Et_[0] = mva_Photons1Et[0]
                    _HardMET_[0] = mva_HardMET[0]
                    _Pt_GG_[0] = mva_Pt_GG[0]
                    _ST_jets_[0] = mva_ST_jets[0]
                    _min_dPhi_[0] = mva_min_dPhi[0]
                    _dPhi_GGHardMET_[0] = mva_dPhi_GGHardMET[0]
                    mva_BDT[0] = reader.EvaluateMVA("BDT")
                    print 'got bdt rands', mva_BDT[0], mva_HardMET[0]
                    tree_out.Fill()


    if isdata: continue


fnew.cd()
fnew.cd('../')
#writeHistoStruct(histoStructDict)
#hGenMetGenHardMetRatio.Write()
hHt.Write()
hHtWeighted.Write()
hfilterfails.Write()
tcounter.Write()

hPassFit.Write()
hTotFit.Write()
if mktree:
    fnew.cd('TreeMaker2')
    tree_out.GetBranch("NJetsAUX").SetName("NJets")    
    tree_out.Write()
print 'just created', fnew.GetName()
fnew.Close()



'''
tree->GetBranch("xxx")->SetName("yyy");
tree->GetLeaf("xxx")->SetTitle("yyy");
'''
