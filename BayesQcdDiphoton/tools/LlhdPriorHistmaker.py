from ROOT import *
from utils import *
import os, sys
from glob import glob


MetConstraintName = 'HardMetPt'
#MetConstraintName = 'MetSignificance'

mettyobject_code_dict = {}
mettyobject_code_dict['HardMetPt'] = 0
mettyobject_code_dict['MetSignificance'] = 1
mettyobject_code = mettyobject_code_dict[MetConstraintName]

###stuff that would be nice in a config file
binPt = [0,8,10,15,20,25,30,35,40,50,70,100,150,200,300,400,500,700,1000,10000]
#binPt = [0,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,44,48,52,56,60,66,72,78,84,90,100,110,120,130,140,150,160,170,180,190,200,220,240,260,280,300,330,360,390,420,450,500,550,600,650,700,750,800,900,1000,10000]
binEta = [0,0.4,0.8,1.2,1.6,2.0,2.5,6.0]#using this march 7 2017
binHt = [0,10000]

##load in delphes libraries to access input collections:
gSystem.Load("/nfs/dust/cms/user/beinsam/RebalanceAndSmear/CMSSW_10_1_0/src/SampleProduction/delphes/build/libDelphes")

##load in UsefulJet class, which the rebalance and smear code uses
gROOT.ProcessLine(open('src/UsefulJet.cc').read())
exec('from ROOT import *')
gROOT.ProcessLine(open('src/BayesRandS.cc').read())
exec('from ROOT import *')

##read in command line arguments
defaultInfile_ = "../SampleProduction/delphes/delphes_qcd1.root"
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=10000,help="analyzer script to batch")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile_,help="file")
parser.add_argument("-quickrun", "--quickrun", type=bool, default=False,help="short run")
args = parser.parse_args()
quickrun = args.quickrun
fnamekeyword = args.fnamekeyword
inputFiles = glob(fnamekeyword)
verbosity = args.verbosity
llhdMhtThresh = 15
BTag_Cut = 0.5 #delphes b-tagging is binary, so any number between 0 and 1 here would do

##declare and load a tree
c = TChain('Delphes')
for fname in inputFiles: 
	print 'adding', fname
	c.Add(fname)

c.Show(0)
nentries = c.GetEntries()
if quickrun: nentries = min(1000,nentries)
print 'n(entries) =', nentries

##feed the tree to delphes, set up which branches need to be used
treeReader = ExRootTreeReader(c)
numberOfEntries = treeReader.GetEntries()
branchJets = treeReader.UseBranch("Jet")
branchHT = treeReader.UseBranch("ScalarHT")
branchGenJet = treeReader.UseBranch("GenJet")
branchMissingET = treeReader.UseBranch("MissingET")
branchPhoton = treeReader.UseBranch("Photon")
branchElectron = treeReader.UseBranch("Electron")
branchMuon = treeReader.UseBranch("Muon")

##Create output file
newname = 'llhd-prior-hists-'+fnamekeyword.split('/')[-1].replace('.root','')+'.root'
fnew = TFile(newname, 'recreate')
print 'creating', newname

hHt       = makeTh1("hHt","HT for number of events", 250,0,5000)
hResponseVsGenPt = TH2F('gResponseVsGenPt','gResponseVsGenPt',1000,0,1000,400,0,4)
binPtArr = array('d',binPt)
nBinPt = len(binPtArr)-1
hPtTemplate = TH1F('hPtTemplate','hPtTemplate',nBinPt,binPtArr)
templatePtAxis = hPtTemplate.GetXaxis()
binEtaArr = array('d',binEta)
nBinEta = len(binEtaArr)-1
hEtaTemplate = TH1F('hEtaTemplate','hEtaTemplate',nBinEta,binEtaArr)
templateEtaAxis = hEtaTemplate.GetXaxis()
binHtArr = array('d',binHt)
nBinHt = len(binHtArr)-1
hHtTemplate = TH1F('hHtTemplate','hHtTemplate',nBinHt,binHtArr)
templateHtAxis = hHtTemplate.GetXaxis()

hResGenTemplates = ['']
hResRecTemplates = ['']
hResGenTemplatesB = ['']
for ieta in range(1,templateEtaAxis.GetNbins()+1):
	hResGenTemplates.append([''])
	hResGenTemplatesB.append([''])
	hResRecTemplates.append([''])
	etarange = str(templateEtaAxis.GetBinLowEdge(ieta))+'-'+str(templateEtaAxis.GetBinUpEdge(ieta))
	for ipt in range(1,templatePtAxis.GetNbins()+1):
		lowedge = templatePtAxis.GetBinLowEdge(ipt)
		upedge = templatePtAxis.GetBinUpEdge(ipt)
		ptrange = str(lowedge)+'-'+str(upedge)
		if int(lowedge)<17:
			nbins = 650
			rupper = 4.0
		else:
			nbins = 350
			rupper = 3.0
		hg = TH1F('hRTemplate(gPt'+ptrange+', gEta'+etarange+')','pt(gen)',nbins,0,rupper)
		hg.Sumw2()
		hResGenTemplates[-1].append(hg)
		hgb = hg.Clone(hg.GetName()+'B')
		hResGenTemplatesB[-1].append(hgb)
		hr = TH1F('hRTemplate(rPt'+ptrange+', rEta'+etarange+')','pt(reco)',nbins,0,rupper)
		hr.Sumw2()
		hResRecTemplates[-1].append(hr)


binHardMetArr = array('d',binning_templates['HardMet'])
nBinHardMet = len(binHardMetArr)-1

if MetConstraintName=='HardMetPt': binMetConstraintArr = array('d',binning_templates['HardMet'])
	
if MetConstraintName=='MetSignificance': binMetConstraintArr = array('d',binning_templates['MetSignificance'])

nBinMetConstraint = len(binMetConstraintArr)-1

nbinsDphi = binning_templates['DPhi1'][0]
lowDphi = binning_templates['DPhi1'][1]
highDphi = binning_templates['DPhi1'][2]


hMetConstraintTemplatesB0 = ['']
hMetConstraintTemplatesB1 = ['']
hMetConstraintTemplatesB2 = ['']
hMetConstraintTemplatesB3 = ['']
hHardMetPhiTemplatesB0 = ['']
hHardMetPhiTemplatesB1 = ['']
hHardMetPhiTemplatesB2 = ['']
hHardMetPhiTemplatesB3 = ['']

for iht in range(1,templateHtAxis.GetNbins()+2):
	htrange = str(templateHtAxis.GetBinLowEdge(iht))+'-'+str(templateHtAxis.GetBinUpEdge(iht))
	hMetConstraintB0 = TH1F('hGen'+MetConstraintName+'PtB0(ght'+htrange+')','hGen'+MetConstraintName+'PtB0(ght'+htrange+')',nBinMetConstraint,binMetConstraintArr)
	hGenHardMetPhiB0 = TH1F('hGenHardMetDPhiB0(ght'+htrange+')','hGenHardMetDPhiB0(ght'+htrange+')',nbinsDphi,lowDphi,highDphi)
	hMetConstraintTemplatesB0.append(hMetConstraintB0)
	hHardMetPhiTemplatesB0.append(hGenHardMetPhiB0)
	hMetConstraintB1 = TH1F('hGen'+MetConstraintName+'PtB1(ght'+htrange+')','hGen'+MetConstraintName+'PtB1(ght'+htrange+')',nBinMetConstraint,binMetConstraintArr)
	hGenHardMetPhiB1 = TH1F('hGenHardMetDPhiB1(ght'+htrange+')','hGenHardMetDPhiB1(ght'+htrange+')',nbinsDphi,lowDphi,highDphi)
	hMetConstraintTemplatesB1.append(hMetConstraintB1)
	hHardMetPhiTemplatesB1.append(hGenHardMetPhiB1)
	hMetConstraintB2 = TH1F('hGen'+MetConstraintName+'PtB2(ght'+htrange+')','hGen'+MetConstraintName+'PtB2(ght'+htrange+')',nBinMetConstraint,binMetConstraintArr)
	hGenHardMetPhiB2 = TH1F('hGenHardMetDPhiB2(ght'+htrange+')','hGenHardMetDPhiB2(ght'+htrange+')',nbinsDphi,lowDphi,highDphi)
	hMetConstraintTemplatesB2.append(hMetConstraintB2)
	hHardMetPhiTemplatesB2.append(hGenHardMetPhiB2)
	hMetConstraintB3 = TH1F('hGen'+MetConstraintName+'PtB3(ght'+htrange+')','hGen'+MetConstraintName+'PtB3(ght'+htrange+')',nBinMetConstraint,binMetConstraintArr)
	hGenHardMetPhiB3 = TH1F('hGenHardMetDPhiB3(ght'+htrange+')','hGenHardMetDPhiB3(ght'+htrange+')',nbinsDphi,lowDphi,highDphi)
	hMetConstraintTemplatesB3.append(hMetConstraintB3)
	hHardMetPhiTemplatesB3.append(hGenHardMetPhiB3)

for ientry in range(nentries):
	if ientry%verbosity==0: print 'now processing event number', ientry, 'of', nentries
	c.GetEntry(ientry) 	
	treeReader.ReadEntry(ientry)
	fillth1(hHt, branchHT[0].HT)


	##some universal selection
	weight = 1
		
	if not len(list(branchPhoton))==0: continue
	if not len(list(branchElectron))==0: continue
	if not len(list(branchMuon))==0: continue		
	
	
	##declare empty vector of UsefulJets (in c++, std::vector<UsefulJet>):
	recojets = vector('UsefulJet')()

	#build up the vector of jets using TLorentzVectors; 
	#this is where you have to interface with the input format you're using
	for ijet, jet in enumerate(branchJets):
		if not jet.PT>15: continue
		if not abs(jet.Eta)<5: continue
		tlvjet = TLorentzVector()
		tlvjet.SetPtEtaPhiE(jet.PT, jet.Eta, jet.Phi, jet.PT*TMath.CosH(jet.Eta))
		ujet = UsefulJet(tlvjet, jet.BTag)
		recojets.push_back(ujet)

	genjets = vector('UsefulJet')()
	#build up the vector of jets using TLorentzVectors; 
	#this is where you have to interface with the input format you're using
	for ijet, jet in enumerate(branchGenJet):
		if not jet.PT>15: continue
		if not abs(jet.Eta)<5: continue
		tlvjet = TLorentzVector()
		tlvjet.SetPtEtaPhiE(jet.PT, jet.Eta, jet.Phi, jet.PT*TMath.CosH(jet.Eta))
		ujet = UsefulJet(tlvjet, jet.BTag)
		genjets.push_back(ujet)

	ght = getHt(genjets, 30)# make HT include the neutrinos 
	iht = templateHtAxis.FindBin(ght)      


	gHardMetVec = getHardMet(genjets,lhdMhtThresh)# changed from genjets, why not?
	gHardMetPt, gHardMetPhi = gHardMetVec.Pt(), gHardMetVec.Phi()
	RecoMetVec = mkmet(branchMissingET[0].MET,branchMissingET[0].Phi)

	if mettyobject_code==0: mettyobject = gHardMetPt
	if mettyobject_code==1: 
		if ght>0: mettyobject = gHardMetPt/TMath.Sqrt(ght)
		else: mettyobject = -1.0
			
	for gjet in genjets:
		if not (gjet.Pt()>2):continue
		geta = abs(gjet.Eta())
		if not (geta<6): continue
		ieta = templateEtaAxis.FindBin(geta)               
		gpt = gjet.Pt()
		ipt = templatePtAxis.FindBin(gpt)

		sumGpt = calcSumPt(genjets, gjet, 0.7, 2)
		ratioGPtSumpt1 = gjet.Pt()/sumGpt
		if not ratioGPtSumpt1 > 0.98: continue #g-isolation
		matched = False
		isolated = False
		dRbig = 9
		ratioRPtSumpt1 = 1
		recoCsv = -1
		for ireco, rjet in enumerate(recojets):
			dR_ = rjet.DeltaR(gjet.tlv)
			if dR_<0.5 and dR_<dRbig:
				dRbig = dR_
				matched = True
				pt0 = rjet.Pt()
				variation = 0 # this can be used for JER scale factors
				pt1 = max(0.,gpt+(1+variation)*(pt0-gpt))
				response = pt1/gpt
				sumpt = calcSumPt(recojets, rjet, 0.8, 0)###0.8 is twice jet radius
				ratioRPtSumpt1 = rjet.Pt()/sumpt
				recoCsv = rjet.csv
				if dR_<0.4:  break # if there's not one within 0.4, keep looking
		if ratioRPtSumpt1 > 0.98: isolated = True
		if not isolated: continue
		if not matched: continue
		if recoCsv<BTag_Cut:
			hResGenTemplates[ieta][ipt].Fill(response,weight)
		else:   hResGenTemplatesB[ieta][ipt].Fill(response,weight)
		hResponseVsGenPt.Fill(gpt,response,weight)

	nbtags = countBJets(recojets, llhdMhtThresh, BTag_Cut)###
	nGenJets = countJets(genjets, 30)    
	if nbtags>2: 
		if nGenJets>2:
			genBjet = getLeadingGenBJet(genjets, recojets, BTag_Cut)

			hMetConstraintTemplatesB3[iht].Fill(mettyobject,weight)
			hHardMetPhiTemplatesB3[iht].Fill(abs(genBjet.tlv.DeltaPhi(gHardMetVec)),weight)
	elif nbtags>1: 
		if nGenJets>1:
			genBjet = getLeadingGenBJet(genjets, recojets, BTag_Cut)
			hMetConstraintTemplatesB2[iht].Fill(mettyobject,weight)
			hHardMetPhiTemplatesB2[iht].Fill(abs(genBjet.tlv.DeltaPhi(gHardMetVec)),weight)
	elif nbtags>0: 
		if nGenJets>1:
			genBjet = getLeadingGenBJet(genjets, recojets, BTag_Cut)
			hMetConstraintTemplatesB1[iht].Fill(mettyobject,weight)
			hHardMetPhiTemplatesB1[iht].Fill(abs(genBjet.tlv.DeltaPhi(gHardMetVec)),weight)
	elif nGenJets>1:
		hMetConstraintTemplatesB0[iht].Fill(mettyobject,weight)
		hHardMetPhiTemplatesB0[iht].Fill(abs(genjets[0].tlv.DeltaPhi(gHardMetVec)),weight)
	
	#if ientry>5: 
	#	exit(0)

	jets = branchJets
	#for ijet, jet in enumerate(jets):
	#	print ijet, jet.PT, jet.Eta, jet.Phi, jet.BTag

	#fillth1(hHt, getattr(c, 'ScalarHT.HT'))	
	#if ientry>3: break

fnew.cd()
hHt.Write()

for etachain in hResGenTemplates[1:]:
	for hrat in etachain[1:]:
		hrat.Write()
		continue 

for etachain in hResGenTemplatesB[1:]:
	for hrat in etachain[1:]:
		hrat.Write()
		continue

for h in hMetConstraintTemplatesB0[1:]: h.Write()
for h in hMetConstraintTemplatesB1[1:]: h.Write()
for h in hMetConstraintTemplatesB2[1:]: h.Write()
for h in hMetConstraintTemplatesB3[1:]: h.Write()
for h in hHardMetPhiTemplatesB0[1:]: h.Write()
for h in hHardMetPhiTemplatesB1[1:]: h.Write()
for h in hHardMetPhiTemplatesB2[1:]: h.Write()
for h in hHardMetPhiTemplatesB3[1:]: h.Write()

hResponseVsGenPt.Write()
hHt.Write()
#hHtWeighted.Write()
hPtTemplate.Write()
hEtaTemplate.Write()
hHtTemplate.Write()

print 'just created', newname
fnew.Close()

