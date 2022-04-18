#Welcome to the industrial age of Sam's rebalance and smear code. You're going to have a lot of fun!
import os,sys
from ROOT import *
from array import array
from glob import glob
from utils import *
import numpy as np
import time

'''
python tools/makeElectronFakingPhotonTFs.py --fnamekeyword Summer16v3.WJetsToLNu_TuneCUETP8M1 --quickrun True
#ls /eos/uscms/store/group/lpcsusyPhotons/TreeMaker/Summer16v3.*
eosls /store/group/lpcsusyPhotons/TreeMaker/ |grep Summer16
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
    if quickrun and iadded>10: break
n2process = c.GetEntries()
nentries = c.GetEntries()
if quickrun: 
    n2process = min(100000,n2process)


print 'will analyze', n2process, 'events'
c.Show(0)

##Create output file
infileID = fnamekeyword.split('/')[-1].replace('.root','')+'_part'+str(extended)
newname = 'efg-'+infileID+'.root'
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


hGenElPt = TH1F('hGenElPt','hGenElPt',20,0,200)
histoStyler(hGenElPt, kGreen+1)
hGenElPtPhoMatched = TH1F('hGenElPtPhoMatched','hGenElPtPhoMatched',20,0,200)
histoStyler(hGenElPtPhoMatched, kOrange)
hGenElPtEleMatched = TH1F('hGenElPtEleMatched','hGenElPtEleMatched',20,0,200)
histoStyler(hGenElPtEleMatched, kTeal-4)

acme_objects = vector('TLorentzVector')()
recophotons = vector('TLorentzVector')()
recoelectrons = vector('TLorentzVector')()
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
    acme_objects.clear()
    
    if not (len(c.Photons)>0 or len(c.Electrons)>0 or len(c.Muons)>0): continue
    
    npasspixelseed = 0
    for iPho, Pho in enumerate(c.Photons):
        if not Pho.Pt()>20: continue #trigger is Pho 70
        if not abs(Pho.Eta())<2.4: continue        
        if not bool(c.Photons_fullID[iPho]): continue 
        tlvPho = TLorentzVector()
        tlvPho.SetPtEtaPhiE(Pho.Pt(), Pho.Eta(), Pho.Phi(), Pho.E())
        if not Pho.Pt()>10: continue
        if int(bool(c.Photons_hasPixelSeed[iPho])): recoelectrons.push_back(tlvPho)
        else: recophotons.push_back(tlvPho)
                

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
        if not abs(gp.Eta())<2.5: continue
        gptlv = TLorentzVector(gp.Px(),gp.Py(), gp.Pz(), gp.E())
        genelectrons.append(gptlv)
    for gene in genelectrons:
        fillth1(hGenElPt, gene.Pt())
        for pho in recophotons:
            dr = pho.DeltaR(gene)
            if dr<0.03: 
                fillth1(hGenElPtPhoMatched, gene.Pt())
                break
        for ele in recoelectrons:
            dr = ele.DeltaR(gene)
            if dr<0.03: 
                fillth1(hGenElPtEleMatched, gene.Pt())
                break                
        
    
    #MetVec = TLorentzVector()
    #MetVec.SetPtEtaPhiE(c.MET,0,c.METPhi,c.MET)

    #tHardMhtVec = TLorentzVector()
    #tHardMetVec = tHardMhtVec.Clone()
    
    
    #tHardMetPt, tHardMetPhi = tHardMetVec.Pt(), tHardMetVec.Phi()
    


fnew.cd()
fnew.cd('../')
hHt.Write()
hHtWeighted.Write()
hGenElPt.Write()
hGenElPtPhoMatched.Write()
hGenElPtEleMatched.Write()
hfilterfails.Write()
tcounter.Write()


print 'just created', fnew.GetName()
fnew.Close()



'''
tree->GetBranch("xxx")->SetName("yyy");
tree->GetLeaf("xxx")->SetTitle("yyy");
'''
