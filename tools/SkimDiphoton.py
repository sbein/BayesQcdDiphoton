#Welcome to the industrial age of Sam's rebalance and smear code. You're going to have a lot of fun!
import os,sys
from ROOT import *
from array import array
from glob import glob
from utils import *
import numpy as np
#from ra2blibs import *
import time as thyme

###stuff that would be nice in a config file:
met4skim = 100
mhtjetetacut = 5.0 # also needs be be changed in UsefulJet.h
AnHardMetJetPtCut = 30.0
rebalancedMetCut = 150

photonWp = 'Medium' ###was used for N-1
photonWp = 'Loose'

#tools/SkimDiphoton.py
#tools/DrawAnalylze.py

nametag = {'Nom':'', 'Up': 'JerUp'}

##load in UsefulJet class, which the rebalance and smear code uses
gROOT.ProcessLine(open('src/UsefulJet.cc').read())
exec('from ROOT import *')
gROOT.ProcessLine(open('src/BayesRandS.cc').read())
exec('from ROOT import *')

'''
python tools/SkimDiphoton.py --fnamekeyword Summer16v3.WGJets --smears 10 --quickrun True
'''

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
parser.add_argument("-muversion", "--muversion", type=bool, default=False,help="short run")
parser.add_argument("-poofmu", "--poofmu", type=bool, default=False, help="for poofing muons")
parser.add_argument("-poofe", "--poofe", type=bool, default=False, help="for poofing electrons")
parser.add_argument("-sayalot", "--sayalot", type=bool, default=False,help="short run")
parser.add_argument("-directoryout", "--directoryout", type=bool, default=False,help="only used in submitjobs.py")


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
muversion = args.muversion
poofmu = args.poofmu
poofe = args.poofe
printevery = args.printevery
quickrun = args.quickrun
sayalot = args.sayalot

if poofmu or poofe:
    met4skim = 0.0

if 'DYJets' in fnamekeyword or 'TTJets' in fnamekeyword: met4skim = 30


debugmode = False
mktree = True


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

inf = 999999
if 'TTJets_TuneC' in fnamekeyword:  madranges = [(0,600)]
elif 'TTJets_HT' in fnamekeyword: madranges = [(600,inf)]
elif 'WJetsToLNu_TuneC' in fnamekeyword: madranges = [(0, 100)]
elif 'WJetsToLNu_HT' in fnamekeyword: madranges = [(100, inf)]
elif 'DYJetsToLL_M-50_TuneC' in fnamekeyword: madranges = [(0, 100)]
elif 'DYJetsToLL_M-50_HT' in fnamekeyword: madranges = [(100, inf)]
else: madranges = [(0, inf)]

if 'Fast' in fnamekeyword: isfast = True
else: isfast = False


if 'Run2016' in fnamekeyword or 'Summer16' in fnamekeyword: 
    BTAG_deepCSV = 0.6324
    is2016 = True
    xmlfilename = "usefulthings/TMVAClassification_BDT_200trees_4maxdepth_T5Wg_m19XX_T6Wg_m17XX_ngenweightedsignal_July28_2021.weights.xml"
    photonSF_file = TFile('usefulthings/Fall17V2_2016_Loose_photons.root')
    photonSF_hist = photonSF_file.Get('EGamma_SF2D')
    #xmlfilename = "usefulthings/TMVAClassification_BDT_200trees_4maxdepth.weights.xml"
if 'Run2017' in fnamekeyword or 'Fall17' in fnamekeyword: 
    BTAG_deepCSV = 0.4941
    is2017 = True
    xmlfilename = "usefulthings/TMVAClassification_BDT_200trees_4maxdepth_T5Wg_m19XX_T6Wg_m17XX_ngenweightedsignal_July28_2021.weights.xml"
    photonSF_file = TFile('usefulthings/2017_PhotonsLoose.root')
    photonSF_hist = photonSF_file.Get('EGamma_SF2D')
if 'Run2018' in fnamekeyword or 'Autumn18' in fnamekeyword: 
    BTAG_deepCSV = 0.4184#0.4941####
    is2018 = True
    xmlfilename = "usefulthings/TMVAClassification_BDT_200trees_4maxdepth_T5Wg_m19XX_T6Wg_m17XX_ngenweightedsignal_July28_2021.weights.xml"
    photonSF_file = TFile('usefulthings/2018_PhotonsLoose.root')
    photonSF_hist = photonSF_file.Get('EGamma_SF2D')

#stuff for Matt's BDT
reader = TMVA.Reader()
_Ngoodjets_ = array('i',[0])
_ST_ = array('f',[0])
_Pt_jets_ = array('f',[0])
_dPhi_GG_ = array('f',[0])
_Photons0Et_ = array('f',[0])
_Photons1Et_ = array('f',[0])
_HardMET_ = array('f',[0])
_Pt_GG_ = array('f',[0])
_ST_jets_ = array('f',[0])
_min_dPhi_ = array('f',[0])
_dPhi1_ = array('f',[0])
_dPhi2_ = array('f',[0])
_dPhi_GGHardMET_ = array('f',[0])
_dRjet1photon1_ = array('f',[0])
_dRjet1photon2_ = array('f',[0])
_dRjet2photon1_ = array('f',[0])
_dRjet2photon2_ = array('f',[0])



prefix = 'mva_'
reader.AddSpectator(prefix+"Ngoodjets",_Ngoodjets_)      
#reader.AddVariable(prefix+"ST",_ST_)          
reader.AddVariable(prefix+"Pt_jets/mva_ST",_Pt_jets_)
reader.AddVariable("abs(mva_dPhi_GG)",_dPhi_GG_)
reader.AddVariable(prefix+"Photons0Et/mva_ST",_Photons0Et_)
reader.AddVariable(prefix+"Photons1Et/mva_ST",_Photons1Et_)
reader.AddVariable(prefix+"HardMET/mva_ST",_HardMET_)
reader.AddVariable(prefix+"Pt_GG/mva_ST",_Pt_GG_)
reader.AddVariable(prefix+"ST_jets/mva_ST",_ST_jets_)
reader.AddVariable(prefix+"min_dPhi",_min_dPhi_)
reader.AddVariable(prefix+"dPhi1",_dPhi1_)
reader.AddVariable(prefix+"dPhi2",_dPhi2_)
reader.AddVariable("abs(mva_dPhi_GGHardMET)",_dPhi_GGHardMET_)
reader.AddVariable(prefix+"dRjet1photon1",_dRjet1photon1_)
reader.AddVariable(prefix+"dRjet1photon2",_dRjet1photon2_)
reader.AddVariable(prefix+"dRjet2photon1",_dRjet2photon1_)
reader.AddVariable(prefix+"dRjet2photon2",_dRjet2photon2_)

reader.BookMVA("BDT", xmlfilename)
BTag_Cut = BTAG_deepCSV


issignal = abs('Fast' in fnamekeyword)

#################
# Load in chain #
#################        root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/

'''
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/*.root > usefulthings/filelistDiphoton.txt
python tools/globthemfiles.py
'''

ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/'
fnamefilename = 'usefulthings/filelistDiphoton.txt'
#if not 'DoubleEG' in fnamekeyword:
#    if 'Summer16v3.QCD_HT' in fnamekeyword or 'WJets' in fnamekeyword: #or 'Run20' in fnamekeyword
#        fnamefilename = 'usefulthings/filelistV17.txt'
print 'as file list, using', fnamefilename
fnamefile = open(fnamefilename)
lines = fnamefile.readlines()
shortfname = fnamekeyword.split('/')[-1].strip().replace('*','')
print 'going to check for ', shortfname
fnamefile.close()
c = TChain('TreeMaker2/PreSelection')
filelist = []
for iline, line in enumerate(lines):
    if not shortfname in line: continue
    fname = line.strip()
#    if ('Summer16v3.QCD_HT' in fnamekeyword or 'WJets' in fnamekeyword): fname = ra2bspace+fname# or 'Summer16v3.WGJets_MonoPhoton' in fnamekeyword
    if '/eos/uscms/' in fname:
        fname = fname.replace('/eos/uscms/','root://cmsxrootd.fnal.gov//')
    else:
        fname = fname.replace('/store/','root://cmseos.fnal.gov//store/')
    #if 'WJets' in fnamekeyword: fname = fname.replace('root://cmsxrootd.fnal.gov///store/group/lpcsusyhad','root://hepxrd01.colorado.edu:1094//store/user/aperloff')
    print 'adding', fname
    c.Add(fname)
    filelist.append(fname)
    if quickrun and iline>10: break
n2process = c.GetEntries()
nentries = c.GetEntries()
if quickrun: 
    n2process = min(200000,n2process)


print 'will analyze', n2process, 'events'
c.Show(0)

if issignal:
    c.GetEntry(0)
    par1, par2 = c.SignalParameters





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
if issignal: 
    newname = newname.split('_')[0]+'_m'+str(par1)+'d'+str(par2)+'_time'+str(round(thyme.time()%100000,2))+'.root'

if muversion: newname = newname.replace('.root','_muskim.root')
if poofmu: newname = newname.replace('.root','_poofmu.root')
if poofe: newname = newname.replace('.root', '_poofe.root')
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

    Pho1_SF = np.zeros(1, dtype=float)
    tree_out.Branch('Pho1_SF', Pho1_SF, 'Pho1_SF/D')
    Pho2_SF = np.zeros(1, dtype=float)
    tree_out.Branch('Pho2_SF', Pho2_SF, 'Pho2_SF/D')
    Pho1_SFE = np.zeros(1, dtype=float)
    tree_out.Branch('Pho1_SFE', Pho1_SFE, 'Pho1_SFE/D')
    Pho2_SFE = np.zeros(1, dtype=float)
    tree_out.Branch('Pho2_SFE', Pho2_SFE, 'Pho2_SFE/D')    

   
    NPhotons = np.zeros(1, dtype=int)
    mass_GG = np.zeros(1, dtype=float)
    mass_mumu = np.zeros(1, dtype=float)
    mass_ee = np.zeros(1, dtype=float)
            
    analysisPhotons = ROOT.std.vector('TLorentzVector')()
    tree_out.Branch('analysisPhotons', analysisPhotons)
    analysisPhotons_passWp = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_passWp', analysisPhotons_passWp)
    analysisPhotons_passWpNminus3 = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_passWpNminus3', analysisPhotons_passWpNminus3)
    analysisPhotons_passWpInvertPsv = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_passWpInvertPsv', analysisPhotons_passWpInvertPsv)
    analysisPhotons_passWpInvertSieie = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_passWpInvertSieie', analysisPhotons_passWpInvertSieie)
    analysisPhotons_passWpInvertHoe = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_passWpInvertHoe', analysisPhotons_passWpInvertHoe)    
    analysisPhotons_passWpInvertSieieAndHoe = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_passWpInvertSieieAndHoe', analysisPhotons_passWpInvertSieieAndHoe)
    analysisPhotons_hoe = ROOT.std.vector('double')()
    tree_out.Branch('analysisPhotons_hoe', analysisPhotons_hoe)
    analysisPhotons_sieie = ROOT.std.vector('double')()
    tree_out.Branch('analysisPhotons_sieie', analysisPhotons_sieie)
    analysisPhotons_hasPixelSeed = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_hasPixelSeed', analysisPhotons_hasPixelSeed)
    analysisPhotons_isGenPho = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_isGenPho', analysisPhotons_isGenPho)
    analysisPhotons_isGenEle = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_isGenEle', analysisPhotons_isGenEle)
    analysisPhotons_isGenMu = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_isGenMu', analysisPhotons_isGenMu) 
    analysisPhotons_isGenTau = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_isGenTau', analysisPhotons_isGenTau)     
    analysisPhotons_isGenNone = ROOT.std.vector('int')()
    tree_out.Branch('analysisPhotons_isGenNone', analysisPhotons_isGenNone) 
    
    analysisPhotons_minDrGenEle = ROOT.std.vector('double')()
    tree_out.Branch('analysisPhotons_minDrGenEle', analysisPhotons_minDrGenEle)
    analysisPhotons_minDrRecEle = ROOT.std.vector('double')()
    tree_out.Branch('analysisPhotons_minDrRecEle', analysisPhotons_minDrRecEle)    
    
    
        
    tree_out.Branch('mass_mumu',mass_mumu, 'mass_mumu/D')
    tree_out.Branch('mass_GG', mass_GG, 'mass_GG/D')
    tree_out.Branch('mass_ee', mass_ee, 'mass_ee/D')
    tree_out.Branch('NPhotons', NPhotons, 'NPhotons/I')




    HardMetMinusMet = np.zeros(1, dtype=float)
    tree_out.Branch('HardMetMinusMet', HardMetMinusMet, 'HardMetMinusMet/D')
    IsUniqueSeed = np.zeros(1, dtype=int)
    tree_out.Branch('IsUniqueSeed', IsUniqueSeed, 'IsUniqueSeed/I')
    JetsAUX = ROOT.std.vector('TLorentzVector')()
    tree_out.Branch('JetsAUX', JetsAUX)
    hadronicJets = ROOT.std.vector('TLorentzVector')()
    tree_out.Branch('hadronicJets', hadronicJets)    
    jetsRebalanced = ROOT.std.vector('TLorentzVector')()
    tree_out.Branch('JetsRebalanced', jetsRebalanced)
    rebalancedHardMet =np.zeros(1, dtype=float)
    tree_out.Branch('rebalancedHardMet', rebalancedHardMet, 'rebalancedHardMet/D')

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
    mva_Pt_Gg = np.zeros(1, dtype=float)
    tree_out.Branch('mva_Pt_Gg', mva_Pt_Gg, 'mva_Pt_Gg/D')
    mva_ST_jets = np.zeros(1, dtype=float)
    tree_out.Branch('mva_ST_jets', mva_ST_jets, 'mva_ST_jets/D')    
    mva_min_dPhi = np.zeros(1, dtype=float)
    tree_out.Branch('mva_min_dPhi', mva_min_dPhi, 'mva_min_dPhi/D')    
    mva_dPhi1 = np.zeros(1, dtype=float)
    tree_out.Branch('mva_dPhi1', mva_dPhi1, 'mva_dPhi1/D')
    mva_dPhi2 = np.zeros(1, dtype=float)
    tree_out.Branch('mva_dPhi2', mva_dPhi2, 'mva_dPhi2/D')
    mva_dPhi_GGHardMET = np.zeros(1, dtype=float)
    tree_out.Branch('mva_dPhi_GGHardMET', mva_dPhi_GGHardMET, 'mva_dPhi_GGHardMET/D') 
    mva_dRjet1photon1 = np.zeros(1, dtype=float)
    tree_out.Branch('mva_dRjet1photon1', mva_dRjet1photon1, 'mva_dRjet1photon1/D')
    mva_dRjet1photon2 = np.zeros(1, dtype=float)
    tree_out.Branch('mva_dRjet1photon2', mva_dRjet1photon2, 'mva_dRjet1photon2/D')
    mva_dRjet2photon1 = np.zeros(1, dtype=float)
    tree_out.Branch('mva_dRjet2photon1', mva_dRjet2photon1, 'mva_dRjet2photon1/D')        
    mva_dRjet2photon2 = np.zeros(1, dtype=float)
    tree_out.Branch('mva_dRjet2photon2', mva_dRjet2photon2, 'mva_dRjet2photon2/D')    


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
recojets_ = vector('UsefulJet')()
recojets = vector('UsefulJet')()
recoelectrons = vector('TLorentzVector')()
recomuons = vector('TLorentzVector')()
genjets_ = vector('TLorentzVector')()
ipvelectrons = vector('TLorentzVector')()

ntot = 0
ndipho = 0

t0 = thyme.time()

ntot = 0
n2pho = 0


for ientry in range((extended-1)*n2process, extended*n2process):

    if ientry%printevery==0:
        print "processing event", ientry, '/', extended*n2process, 'time', thyme.time()-t0

    if debugmode:
        #if not ientry>102000 and ientry < 112850: continue
        if not ientry in [102850]: continue


    if ientry>nentries: break
    c.GetEntry(ientry)
    if issignal:

        '''
        nsignalpho = 0
        for igen, gp in enumerate(c.GenParticles):
            if not abs(c.GenParticles_PdgId[igen])==22: continue            
            if not c.GenParticles_Status[igen]==1: continue
            if not abs(c.GenParticles_ParentId[igen])>1000000: continue
            nsignalpho+=1

        print ientry, 'nsignalpho', nsignalpho
        if nsignalpho==2: n2pho+=1
        ntot+=1
        #print 'br22pho =', 1.0*n2pho/ntot
        #pause()
        '''

        par1_, par2_ = c.SignalParameters
        if not (par1_==par1 and par2_==par2):
            print 'starting new file'

            par1, par2 = par1_, par2_
            print 'cross section', par1, par2, c.CrossSection
            fnew.cd()
            fnew.cd('../')
            hHt.Write()
            hHtWeighted.Write()
            hfilterfails.Write()
            tcounter.Write()
            hPassFit.Write()
            hTotFit.Write()
            if mktree:
                fnew.cd()
                fnew.cd('TreeMaker2')
                tree_out.Write()
            print 'just created', fnew.GetName()
            for obj in [hHt, hHtWeighted, hfilterfails, tcounter, tree_out, hPassFit, hTotFit]: obj.SetDirectory(0)
            fnew.Close()
            for obj in [hHt, hHtWeighted, hfilterfails, tcounter, tree_out, hPassFit, hTotFit]: obj.Reset()
            newname = newname.split('_')[0]+'_m'+str(par1)+'d'+str(par2)+'_time'+str(round(thyme.time()%100000,2))+'.root'
            fnew = TFile(newname, 'recreate')
            fnew.mkdir('TreeMaker2')
            fnew.cd('TreeMaker2')
            print 'creating', newname

    tcounter.Fill()
    IsUniqueSeed[0] = 1

    if isdata:  
        weight = 1.0
    else:  
        weight = c.CrossSection
        isValidHtRange = False
        for madrange in madranges:
            if (c.madHT>=madrange[0] and c.madHT<madrange[1]):
                isValidHtRange = True
                break 
        if not isValidHtRange: continue#####this should be changed/fixed in Prompt code	

    if isfast: 
        if not passesUniversalSelectionFast(c): continue
    else:

        if passesUniversalSelection(c)<0: 
            if len(c.Photons)>1: 
                hfilterfails.Fill(passesUniversalSelection(c))
                continue
            elif len(c.Photons)>1: hfilterfails.Fill(0)    
    #if not passesHadronicSusySelection(c): continue


    npsv = 0
    mass_ee[0] = -1.0
    mass_mumu[0] = -1.0
    if muversion: 
        if not len(c.Muons)>1: continue
    else:
        if not len(c.Photons)>1: continue

    if poofmu:
        if not len(c.Muons)>1: continue
        if not len(c.Photons)>1: continue

        
    if poofe:
#        if not len(c.Electrons)>1: continue
        if not len(c.Photons)>3: continue


    ipvelectrons.clear()
    acme_objects.clear()
    analysisPhotons.clear()
    analysisPhotons_passWp.clear()
    analysisPhotons_passWpNminus3.clear()
    analysisPhotons_passWpInvertPsv.clear()        
    analysisPhotons_passWpInvertSieie.clear()
    analysisPhotons_passWpInvertHoe.clear()
    analysisPhotons_passWpInvertSieieAndHoe.clear()    
    analysisPhotons_hoe.clear()
    analysisPhotons_sieie.clear()
    analysisPhotons_hasPixelSeed.clear()
    analysisPhotons_isGenPho.clear()
    analysisPhotons_isGenEle.clear()
    analysisPhotons_isGenMu.clear()
    analysisPhotons_isGenTau.clear()    
    analysisPhotons_isGenNone.clear()  
    
    analysisPhotons_minDrGenEle.clear()
    analysisPhotons_minDrRecEle.clear()    
    #build up the vector of jets using TLorentzVectors; 
    #this is where you have to interface with the input format you're using
    if not (len(c.Photons)>0 or len(c.Electrons)>0 or len(c.Muons)>0): continue
    #idea: use HT to reference prior instead of ST

    npasspixelseed = 0
    for ipho, pho in enumerate(c.Photons):

        if not pho.Pt()>20: continue #trigger is pho 70

        if not abs(pho.Eta())<2.4: continue        

        if not bool(c.Photons_fullID[ipho]): continue #####this was off for VN-1

        tlvpho = TLorentzVector()
        tlvpho.SetPtEtaPhiE(pho.Pt(), pho.Eta(), pho.Phi(), pho.E())
        usefulpho = UsefulJet(tlvpho, 0, 0, -1)
        acme_objects.push_back(usefulpho)
        #if not c.Photons_passElectronVeto[ipho]: continue

        if (poofmu or poofe) and (not pho.Pt()>30): continue
        elif not pho.Pt()>75: continue
        
        
        if photonWp=='Loose':
            if abs(pho.Eta())<1.48:
                if not (c.Photons_pfChargedIsoRhoCorr[ipho]<1.694 and c.Photons_pfNeutralIsoRhoCorr[ipho]<(24.032 +0.01512*pho.Pt()+0.00002259*pow(pho.Pt(),2)) and c.Photons_pfGammaIsoRhoCorr[ipho]<(2.876 + 0.004017*pho.Pt())):
                    continue     
            if abs(pho.Eta())>=1.48:
                if not (c.Photons_pfChargedIsoRhoCorr[ipho]<2.089 and c.Photons_pfNeutralIsoRhoCorr[ipho]<(19.722 +0.0117*pho.Pt()+0.000023*pow(pho.Pt(),2)) and c.Photons_pfGammaIsoRhoCorr[ipho]<(4.162 + 0.0037*pho.Pt())):
                    continue      
        elif photonWp=='Medium':
            if abs(pho.Eta())<1.48:
                if not (c.Photons_pfChargedIsoRhoCorr[ipho]<0.441 and c.Photons_pfNeutralIsoRhoCorr[ipho]<(2.725 +0.0148*pho.Pt()+0.000017*pow(pho.Pt(),2)) and c.Photons_pfGammaIsoRhoCorr[ipho]<(2.571 + 0.0047*pho.Pt())):
                    continue       
            if abs(pho.Eta())>=1.48:
                if not (c.Photons_pfChargedIsoRhoCorr[ipho]<0.442 and c.Photons_pfNeutralIsoRhoCorr[ipho]<(1.715 +0.0163*pho.Pt()+0.000014*pow(pho.Pt(),2)) and c.Photons_pfGammaIsoRhoCorr[ipho]<(3.863 + 0.0034*pho.Pt())):
                    continue                                                  

        analysisPhotons.push_back(tlvpho)
        analysisPhotons_passWpNminus3.push_back(True)
        analysisPhotons_passWp.push_back(False)
        analysisPhotons_passWpInvertPsv.push_back(False)
        analysisPhotons_passWpInvertSieie.push_back(False)
        analysisPhotons_passWpInvertHoe.push_back(False)
        analysisPhotons_passWpInvertSieieAndHoe.push_back(False)
        analysisPhotons_hoe.push_back(-1)
        analysisPhotons_sieie.push_back(-1)
        analysisPhotons_hasPixelSeed.push_back(-1)
        idx = analysisPhotons_passWp.size()-1
        analysisPhotons_isGenPho.push_back(False)
        analysisPhotons_isGenEle.push_back(False)
        analysisPhotons_isGenMu.push_back(False)
        analysisPhotons_isGenTau.push_back(False)        
        analysisPhotons_isGenNone.push_back(False)
        analysisPhotons_minDrGenEle.push_back(99)
        analysisPhotons_minDrRecEle.push_back(99)        
              
        if photonWp=='Loose':
            if abs(pho.Eta())<1.48:
                if c.Photons_hadTowOverEM[ipho]<0.04596 and c.Photons_sigmaIetaIeta[ipho]<0.01031 and (not bool(c.Photons_hasPixelSeed[ipho])):analysisPhotons_passWp[idx] = True
                if c.Photons_hadTowOverEM[ipho]<0.04596 and c.Photons_sigmaIetaIeta[ipho]<0.01031 and bool(c.Photons_hasPixelSeed[ipho]):analysisPhotons_passWpInvertPsv[idx] = True
                if c.Photons_hadTowOverEM[ipho]<0.04596 and c.Photons_sigmaIetaIeta[ipho]>=0.01031 and bool(c.Photons_hasPixelSeed[ipho]):analysisPhotons_passWpInvertSieie[idx] = True
                if c.Photons_hadTowOverEM[ipho]>=0.04596 and c.Photons_sigmaIetaIeta[ipho]<0.01031 and bool(c.Photons_hasPixelSeed[ipho]):analysisPhotons_passWpInvertHoe[idx] = True
                if c.Photons_hadTowOverEM[ipho]>=0.04596 and c.Photons_sigmaIetaIeta[ipho]>=0.01031 and bool(c.Photons_hasPixelSeed[ipho]):analysisPhotons_passWpInvertSieieAndHoe[idx] = True
            if abs(pho.Eta())>=1.48:
                if c.Photons_hadTowOverEM[ipho]<0.0590 and c.Photons_sigmaIetaIeta[ipho]<0.03001 and (not bool(c.Photons_hasPixelSeed[ipho])):analysisPhotons_passWp[idx] = True
                if c.Photons_hadTowOverEM[ipho]<0.0590 and c.Photons_sigmaIetaIeta[ipho]<0.03001 and bool(c.Photons_hasPixelSeed[ipho]):analysisPhotons_passWpInvertPsv[idx] = True
                if c.Photons_hadTowOverEM[ipho]<0.0590 and c.Photons_sigmaIetaIeta[ipho]>=0.03001 and bool(c.Photons_hasPixelSeed[ipho]):analysisPhotons_passWpInvertSieie[idx] = True
                if c.Photons_hadTowOverEM[ipho]>=0.0590 and c.Photons_sigmaIetaIeta[ipho]<0.03001 and bool(c.Photons_hasPixelSeed[ipho]):analysisPhotons_passWpInvertHoe[idx] = True
                if c.Photons_hadTowOverEM[ipho]>=0.0590 and c.Photons_sigmaIetaIeta[ipho]>=0.03001 and bool(c.Photons_hasPixelSeed[ipho]):analysisPhotons_passWpInvertSieieAndHoe[idx] = True        
        elif photonWp=='Medium':
            if abs(pho.Eta())<1.48:
                if c.Photons_hadTowOverEM[ipho]<0.0396 and c.Photons_sigmaIetaIeta[ipho]<0.01022 and (not bool(c.Photons_hasPixelSeed[ipho])): analysisPhotons_passWp[idx] = True
                if c.Photons_hadTowOverEM[ipho]<0.0396 and c.Photons_sigmaIetaIeta[ipho]<0.01022 and bool(c.Photons_hasPixelSeed[ipho]): analysisPhotons_passWpInvertPsv[idx] = True
                if c.Photons_hadTowOverEM[ipho]<0.0396 and c.Photons_sigmaIetaIeta[ipho]>=0.01022 and bool(c.Photons_hasPixelSeed[ipho]): analysisPhotons_passWpInvertSieie[idx] = True
                if c.Photons_hadTowOverEM[ipho]>=0.0396 and c.Photons_sigmaIetaIeta[ipho]<0.01022 and bool(c.Photons_hasPixelSeed[ipho]): analysisPhotons_passWpInvertSieie[idx] = True
                if c.Photons_hadTowOverEM[ipho]>=0.0396 and c.Photons_sigmaIetaIeta[ipho]>=0.01022 and bool(c.Photons_hasPixelSeed[ipho]): analysisPhotons_passWpInvertSieieAndHoe[idx] = True
            if abs(pho.Eta())>=1.48:
                if c.Photons_hadTowOverEM[ipho]<0.0219 and c.Photons_sigmaIetaIeta[ipho]<0.03001 and (not bool(c.Photons_hasPixelSeed[ipho])): analysisPhotons_passWp[idx] = True
                if c.Photons_hadTowOverEM[ipho]<0.0219 and c.Photons_sigmaIetaIeta[ipho]<0.03001 and bool(c.Photons_hasPixelSeed[ipho]): analysisPhotons_passWpInvertPsv[idx] = True
                if c.Photons_hadTowOverEM[ipho]<0.0219 and c.Photons_sigmaIetaIeta[ipho]>=0.03001 and bool(c.Photons_hasPixelSeed[ipho]): analysisPhotons_passWpInvertSieie[idx] = True
                if c.Photons_hadTowOverEM[ipho]>=0.0219 and c.Photons_sigmaIetaIeta[ipho]<0.03001 and bool(c.Photons_hasPixelSeed[ipho]): analysisPhotons_passWpInvertSieie[idx] = True
                if c.Photons_hadTowOverEM[ipho]>=0.0219 and c.Photons_sigmaIetaIeta[ipho]>=0.03001 and bool(c.Photons_hasPixelSeed[ipho]): analysisPhotons_passWpInvertSieieAndHoe[idx] = True
                
        analysisPhotons_hoe[idx] = c.Photons_hadTowOverEM[ipho]
        analysisPhotons_sieie[idx] = c.Photons_sigmaIetaIeta[ipho]
        analysisPhotons_hasPixelSeed[idx] = bool(c.Photons_hasPixelSeed[ipho])
        
        if analysisPhotons_passWpInvertPsv[idx]:
            ipvelectrons.push_back(tlvpho)

        #if not c.Photons_genMatched[ipho]: continue
        #if bool(c.Photons_nonPrompt[ipho]): continue
        ########if bool(c.Photons_hasPixelSeed[ipho]): continue 
                 
        if sayalot:
            print ientry, 'acme photon', pho.Pt(), pho.Eta(), pho.Phi()
            print 'Photons_genMatched', c.Photons_genMatched[ipho]
            print 'Photons_nonPrompt', bool(c.Photons_nonPrompt[ipho])
            print 'Photons_pfGammaIsoRhoCorr', c.Photons_pfGammaIsoRhoCorr[ipho]
            
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
        if not mu.Pt()>30: continue  #Changed from 75 to 30 to check muon poofing (5/3/2021)
        recomuons.push_back(tlvmu)		
    #if not len(recomuons)==0: continue  

    #if we're in muon mode, overrwrite the photons with muons:
    if muversion: analysisPhotons = recomuons
    
    NPhotons[0] = len(analysisPhotons)
    
    if not int(analysisPhotons.size())>1: continue
        
    if False: 
     for ipho in range(len(analysisPhotons)):
        print ientry, ipho, 'analysisPhotons', analysisPhotons[ipho]
        print ientry, ipho, 'analysisPhotons_passWp', analysisPhotons_passWp[ipho]
        print ientry, ipho, 'analysisPhotons_passWpNminus3', analysisPhotons_passWpNminus3[ipho]
        print ientry, ipho, 'analysisPhotons_passWpInvertPsv', analysisPhotons_passWpInvertPsv[ipho]        
        print ientry, ipho, 'analysisPhotons_passWpInvertSieie', analysisPhotons_passWpInvertSieie[ipho]
        print ientry, ipho, 'analysisPhotons_passWpInvertHoe', analysisPhotons_passWpInvertHoe[ipho]
        print ientry, ipho, 'analysisPhotons_passWpInvertSieieAndHoe', analysisPhotons_passWpInvertSieieAndHoe[ipho]    
        print ientry, ipho, 'analysisPhotons_hoe', analysisPhotons_hoe[ipho]
        print ientry, ipho, 'analysisPhotons_sieie', analysisPhotons_sieie[ipho]
        print ientry, ipho, 'analysisPhotons_hasPixelSeed', analysisPhotons_hasPixelSeed[ipho]
        print ientry, ipho, 'analysisPhotons_isGenPho', analysisPhotons_isGenPho[ipho]
        print ientry, ipho, 'analysisPhotons_isGenEle', analysisPhotons_isGenEle[ipho]
        print ientry, ipho, 'analysisPhotons_isGenMu', analysisPhotons_isGenMu[ipho]
        print ientry, ipho, 'analysisPhotons_isGenTau', analysisPhotons_isGenTau[ipho]        
        print ientry, ipho, 'analysisPhotons_isGenNone', analysisPhotons_isGenNone[ipho] 
        
        
    dphiGG = abs(analysisPhotons[0].DeltaPhi(analysisPhotons[1]))
    drGG = abs(analysisPhotons[0].DeltaR(analysisPhotons[1]))

    recoelectrons.clear()
    for iel, el in enumerate(c.Electrons):
        if not el.Pt()>10: continue
        if not c.Electrons_mediumID[iel]: continue
        if not c.Electrons_passIso[iel]: continue        
        tlvel = TLorentzVector()
        tlvel.SetPtEtaPhiE(el.Pt(), el.Eta(), el.Phi(), el.Pt()*TMath.CosH(el.Eta()))
        if debugmode:
            print ientry, 'acme electron', el.Pt()		
        usefulele = UsefulJet(tlvel, 0, 0, -1)
        #acme_objects.push_back(usefulele)		# this should have been counted as an electron
        if not abs(el.Eta())<2.4: continue		
        recoelectrons.push_back(tlvel)
    #if not len(recoelectrons)==0: continue      		

    if not isdata:
        genphos, genels, genmus, gentaus, fakes = [],[],[],[], []
        for igen, gp in enumerate(c.GenParticles):
            if not gp.Pt()>10: continue
            if not c.GenParticles_Status[igen]==1: continue
            pid = abs(c.GenParticles_PdgId[igen])
            if not pid in [11,13,15,22]: continue
            gpvec = TLorentzVector(gp.px(),gp.py(),gp.pz(),gp.e())
            if pid==22: genphos.append(gpvec)
            if pid==11: genels.append(gpvec)
            if pid==13: genmus.append(gpvec)
            if pid==15: gentaus.append(gpvec)
        for ipho, pho in enumerate(analysisPhotons):
            drmin = 99                  
            for gp in genphos:
                drmin = min(drmin,gp.DeltaR(pho))
                analysisPhotons_minDrGenEle[ipho] = drmin
                if drmin<0.1: analysisPhotons_isGenPho[ipho] = True
            drmin = 99  
            for gp in genels: 
                drmin = min(drmin,gp.DeltaR(pho))
                if drmin<0.1: analysisPhotons_isGenEle[ipho] = True
            drmin = 99                  
            for gp in genmus: 
                drmin = min(drmin,gp.DeltaR(pho))
                if drmin<0.1: analysisPhotons_isGenMu[ipho] = True
            drmin = 99                  
            for gp in gentaus: 
                drmin = min(drmin,gp.DeltaR(pho))
                if drmin<0.1: analysisPhotons_isGenTau[ipho] = True                
            if not (analysisPhotons_isGenPho[ipho] or analysisPhotons_isGenEle[ipho] or analysisPhotons_isGenMu[ipho] or analysisPhotons_isGenTau[ipho]):
                analysisPhotons_isGenNone[ipho] = True
            drmin = 99                  
            for rel in recoelectrons:
                drmin = min(drmin,rel.DeltaR(pho))
                analysisPhotons_minDrRecEle[ipho] = drmin                
                
    AcmeVector_ = TLorentzVector()
    AcmeVector_.SetPxPyPzE(0,0,0,0)
    for obj in acme_objects: AcmeVector_+=obj.tlv		

    _Templates_.AcmeVector = AcmeVector_	

    recojets_.clear()
    for ijet, jet in enumerate(c.Jets):
        if not (jet.Pt()>2 and abs(jet.Eta())<5.0): continue
        jettlv = TLorentzVector(jet.Px(),jet.Py(),jet.Pz(), jet.E())
        recojets_.push_back(UsefulJet(jettlv, c.Jets_bJetTagDeepCSVBvsAll[ijet], float(int(bool(c.Jets_ID[ijet]))), ijet))



    if is2017: # ecal noise treatment
        recojets_.clear()
        for ijet, jet in enumerate(c.Jets):
            if not (jet.Pt()>2 and abs(jet.Eta())<5.0): continue
            if abs(jet.Eta())>2.65 and abs(jet.Eta()) < 3.139 and jet.Pt()/c.Jets_jecFactor[ijet]<50: continue #/c.Jets_jerFactor[ijet]
            jettlv = TLorentzVector(jet.Px(),jet.Py(),jet.Pz(), jet.E())
            recojets_.push_back(UsefulJet(jettlv, c.Jets_bJetTagDeepCSVBvsAll[ijet], float(int(bool(c.Jets_ID[ijet]))), ijet))



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
            if jet.DeltaR(closestAcme)<0.4:
                nMatchedAcmeInnerPairs+=1
                if sayalot: print 'skipping reco jet with pT, eta', jet.Pt(), jet.Eta(), jet.DeltaR(acme_objects[0].tlv)
                continue
        if jet.Pt()>AnHardMetJetPtCut and jet.JetId()<0.5: 
            passesJetId = False
            break
        ujet = UsefulJet(jet.tlv, jet.btagscore, jet.jetId, jet.originalIdx)
        recojets.push_back(ujet)

    if not passesJetId: 
        ###print ientry, 'failed jet ID'
        continue


    shouldskipevent = False
    if not nMatchedAcmeOuterPairs==nMatchedAcmeInnerPairs: 
        ##print 'contingency a'
        shouldskipevent = True    
    if not nMatchedAcmeInnerPairs==len(acme_objects): 
        ##print 'contingency b', nMatchedAcmeInnerPairs, len(acme_objects)     
        shouldskipevent = True
    if shouldskipevent: 
        ##print ientry, 'acme mismatch'
        continue


    if not isdata:
        genjets_.clear()
        for ijet, jet in enumerate(c.GenJets):
            #if not jet.Pt()>15: continue
            #if not abs(jet.Eta())<5: continue
            jettlv = TLorentzVector(jet.Px(),jet.Py(),jet.Pz(), jet.E())
            ujet = UsefulJet(jettlv, 0, 0, -1)
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

    ##observed histogram
    tHt = getHt(recojets,AnHardMetJetPtCut)
    tSt = tHt
    for obj in acme_objects: tSt+=obj.Pt()
    tHardMhtVec = getHardMet(recojets,AnHardMetJetPtCut, mhtjetetacut)
    tHardMetVec = tHardMhtVec.Clone()
    tHardMetVec-=AcmeVector_ # this still needed because the reco-jets don't contain the acme_objects


    tHardMetPt, tHardMetPhi = tHardMetVec.Pt(), tHardMetVec.Phi()
    HardMETPt[0], HardMETPhi[0] = tHardMetPt, tHardMetPhi

    sumjetpt = TLorentzVector()
    for irjet, rjet in enumerate(recojets):
        if not rjet.Pt()>30: continue
        sumjetpt-=rjet.tlv


    if tHardMetPt> met4skim:
        print str(c.RunNum)+':'+str(c.LumiBlockNum)+':'+str(c.EvtNum)
        #continue




    tjets_pt = tHardMhtVec.Clone()
    tjets_pt*=-1

    if poofmu:
        if len(recomuons)>1:
            mass_mumu[0] = (recomuons[0]+recomuons[1]).M()
            tHardMetVec+=recomuons[0]
            tHardMetVec+=recomuons[1]
            MetVec+=recomuons[0]
            MetVec+=recomuons[1]

    
    if poofe:
        if len(ipvelectrons)>1:
            mass_ee[0] = (ipvelectrons[0]+ipvelectrons[1]).M()
            tHardMetVec+=ipvelectrons[0]
            tHardMetVec+=ipvelectrons[1]
            MetVec+=ipvelectrons[0]
            MetVec+=ipvelectrons[1]
    

    mass_GG[0] = (analysisPhotons[0]+analysisPhotons[1]).M()   

    #if  not abs(MetVec.Pt()-tHardMetVec.Pt())<60: continue
    HardMetMinusMet[0] = MetVec.Pt()-tHardMetVec.Pt()

    if tHt>0: tMetSignificance = tHardMetPt/TMath.Sqrt(tHt)
    else: tMetSignificance = 99
    tNJets = countJets(recojets,AnHardMetJetPtCut)##these moved below to pick up the acmes again
    tBTags = countBJets(recojets,AnHardMetJetPtCut)


    #tNJets = countJets(recojets,AnHardMetJetPtCut)##these moved to the earliest moment possible
    #tBTags = countBJets(recojets,AnHardMetJetPtCut)##these moved to the earliest moment possible
    tmindphi = 4##these moved to the earliest moment possible
    for jet in recojets[:4]: 
        if jet.Pt()>30:
            tmindphi = min(tmindphi, abs(jet.tlv.DeltaPhi(tHardMetVec)))    ##these moved to the earliest moment possible

    if len(recojets)>1:
        tdphi1 = abs(recojets[0].tlv.DeltaPhi(tHardMetVec))
        tdphi2 = abs(recojets[1].tlv.DeltaPhi(tHardMetVec))
        drjet1pho1 = abs(recojets[0].tlv.DeltaR(analysisPhotons[0]))
        drjet1pho2 = abs(recojets[0].tlv.DeltaR(analysisPhotons[1]))
        drjet2pho1 = abs(recojets[1].tlv.DeltaR(analysisPhotons[0]))
        drjet2pho2 = abs(recojets[1].tlv.DeltaR(analysisPhotons[1]))

    elif len(recojets)>0:
        tdphi1 = abs(recojets[0].tlv.DeltaPhi(tHardMetVec))
        tdphi2 = 4.0
        drjet1pho1 = abs(recojets[0].tlv.DeltaR(analysisPhotons[0]))
        drjet1pho2 = abs(recojets[0].tlv.DeltaR(analysisPhotons[1]))
        drjet2pho1 = -1.0
        drjet2pho2 = -1.0

    else:
        tdphi1 = 4.0
        tdphi2 = 4.0
        drjet1pho1 = -1.0
        drjet1pho2 = -1.0
        drjet2pho1 = -1.0
        drjet2pho2 = -1.0

    hadronicJets.clear()
    for jet in recojets:
        hadronicJets.push_back(jet.tlv)
        
        
    nsmears = smears*bootupfactor

    pt1 = analysisPhotons[0].Pt()
    pt2 = analysisPhotons[1].Pt()
    if pt1 > 500:
        pt1 = 499
    if pt1 > 500:
        pt2 = 499
    Pho1_SF[0] = photonSF_hist.GetBinContent(photonSF_hist.FindFixBin(analysisPhotons[0].Eta(), pt1))
    Pho2_SF[0] = photonSF_hist.GetBinContent(photonSF_hist.FindFixBin(analysisPhotons[1].Eta(), pt2))
    Pho1_SFE[0] = photonSF_hist.GetBinError(photonSF_hist.FindFixBin(analysisPhotons[0].Eta(), pt1))
    Pho2_SFE[0] = photonSF_hist.GetBinError(photonSF_hist.FindFixBin(analysisPhotons[1].Eta(), pt2))

    #print ientry, 'tHardMetPt', tHardMetPt, len(recojets), 'len(acme_objects)', len(acme_objects), _Templates_.AcmeVector.Pt()
        
    if mktree and tHardMetPt>met4skim:

            IsRandS[0] = 0 
            JetsAUX.clear()
            JetsAUX_bJetTagDeepCSVBvsAll.clear()
            for ijet, jet in enumerate(c.Jets):
                jettlv = TLorentzVector(jet.Px(),jet.Py(),jet.Pz(), jet.E())
                JetsAUX.push_back(jettlv)
                JetsAUX_bJetTagDeepCSVBvsAll.push_back(c.Jets_bJetTagDeepCSVBvsAll[ijet])

            HTAUX[0] = c.HT
            NJetsAUX[0] = c.NJets
            BTagsAUX[0] = c.BTags

            HardMETPt[0] = tHardMetPt
            HardMETPhi[0] = tHardMetPhi
            MinDPhiHardMetJets[0] = tmindphi
            NSmearsPerEvent[0] = nsmears
            mva_Ngoodjets[0] = tNJets
            mva_ST[0] = tSt##
            mva_Pt_jets[0] = tjets_pt.Pt()#
            mva_dPhi_GG[0] = dphiGG#
            mva_Photons0Et[0] = analysisPhotons[0].Pt()#
            mva_Photons1Et[0] = analysisPhotons[1].Pt()#
            mva_HardMET[0] = tHardMetVec.Pt()
            mva_Pt_Gg[0] = (analysisPhotons[0]+analysisPhotons[1]).Pt()#
            mva_ST_jets[0] = tHt#
            mva_min_dPhi[0] = tmindphi#
            mva_dPhi_GGHardMET[0] = abs(tHardMetVec.DeltaPhi(analysisPhotons[0]+analysisPhotons[1]))#
            mva_dPhi1[0] = tdphi1
            mva_dPhi2[0] = tdphi2
            mva_dRjet1photon1[0] = drjet1pho1
            mva_dRjet1photon2[0] = drjet1pho2
            mva_dRjet2photon1[0] = drjet2pho1
            mva_dRjet2photon2[0] = drjet2pho2

            _Ngoodjets_[0] = int(mva_Ngoodjets[0])
            _ST_[0] = mva_ST[0]
            _Pt_jets_[0] = mva_Pt_jets[0]/_ST_[0]
            _dPhi_GG_[0] = mva_dPhi_GG[0]
            _Photons0Et_[0] = mva_Photons0Et[0]/_ST_[0]
            _Photons1Et_[0] = mva_Photons1Et[0]/_ST_[0]
            _HardMET_[0] = mva_HardMET[0]/_ST_[0]
            _Pt_GG_[0] = mva_Pt_Gg[0]/_ST_[0]
            _ST_jets_[0] = mva_ST_jets[0]/_ST_[0]
            _min_dPhi_[0] = mva_min_dPhi[0]
            _dPhi_GGHardMET_[0] = mva_dPhi_GGHardMET[0]
            _dPhi1_[0] = mva_dPhi1[0]
            _dPhi2_[0] = mva_dPhi2[0]
            _dRjet1photon1_[0] = mva_dRjet1photon1[0]
            _dRjet1photon2_[0] = mva_dRjet1photon2[0]
            _dRjet2photon1_[0] = mva_dRjet2photon1[0]
            _dRjet1photon2_[0] = mva_dRjet2photon2[0]

            mva_BDT[0] = reader.EvaluateMVA("BDT")
            tree_out.Fill()
            IsUniqueSeed[0] = 0            


    if nsmears==0: continue
            
    fitsucceed = RebalanceJets(recojets)
    rebalancedJets = _Templates_.dynamicJets



    for obj in acme_objects: ##this has got to come after the rebalancing
        recojets.push_back(obj)
    sortThatThang(recojets)
    NOrigJets15[0] = len(recojets)


    mHardMetVec = getHardMet(rebalancedJets,AnHardMetJetPtCut, mhtjetetacut)
    
    #print ientry, 'mHardMetVec.Pt()', mHardMetVec.Pt()
    #if len(rebalancedJets)>0: print 'here ya go', rebalancedJets[0].Pt(), recojets[0].Pt(), 'acme vector pt', AcmeVector_.Pt()

    mHardMetVec-=AcmeVector_ # this is now done because the acme_objects were not stuck back into the reblanced jets
    mHardMetPt, mHardMetPhi = mHardMetVec.Pt(), mHardMetVec.Phi()

    rebalancedHardMet[0] = mHardMetPt

    mBTags = countBJets(rebalancedJets,AnHardMetJetPtCut)###

    fitsucceed = (fitsucceed and mHardMetPt<rebalancedMetCut)# mHardMetPt>min(mHt/2,180):# was 160	

    #redoneMET = redoMET(MetVec,recojets,rebalancedJets)
    #mMetPt,mMetPhi = redoneMET.Pt(), redoneMET.Phi()


    fillth1(hTotFit, mBTags, weight)

    if fitsucceed: fillth1(hPassFit, mBTags, weight)

    for ijet, jet in enumerate(rebalancedJets):
        jetsRebalanced.push_back(jet.tlv)
        
        
        
    
    for i in range(nsmears):

        if (not fitsucceed): break

        RplusSJets = smearJets(rebalancedJets,99+_Templates_.nparams)
        rpsHt = getHt(RplusSJets,AnHardMetJetPtCut)
        rpsSt = rpsHt
        for obj in acme_objects: rpsSt+=obj.Pt()

        rps_jets_pt = getHardMet(RplusSJets,AnHardMetJetPtCut, mhtjetetacut)
        rps_jets_pt*=-1


        rpsHardMetVec = getHardMet(RplusSJets,AnHardMetJetPtCut, mhtjetetacut)
        rpsHardMetVec-=AcmeVector_ # this is now done because the acme_objects are not stuck back into the R&S jets yet
        rpsHardMetPt, rpsHardMetPhi = rpsHardMetVec.Pt(), rpsHardMetVec.Phi()


        rpsNJets = countJets(RplusSJets,AnHardMetJetPtCut)
        rpsBTags = countBJets(RplusSJets,AnHardMetJetPtCut)
        rpsmindphi = 4
        for jet in RplusSJets[:4]: 
            if jet.Pt()>30:
                rpsmindphi = min(rpsmindphi, abs(jet.tlv.DeltaPhi(rpsHardMetVec)))

        if len(RplusSJets)>1:
            rpsdphi1 = abs(RplusSJets[0].tlv.DeltaPhi(tHardMetVec))
            rpsdphi2 = abs(RplusSJets[1].tlv.DeltaPhi(tHardMetVec))
            rpsdrjet1pho1 = abs(RplusSJets[0].tlv.DeltaR(analysisPhotons[0]))
            rpsdrjet1pho2 = abs(RplusSJets[0].tlv.DeltaR(analysisPhotons[1]))
            rpsdrjet2pho1 = abs(RplusSJets[1].tlv.DeltaR(analysisPhotons[0]))
            rpsdrjet2pho2 = abs(RplusSJets[1].tlv.DeltaR(analysisPhotons[1]))

        elif len(RplusSJets)>0:
            rpsdphi1 = abs(RplusSJets[0].tlv.DeltaPhi(tHardMetVec))
            rpsdphi2 = 4.0
            rpsdrjet1pho1 = abs(RplusSJets[0].tlv.DeltaR(analysisPhotons[0]))
            rpsdrjet1pho2 = abs(RplusSJets[0].tlv.DeltaR(analysisPhotons[1]))
            rpsdrjet2pho1 = -1.0
            rpsdrjet2pho2 = -1.0

        else:
            rpsdphi1 = 4.0
            rpsdphi2 = 4.0
            rpsdrjet1pho1 = -1.0
            rpsdrjet1pho2 = -1.0
            rpsdrjet2pho1 = -1.0
            rpsdrjet2pho2 = -1.0




        hadronicJets.clear()
        for jet in RplusSJets:
            hadronicJets.push_back(jet.tlv)
        for acme in acme_objects: RplusSJets.push_back(acme)#This will save the R&S jets even for nonR&S events if hardMET<cut

        sortThatThang(RplusSJets)
        #if len(RplusSJets)>3:
            #print ientry, RplusSJets[0].Pt(),RplusSJets[1].Pt(),RplusSJets[2].Pt(),RplusSJets[3].Pt()
            #print 'nparams was', _Templates_.nparams
            
            
        
        if mktree:
            if rpsHardMetPt>met4skim:

                if IsUniqueSeed[0]==1: ##write the true event if teh R&S hard MET was large enough

                    JetsAUX.clear()
                    JetsAUX_bJetTagDeepCSVBvsAll.clear()
                    for ijet, jet in enumerate(c.Jets):
                        jettlv = TLorentzVector(jet.Px(),jet.Py(),jet.Pz(), jet.E())
                        JetsAUX.push_back(jettlv)
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
                    mva_Ngoodjets[0] = tNJets
                    mva_ST[0] = tSt##
                    mva_Pt_jets[0] = tjets_pt.Pt()#
                    mva_dPhi_GG[0] = dphiGG
                    mva_Photons0Et[0] = analysisPhotons[0].Pt()#
                    mva_Photons1Et[0] = analysisPhotons[1].Pt()#
                    mva_HardMET[0] = tHardMetVec.Pt()#
                    mva_Pt_Gg[0] = (analysisPhotons[0]+analysisPhotons[1]).Pt()#
                    mva_ST_jets[0] = tHt#
                    mva_min_dPhi[0] = tmindphi#
                    mva_dPhi_GGHardMET[0] = abs(tHardMetVec.DeltaPhi(analysisPhotons[0]+analysisPhotons[1]))#
                    mva_dPhi1[0] = tdphi1
                    mva_dPhi2[0] = tdphi2

                    mva_dRjet1photon1[0] = drjet1pho1
                    mva_dRjet1photon2[0] = drjet1pho2
                    mva_dRjet2photon1[0] = drjet2pho1
                    mva_dRjet2photon2[0] = drjet2pho2


                    _Ngoodjets_[0] = int(mva_Ngoodjets[0])
                    _ST_[0] = mva_ST[0]
                    _Pt_jets_[0] = mva_Pt_jets[0]/_ST_[0]
                    _dPhi_GG_[0] = mva_dPhi_GG[0]
                    _Photons0Et_[0] = mva_Photons0Et[0]/_ST_[0]
                    _Photons1Et_[0] = mva_Photons1Et[0]/_ST_[0]            
                    _HardMET_[0] = mva_HardMET[0]/_ST_[0]
                    _Pt_GG_[0] = mva_Pt_Gg[0]/_ST_[0]
                    _ST_jets_[0] = mva_ST_jets[0]/_ST_[0]
                    _min_dPhi_[0] = mva_min_dPhi[0]
                    _dPhi_GGHardMET_[0] = mva_dPhi_GGHardMET[0]
                    _dPhi1_[0] = mva_dPhi1[0]
                    _dPhi2_[0] = mva_dPhi2[0]
                    _dRjet1photon1_[0] = mva_dRjet1photon1[0]
                    _dRjet1photon2_[0] = mva_dRjet1photon2[0]
                    _dRjet2photon1_[0] = mva_dRjet2photon1[0]
                    _dRjet1photon2_[0] = mva_dRjet2photon2[0]

                    mva_BDT[0] = reader.EvaluateMVA("BDT")
                    tree_out.Fill()
                    print ientry, 'fillin up the tank'
                    IsUniqueSeed[0] = 0

                if True:##fill with the R&S entry

                    IsRandS[0] = 1 
                    JetsAUX.clear()
                    JetsAUX_bJetTagDeepCSVBvsAll.clear()
                    for ijet, jet in enumerate(RplusSJets):
                        JetsAUX.push_back(jet.tlv)
                        JetsAUX_bJetTagDeepCSVBvsAll.push_back(jet.btagscore) 

                    #do things like they are RandS


                    HTAUX[0] = rpsHt
                    NJetsAUX[0] = rpsNJets
                    BTagsAUX[0] = rpsBTags

                    HardMETPt[0] = rpsHardMetPt
                    HardMETPhi[0] = rpsHardMetPhi
                    MinDPhiHardMetJets[0] = rpsmindphi
                    NSmearsPerEvent[0] = nsmears
                    FitSucceed[0] = fitsucceed     
                    mva_Ngoodjets[0] = rpsNJets
                    mva_ST[0] = rpsSt
                    mva_Pt_jets[0] = rps_jets_pt.Pt()
                    mva_dPhi_GG[0] = dphiGG
                    mva_Photons0Et[0] = analysisPhotons[0].Pt()
                    mva_Photons1Et[0] = analysisPhotons[1].Pt()
                    mva_HardMET[0] = rpsHardMetPt
                    mva_Pt_Gg[0] = (analysisPhotons[0]+analysisPhotons[1]).Pt()
                    mva_ST_jets[0] = rpsHt
                    mva_min_dPhi[0] = rpsmindphi
                    mva_dPhi_GGHardMET[0] = abs(rpsHardMetVec.DeltaPhi(analysisPhotons[0]+analysisPhotons[1]))
                    mva_dPhi1[0] = rpsdphi1
                    mva_dPhi2[0] = rpsdphi2

                    mva_dRjet1photon1[0] = rpsdrjet1pho1
                    mva_dRjet1photon2[0] = rpsdrjet1pho2
                    mva_dRjet2photon1[0] = rpsdrjet2pho1
                    mva_dRjet2photon2[0] = rpsdrjet2pho2


                    _Ngoodjets_[0] = int(mva_Ngoodjets[0])
                    _ST_[0] = mva_ST[0]
                    _Pt_jets_[0] = mva_Pt_jets[0]/_ST_[0]
                    _dPhi_GG_[0] = mva_dPhi_GG[0]
                    _Photons0Et_[0] = mva_Photons0Et[0]/_ST_[0]
                    _Photons1Et_[0] = mva_Photons1Et[0]/_ST_[0]
                    _HardMET_[0] = mva_HardMET[0]/_ST_[0]
                    _Pt_GG_[0] = mva_Pt_Gg[0]/_ST_[0]
                    _ST_jets_[0] = mva_ST_jets[0]/_ST_[0]
                    _min_dPhi_[0] = mva_min_dPhi[0]
                    _dPhi_GGHardMET_[0] = mva_dPhi_GGHardMET[0]
                    _dPhi1_[0] = mva_dPhi1[0]
                    _dPhi2_[0] = mva_dPhi2[0]
                    _dRjet1photon1_[0] = mva_dRjet1photon1[0]
                    _dRjet1photon2_[0] = mva_dRjet1photon2[0]
                    _dRjet2photon1_[0] = mva_dRjet2photon1[0]
                    _dRjet1photon2_[0] = mva_dRjet2photon2[0]

                    mva_BDT[0] = reader.EvaluateMVA("BDT")
                    tree_out.Fill()

    if isdata: continue


fnew.cd()
fnew.cd('../')
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
