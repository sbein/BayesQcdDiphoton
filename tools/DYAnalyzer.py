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
met4skim = 100
mhtjetetacut = 5.0 # also needs be be changed in UsefulJet.h
AnHardMetJetPtCut = 30.0
rebalancedMetCut = 150
useMediumPho = False


sayalot = False
nametag = {'Nom':'', 'Up': 'JerUp'}


'''
python tools/DYAnalyzer.py --fnamekeyword Summer16v3.DYJetsToLL_M-50_Tune --quickrun True
python tools/submitHistJobs.py --analyzer tools/DYAnalyzer.py --fnamekeyword Summer16v3.DYJetsToLL_M-50_Tune
'''

##load in UsefulJet class, which the rebalance and smear code uses
gROOT.ProcessLine(open('src/UsefulJet.cc').read())
exec('from ROOT import *')
gROOT.ProcessLine(open('src/BayesRandS.cc').read())
exec('from ROOT import *')


##read in command line arguments
defaultInfile_ = "Summer16v3.DYJetsToLL_M-50_Tune"
#T2qqGG.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=1,help="analyzer script to batch")
parser.add_argument("-printevery", "--printevery", type=int, default=1000,help="short run")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile_,help="file")
parser.add_argument("-quickrun", "--quickrun", type=bool, default=False,help="short run")
args = parser.parse_args()
fnamekeyword = args.fnamekeyword
inputFiles = glob(fnamekeyword)
verbosity = args.verbosity
printevery = args.printevery
quickrun = args.quickrun




if 'Summer16' in fnamekeyword or 'Fall17' in fnamekeyword or 'Autumn18' in fnamekeyword:
    isdata = False
else: 
    isdata = True

is2017 = False
is2016 = False
is2018 = False

if 'Fast' in fnamekeyword: isfast = True
else: isfast = False

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

issignal = abs('Fast' in fnamekeyword)

#################
# Load in chain #
#################        root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/
''' ususally did something like this: 
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2016/*/*.root > usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2017/*/*.root >> usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2018/*/*.root >> usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2016/*/*/*.root >> usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2017/*/*/*.root >> usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2018/*/*/*2018A*.root >> usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2018/*/*/*2018B*.root >> usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2018/*/*/*2018C*.root >> usefulthings/filelistDiphotonBig.txt
ls -1 -d /eos/uscms//store/group/lpcsusyphotons/TreeMaker/2018/*/*/*2018D*.root >> usefulthings/filelistDiphotonBig.txt

'''

ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/'
fnamefilename = 'usefulthings/filelistDiphoton.txt'
fnamefilename = 'usefulthings/filelistDiphotonBig.txt'
if not 'DoubleEG' in fnamekeyword:
    if 'Summer16v3.QCD_HT' in fnamekeyword or 'WJets' in fnamekeyword: #or 'Run20' in fnamekeyword
        fnamefilename = 'usefulthings/filelistV17.txt'
fnamefile = open(fnamefilename)
lines = fnamefile.readlines()
a = fnamekeyword.strip()
shortfname = fnamekeyword.strip()
print 'going to check for ', shortfname
fnamefile.close()
c = TChain('TreeMaker2/PreSelection')
filelist = []
for line in lines:
    if not shortfname in line: continue
    fname = line.strip()
    if ('Summer16v3.QCD_HT' in fnamekeyword or 'WJets' in fnamekeyword): fname = ra2bspace+fname# or 'Summer16v3.WGJets_MonoPhoton' in fnamekeyword
    fname = fname.replace('/eos/uscms/','root://cmsxrootd.fnal.gov//')
    #if 'WGJets' in fnamekeyword: fname = fname.replace('root://cmsxrootd.fnal.gov///store/group/lpcsusyhad','root://hepxrd01.colorado.edu:1094//store/user/aperloff')
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


##Create output file
infileID = fnamekeyword.split('/')[-1].replace('.root','')+'_part'
newname = 'dyanalysis_'+infileID+'.root'
if issignal: 
    newname = newname.split('_')[0]+'_m'+str(par1)+'d'+str(par2)+'_time'+str(round(time.time()%100000,2))+'.root'
fnew = TFile(newname, 'recreate')
print 'creating', newname


print 'n(entries) =', n2process

hHt = TH1F('hHt','hHt',120,0,2500)
hHt.Sumw2()
hHtWeighted = TH1F('hHtWeighted','hHtWeighted',120,0,2500)
hHtWeighted.Sumw2()

tcounter = TTree('tcounter','tcounter')

hMassPPSV = makeTh1('hMassPPSV', 'hMassPPSV', 60, 60, 120, color=kBlack)
hMassFPSV = makeTh1('hMassFPSV', 'hMassFPSV', 60, 60, 120, color=kBlack)

t0 = time.time()
for ientry in range(n2process):

    if ientry%printevery==0:
        print "processing event", ientry, '/', n2process, 'time', time.time()-t0

    if ientry>nentries: break
    c.GetEntry(ientry)
    tcounter.Fill()

    
    recoelectrons = []
    for iel, el in enumerate(c.Electrons):
        if not el.Pt()>20: continue
        if not c.Electrons_mediumID[iel]: continue
        if not c.Electrons_passIso[iel]: continue        
        tlvel = TLorentzVector()
        tlvel.SetPtEtaPhiE(el.Pt(), el.Eta(), el.Phi(), el.Pt()*TMath.CosH(el.Eta()))
        usefulele = UsefulJet(tlvel, 0, 0, -1)	
        if not abs(el.Eta())<2.4: continue		
        recoelectrons.append(tlvel)
    if not len(recoelectrons)==1: continue


    recophotons_ppsv = []
    recophotons_fpsv = []
    
    for ipho, pho in enumerate(c.Photons):
        if not pho.Pt()>75: continue #trigger is pho 70
        if not bool(c.Photons_fullID[ipho]): continue ##need to BOOL this?
        if not abs(pho.Eta())<2.4: continue
        tlvpho = TLorentzVector()
        tlvpho.SetPtEtaPhiE(pho.Pt(), pho.Eta(), pho.Phi(), pho.E())  
        usefulpho = UsefulJet(tlvpho, 0, 0, -1)
        if not recoelectrons[0].DeltaR(usefulpho.tlv)>0.2: continue
               
        if bool(c.Photons_hasPixelSeed[ipho]): recophotons_ppsv.append(tlvpho)# loose photon
        else: recophotons_fpsv.append(tlvpho)# loose photon            
        
    if not (len(recophotons_fpsv)==1 or len(recophotons_ppsv)==1): continue

    if len(recophotons_ppsv)==1:
        invmass = (recoelectrons[0]+recophotons_ppsv[0]).M()
        fillth1(hMassPPSV, invmass)
        print ientry, 'PPSV mass', invmass
    if len(recophotons_fpsv)==1:
        invmass = (recoelectrons[0]+recophotons_fpsv[0]).M()
        fillth1(hMassFPSV, invmass)
        print ientry, 'FPSV mass', (recoelectrons[0]+recophotons_fpsv[0]).M()        


    
fnew.cd()
hMassFPSV.Write()
hMassPPSV.Write()
hHt.Write()
tcounter.Write()
print 'just created file', fnew.GetName()
fnew.Close()
