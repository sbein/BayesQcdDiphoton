from ROOT import *
from utils import *
import os, sys
from glob import glob


defaultInfile_ = "../SampleProduction/delphes/delphes_nolhe1.root"
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=int, default=1,help="analyzer script to batch")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultInfile_,help="file")
args = parser.parse_args()
inputFileNames = args.fnamekeyword
inputFiles = glob(inputFileNames)
verbosity = args.verbosity


gSystem.Load("/nfs/dust/cms/user/beinsam/RebalanceAndSmear/CMSSW_10_1_0/src/SampleProduction/delphes/build/libDelphes")


c = TChain('Delphes')
for fname in inputFiles: c.Add(fname)
	
c.Show(0)
treeReader = ExRootTreeReader(c)
numberOfEntries = treeReader.GetEntries()
branchJets = treeReader.UseBranch("Jet")
branchHT = treeReader.UseBranch("ScalarHT")

nentries = c.GetEntries()
print 'n(entries) =', nentries



hHt       = makeTh1("hHt","HT for number of events", 250,0,5000)
hMht       = makeTh1("hMht","hMht", 25,0,250)

for ientry in range(nentries):
	if ientry%verbosity==0: print 'now processing event number', ientry, 'of', nentries
	c.GetEntry(ientry) 	
	treeReader.ReadEntry(ientry)
	scalarht = branchHT[0].HT
	print 'filling with', scalarht
		
	#fillth1(hHt, getattr(c, 'ScalarHT.HT'))	
	if ientry>3: break
	
newname = 'hists.root'
fnew = TFile(newname, 'recreate')
hHt.Write()
print 'just created', newname
fnew.Close()
