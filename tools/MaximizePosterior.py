#Welcome to the industrial age of Sam's rebalance and smear code. You're going to have a lot of fun!
import os,sys
from ROOT import *
from array import array
from glob import glob
from utils import *
#from ra2blibs import *
import time

###stuff that would be nice in a config file
mhtjetetacut = 5.0 # also needs be be changed in UsefulJet.h
lhdHardMetJetPtCut = 15.0
AnHardMetJetPtCut = 30.0
cutoff = 15.0
isdata = False
rebalancedMetCut = 110
rebalancedMetCut = 150


debugmode = False


##load in delphes libraries to access input collections:
gSystem.Load("/nfs/dust/cms/user/beinsam/RebalanceAndSmear/CMSSW_10_1_0/src/SampleProduction/delphes/build/libDelphes")
##load in UsefulJet class, which the rebalance and smear code uses
gROOT.ProcessLine(open('src/UsefulJet.cc').read())
exec('from ROOT import *')
gROOT.ProcessLine(open('src/BayesRandS.cc').read())
exec('from ROOT import *')


##read in command line arguments
defaultInfile_ = "../SampleProduction/delphes/delphes_gjet4.root"
#T2qqGG.root
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=1,help="analyzer script to batch")
parser.add_argument("-printevery", "--printevery", type=int, default=100000,help="short run")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile_,help="file")
parser.add_argument("-bootstrap", "--bootstrap", type=str, default='0',help="boot strapping (0,1of5,2of5,3of5,...)")
parser.add_argument("-quickrun", "--quickrun", type=bool, default=False,help="short run")
args = parser.parse_args()
fnamekeyword = args.fnamekeyword
inputFiles = glob(fnamekeyword)
bootstrap = args.bootstrap
verbosity = args.verbosity
printevery = args.printevery
quickrun = args.quickrun
if quickrun: 
	n2process = 200000
	if 'T2' in fnamekeyword: n2process = 20000
else: n2process = 9999999999999
llhdHardMetThresh = 15
mktree = False
BTag_Cut = 0.5 #Delphes b-tagging binary
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


#Dictionary list of signal regions
regionCuts = {}
pi = 3.14159
Inf = 9999
#varlist =                            ['St',    'HardMet','NJets','BTags','DPhiPhoPho','NPhotons', 'MetSignificance']
regionCuts['NoCuts']                = [[0,Inf],  [0,Inf], [0,Inf],[0,Inf],[-Inf,Inf],    [1,Inf],  [-1,Inf]]
regionCuts['Baseline1Pho']          = [[200,Inf],[90,Inf],[0,Inf],[0,Inf],[-Inf,Inf],    [1,1],    [-1,Inf]]
regionCuts['Baseline2Pho']          = [[200,Inf],[90,Inf],[0,Inf],[0,Inf],[-Inf,Inf],    [2,Inf],  [-1,Inf]]


##declare and load a tree
c = TChain('Delphes')
for fname in inputFiles: 
	print 'adding', fname
	c.Add(fname)
nentries = c.GetEntries()
c.Show(0)
n2process = min(n2process, nentries)
print 'n(entries) =', n2process

##feed the tree to delphes, set up which branches need to be used
treeReader = ExRootTreeReader(c)
numberOfEntries = treeReader.GetEntries()
branchHT = treeReader.UseBranch("ScalarHT")
branchJets = treeReader.UseBranch("Jet")
branchGenJet = treeReader.UseBranch("GenJet")
branchMissingET = treeReader.UseBranch("MissingET")
branchGenMissingET = treeReader.UseBranch("GenMissingET")
branchPhoton = treeReader.UseBranch("Photon")
branchElectron = treeReader.UseBranch("Electron")
branchMuon = treeReader.UseBranch("Muon")


branchParticles = treeReader.UseBranch("Particle")


varlist = ['St','HardMet','NJets','BTags','DPhiPhoPho','NPhotons', 'MetSignificance']
indexVar = {}
for ivar, var in enumerate(varlist): indexVar[var] = ivar
indexVar[''] = -1
nmain = len(varlist)

def selectionFeatureVector(fvector, regionkey='', omitcuts='', omitcuts_dphi=''):
	iomits, iomits_dphi = [], []  
	for cut in omitcuts.split('Vs'): iomits.append(indexVar[cut])
	for i, feature in enumerate(fvector):
		if i==nmain: break
		if i in iomits: continue
		if not (feature>=regionCuts[regionkey][i][0] and feature<=regionCuts[regionkey][i][1]): 
			return False
	return True


templateFileName = 'usefulthings/llhd-prior-coarse-ak4.root'
templateFileName = 'usefulthings/llhd-prior-coarse-ak4-extra.root'
#templateFileName = 'usefulthings/llhd-prior-MetSignificance.root'
ftemplate = TFile(templateFileName)
print 'using templates from',templateFileName
hPtTemplate = ftemplate.Get('hPtTemplate')
templatePtAxis = hPtTemplate.GetXaxis()
hEtaTemplate = ftemplate.Get('hEtaTemplate')
templateEtaAxis = hEtaTemplate.GetXaxis()

hHtTemplate = ftemplate.Get('hHtTemplate')
templateStAxis = hHtTemplate.GetXaxis()

'''#option for using FullSim-based prior
priorFileName = templateFileName
priorFileName = 'usefulthings/ResponseFunctionsMC17AllFilters_deepCsv.root'
fprior = TFile(priorFileName)
hHtTemplate = fprior.Get('hHtTemplate')
templateStAxis = hHtTemplate.GetXaxis()
'''

##Create output file
infileID = fnamekeyword.split('/')[-1].replace('.root','')
newname = 'posterior-'+infileID+'.root'
fnew = TFile(newname, 'recreate')
print 'creating', newname
if mktree:
	treefile = TFile('littletreeLowHardMet'+fnamekeyword+'.root','recreate')
	littletree = TTree('littletree','littletree')
	prepareLittleTree(littletree)

hSt = TH1F('hSt','hSt',120,0,2500)
hSt.Sumw2()
hStWeighted = TH1F('hStWeighted','hStWeighted',120,0,2500)
hStWeighted.Sumw2()
hGenMetGenHardMetRatio = TH1F('hGenMetGenHardMetRatio','hGenMetGenHardMetRatio',50,0,5)
hGenMetGenHardMetRatio.Sumw2()
hPassFit = TH1F('hPassFit','hPassFit',5,0,5)
hPassFit.Sumw2()
hTotFit = TH1F('hTotFit','hTotFit',5,0,5)
hTotFit.Sumw2()


GleanTemplatesFromFile(ftemplate)#, fprior)

histoStructDict = {}
for region in regionCuts:
	for var in varlist:
		histname = region+'_'+var
		histoStructDict[histname] = mkHistoStruct(histname, binning)

xsec_times_lumi_over_nevents = 1.0
t0 = time.time()
for ientry in range(n2process):


	if ientry%printevery==0:
		print "processing event", ientry, '/', n2process, 'time', time.time()-t0
		
	if debugmode:
		#if not ientry>122000: continue
		if not ientry > 139833: continue#,139832,183619]: continue#,30548,49502]: continue
		a = 2
	c.GetEntry(ientry)

	weight = xsec_times_lumi_over_nevents
	
	#if not branchMissingET[0].MET>100: continue
	
	acme_objects = vector('TLorentzVector')()
	recophotons = vector('TLorentzVector')()
	#build up the vector of jets using TLorentzVectors; 
	#this is where you have to interface with the input format you're using
	if not len(branchPhoton)>0: continue
	for ipho, pho in enumerate(branchPhoton):
		if not pho.PT>30: continue
		tlvpho = TLorentzVector()
		tlvpho.SetPtEtaPhiE(pho.PT, pho.Eta, pho.Phi, pho.E)
		if debugmode:
			#print ientry, 'acme photon', pho.PT, pho.Eta, pho.Phi
			a=2
		acme_objects.push_back(tlvpho)			
		if not abs(pho.Eta)<2.4: continue		
		recophotons.push_back(tlvpho)			
	
	#123672 acme photon 379.416259766 1.68068277836 -2.87252449989	
	##some universal selection (filters, etc)
	# <insert any event filters here>
	if not int(recophotons.size())>0: continue
	
	if len(recophotons)>1: dphi = abs(recophotons[0].DeltaPhi(recophotons[1]))
	else: dphi = -1
		
	recoelectrons = vector('TLorentzVector')()
	#build up the vector of jets using TLorentzVectors; 
	#this is where you have to interface with the input format you're using
	for iel, el in enumerate(branchElectron):
		if not el.PT>30: continue
		tlvel = TLorentzVector()
		tlvel.SetPtEtaPhiE(el.PT, el.Eta, el.Phi, el.PT*TMath.CosH(el.Eta))
		if debugmode:
			print ientry, 'acme electron', el.PT		
		acme_objects.push_back(tlvel)		
		if not abs(el.Eta)<2.4: continue		
		recoelectrons.push_back(tlvel)
		
	recomuons = vector('TLorentzVector')()
	#build up the vector of jets using TLorentzVectors; 
	#this is where you have to interface with the input format you're using
	for imu, mu in enumerate(branchMuon):
		if not mu.PT>30: continue
		tlvmu = TLorentzVector()
		tlvmu.SetPtEtaPhiE(mu.PT, mu.Eta, mu.Phi, mu.PT*TMath.CosH(mu.Eta))
		if debugmode:
			print ientry, 'acme muon', mu.PT				
		acme_objects.push_back(tlvmu)			
		if not abs(mu.Eta)<2.4: continue		
		recomuons.push_back(tlvmu)				
	
	AcmeVector = TLorentzVector()
	AcmeVector.SetPxPyPzE(0,0,0,0)
	for obj in acme_objects: AcmeVector+=obj		
	
	_Templates_.AcmeVector = AcmeVector	
	
	##declare empty vector of UsefulJets (in c++, std::vector<UsefulJet>):
	recojets = vector('UsefulJet')()

	#build up the vector of jets using TLorentzVectors; 
	#this is where you have to interface with the input format you're using
	onlygoodjets = True
	for ijet, jet in enumerate(branchJets):
		if not jet.PT>15: continue
		if not abs(jet.Eta)<5: continue
		tlvjet = TLorentzVector()
		tlvjet.SetPtEtaPhiE(jet.PT, jet.Eta, jet.Phi, jet.PT*TMath.CosH(jet.Eta))
		ujet = UsefulJet(tlvjet, jet.BTag)
		if calcMinDr(acme_objects, ujet, 0.3)<0.3:
			continue
		recojets.push_back(ujet)
		if ujet.Pt()>50 and jet.EhadOverEem>100: 
			onlygoodjets = False
			break
	if not onlygoodjets: continue

	genjets_ = vector('TLorentzVector')()
	#build up the vector of jets using TLorentzVectors; 
	#this is where you have to interface with the input format you're using
	for ijet, jet in enumerate(branchGenJet):
		#if not jet.PT>15: continue
		#if not abs(jet.Eta)<5: continue
		tlvjet = TLorentzVector()
		tlvjet.SetPtEtaPhiE(jet.PT, jet.Eta, jet.Phi, jet.PT*TMath.CosH(jet.Eta))
		if calcMinDr(acme_objects, tlvjet, 0.3)<0.3: 
			#if debugmode: 
			#	print 'throwing away jet with pT, eta', jet.PT, jet.Eta
			#	print 'gen dr was', calcMinDr(acme_objects, tlvjet, 0.01)
			continue		
		genjets_.push_back(tlvjet)
	gHt = getHt(genjets_,AnHardMetJetPtCut)
	gSt = gHt
	for obj in acme_objects: gSt+=obj.Pt()
	fillth1(hSt, gSt,1)
	
	matchedCsvVec = createMatchedCsvVector(genjets_, recojets)
	genjets = CreateUsefulJetVector(genjets_, matchedCsvVec)

	##a few global objects
	MetVec = TLorentzVector()
	MetVec.SetPtEtaPhiE(branchMissingET[0].MET,0,branchMissingET[0].Phi,branchMissingET[0].MET)

	##observed histogram
	tHt = getHt(recojets,AnHardMetJetPtCut)
	tSt = tHt
	for obj in acme_objects: tSt+=obj.Pt()
	tHardMetVec = getHardMet(recojets,AnHardMetJetPtCut, mhtjetetacut)
	tHardMhtVec = tHardMetVec.Clone()
	tHardMetVec-=AcmeVector
	tHardMetPt, tHardMetPhi = tHardMetVec.Pt(), tHardMetVec.Phi()
	tHardMhtPt, tHardMhtPhi = tHardMhtVec.Pt(), tHardMhtVec.Phi()
	

	
	met_consistency = abs(branchMissingET[0].MET-tHardMetPt)/tHardMetPt
	if not met_consistency<0.5: continue
		
	if tHt>0: tMetSignificance = tHardMetPt/TMath.Sqrt(tHt)
	else: tMetSignificance = 8
	tNJets = countJets(recojets,AnHardMetJetPtCut)
	tBTags = countBJets(recojets,AnHardMetJetPtCut)

	if debugmode:
		if not tHardMetPt>150: continue
		
	fv = [tSt,tHardMetPt,tNJets,tBTags,dphi, int(recophotons.size()),tMetSignificance]
	for regionkey in regionCuts:
		for ivar, varname in enumerate(varlist):
			hname = regionkey+'_'+varname
			if selectionFeatureVector(fv,regionkey,varname,''): 
				fillth1(histoStructDict[hname].Observed, fv[ivar], weight)

	if mktree:
		if fv[1]>=150 and fv[1]<=200 and fv[0]>500 and fv[2]>3:
			growTree(littletree, fv, jetPhis, weight)            
		
	#if tHt>0 and (tHardMetPt>50 and tMetSignificance>3):
	fitsucceed = RebalanceJets(recojets)
	rebalancedJets = _Templates_.dynamicJets
	#else:
	#	fitsucceed = True
	#	rebalancedJets = recojets
	mHt = getHt(rebalancedJets,AnHardMetJetPtCut)
	mSt = mHt
	for obj in acme_objects: mSt+=obj.Pt()
	mHardMetVec = getHardMet(rebalancedJets,AnHardMetJetPtCut, mhtjetetacut)
	mHardMetVec-=AcmeVector
	mHardMetPt, mHardMetPhi = mHardMetVec.Pt(), mHardMetVec.Phi()
	if mHt>0: mMetSignificance = mHardMetPt/TMath.Sqrt(mHt)
	else: mMetSignificance = 8	

	mNJets = countJets(rebalancedJets,AnHardMetJetPtCut)
	mBTags = countBJets(rebalancedJets,AnHardMetJetPtCut)###

	#hope = (fitsucceed and mHardMetPt<rebalancedMetCut)# mHardMetPt>min(mSt/2,180):# was 160
	#hope = (fitsucceed and mSignificance<rebalancedSignificanceCut)# mHardMetPt>min(mSt/2,180):# was 160
	hope = (fitsucceed and mHardMetPt<rebalancedMetCut)# mHardMetPt>min(mSt/2,180):# was 160	

	redoneMET = redoMET(MetVec,recojets,rebalancedJets)
	mMetPt,mMetPhi = redoneMET.Pt(), redoneMET.Phi()
	#mindphi = 4
	#for jet in rebalancedJets[:4]: mindphi = min(mindphi, abs(jet.DeltaPhi(mHardMetVec)))	
	fv = [mSt,mHardMetPt,mNJets,mBTags,dphi, int(recophotons.size()),mMetSignificance]

	for regionkey in regionCuts:      
		for ivar, varname in enumerate(varlist):
			hname = regionkey+'_'+varname
			if selectionFeatureVector(fv,regionkey,varname,''): 
				fillth1(histoStructDict[hname].Rebalanced, fv[ivar],weight)

	fillth1(hTotFit, fv[3], weight)
 
	if hope: fillth1(hPassFit, fv[3], weight)

	nsmears = 100*bootupfactor
	weight = xsec_times_lumi_over_nevents / nsmears

	for i in range(nsmears):

		if not hope: break
		RplusSJets = smearJets(rebalancedJets,99+_Templates_.nparams)
		rpsHt = getHt(RplusSJets,AnHardMetJetPtCut)
		rpsSt = rpsHt
		for obj in acme_objects: rpsSt+=obj.Pt()
		rpsHardMetVec = getHardMet(RplusSJets,AnHardMetJetPtCut, mhtjetetacut)
		rpsHardMetVec-=AcmeVector
		rpsHardMetPt, rpsHardMetPhi = rpsHardMetVec.Pt(), rpsHardMetVec.Phi()
		if rpsHt>0: rpsMetSignificance = rpsHardMetPt/TMath.Sqrt(rpsHt)
		else: rpsMetSignificance = 8			
		rpsNJets = countJets(RplusSJets,AnHardMetJetPtCut)
		rpsBTags = countBJets(RplusSJets,AnHardMetJetPtCut)
		fv = [rpsSt,rpsHardMetPt,rpsNJets,rpsBTags,dphi, int(recophotons.size()),rpsMetSignificance]
		#print i, 'of', nsmears, fv
		for regionkey in regionCuts:     
			for ivar, varname in enumerate(varlist):
				hname = regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname,''):
					fillth1(histoStructDict[hname].RplusS, fv[ivar],weight)
		if mktree and 'JetHT' in physicsProcess and fv[1]>=150 and fv[1]<200 and fv[0]>=500 and fv[2]>=4: 
			growTree(littletree, fv, jetPhis, weight)


	if isdata: continue    
	genMetVec = mkmet(branchGenMissingET[0].MET, branchGenMissingET[0].Phi)
	weight = xsec_times_lumi_over_nevents


	weight = xsec_times_lumi_over_nevents
	gHt = getHt(genjets,AnHardMetJetPtCut)
	gSt = gHt
	for obj in acme_objects: gSt+=obj.Pt()
	
	gHardMetVec = getHardMet(genjets,AnHardMetJetPtCut, mhtjetetacut)
	gHardMetVec-=AcmeVector
	gHardMetPt, gHardMetPhi = gHardMetVec.Pt(), gHardMetVec.Phi()
	if gHt>0: gMetSignificance = gHardMetPt/TMath.Sqrt(gHt)
	else: gMetSignificance = 8	
	
	###Delphes filter, because I think Delphes is mis-computing its own gen MET
	if gHardMetPt>80: 
		fillth1(hGenMetGenHardMetRatio,abs(gHardMetPt-genMetVec.Pt())/gHardMetPt)
		if abs(gHardMetPt-genMetVec.Pt())/gHardMetPt>0.5: 
			print 'skipping', ientry, gHardMetPt, genMetVec.Pt()
			continue
	###Delphes
		
	gNJets = countJets(genjets,AnHardMetJetPtCut)
	gBTags = countBJets(genjets,AnHardMetJetPtCut)
	

	if debugmode:
		c.Show(ientry)
		print 'ientry', ientry, [tSt,tHardMetPt,tNJets,tBTags,dphi, int(recophotons.size()),tMetSignificance]
		print 'missingET', branchMissingET[0].MET
		print 'gen missingET', genMetVec.Pt()
		print 'genHardMet', gHardMetVec.Pt(), gHardMetVec.Phi()		
		print 'genjets'
		for ijet, jet in enumerate(genjets):
			print ijet, jet.Pt(), jet.Eta(), jet.Phi()
		print 'recoHardMet', tHardMetVec.Pt(), tHardMetVec.Phi()
		print 'recojets:'
		for ijet, jet in enumerate(recojets):
			print ijet, jet.Pt(), jet.Eta(), jet.Phi()
			matchedgen = calcMinDr(genjets, jet, 0.01)
			print 'matchedgenjet pt', matchedgen.Pt(), matchedgen.Eta(), matchedgen.Phi(), 'dr', matchedgen.DeltaR(jet.tlv)
			print 'particles in der naher:'
			for igp_, gp_ in enumerate(branchParticles):
				#if not gp_.PT>10: continue
				if not gp_.Status==1: continue
				gp = TLorentzVector()
				gp.SetPtEtaPhiE(gp_.PT,gp_.Eta,gp_.Phi,gp_.E)
				dr = gp.DeltaR(jet.tlv)
				if dr<0.8:
					print igp_, '('+str(gp_.PID)+', status='+str(gp_.Status)+')', 'particle', gp.Pt(), gp.Eta(), gp.Phi(), 'DR=', dr
			
		print 'acme_objects'
		for ijet, jet in enumerate(acme_objects):
			print ijet, jet.Pt(), jet.Eta(), jet.Phi()
					
		print 'other particles:'
		for ijet, jet in enumerate(branchParticles):
			part = TLorentzVector()
			if not jet.PT>10: continue
			print ijet, jet.PT, jet.Eta, jet.Phi, '('+str(jet.PID)+')', '-'+str(jet.Status)
		
	fv = [gSt,gHardMetPt,gNJets,gBTags,dphi, int(recophotons.size()),gMetSignificance]	
	for regionkey in regionCuts:
		for ivar, varname in enumerate(varlist):
			hname = regionkey+'_'+varname
			if selectionFeatureVector(fv,regionkey,varname,''): 
				fillth1(histoStructDict[hname].Gen, fv[ivar],weight)

	#Gen-smearing
	nsmears = 3
	if isdata: weight = 1.0*prescaleweight/nsmears    
	else: weight = xsec_times_lumi_over_nevents / nsmears
	for i in range(nsmears):
		if not (gHardMetPt<rebalancedMetCut): break
		smearedJets = smearJets(genjets,9999)
		#smearedJets,csvSmearedJets = smearJets(genjets,matchedCsvVec,_Templates_.ResponseFunctions,_Templates_.hEtaTemplate,_Templates_.hPtTemplate,999)
		mHt = getHt(smearedJets,AnHardMetJetPtCut)
		mSt = mHt
		for obj in acme_objects: mSt+=obj.Pt()
		mHardMetVec = getHardMet(smearedJets,AnHardMetJetPtCut, mhtjetetacut)
		mHardMetVec-=AcmeVector
		mHardMetPt, mHardMetPhi = mHardMetVec.Pt(), mHardMetVec.Phi()
		if mHt>0: mMetSignificance = mHardMetPt/TMath.Sqrt(mHt)
		else: mMetSignificance = 8		
		mNJets = countJets(smearedJets,AnHardMetJetPtCut)
		mBTags = countBJets(smearedJets,AnHardMetJetPtCut)
		redoneMET = redoMET(genMetVec, genjets, smearedJets)
		mMetPt, mMetPhi = redoneMET.Pt(), redoneMET.Phi()
		#mindphi = 4
		#for jet in smearedJets[:4]: mindphi = min(mindphi, abs(jet.DeltaPhi(mHardMetVec)))	
		fv = [mSt,mHardMetPt,mNJets,mBTags,dphi, int(recophotons.size()),mMetSignificance]

		for regionkey in regionCuts:
			for ivar, varname in enumerate(varlist):
				hname = regionkey+'_'+varname
				if selectionFeatureVector(fv,regionkey,varname,''): 
					fillth1(histoStructDict[hname].GenSmeared, fv[ivar],weight)

fnew.cd()
writeHistoStruct(histoStructDict)
hGenMetGenHardMetRatio.Write()
hSt.Write()
hStWeighted.Write()

hPassFit.Write()
hTotFit.Write()
if mktree:
	treefile.cd()
	littletree.Write()
	treefile.Close()
print 'just created', fnew.GetName()
fnew.Close()



