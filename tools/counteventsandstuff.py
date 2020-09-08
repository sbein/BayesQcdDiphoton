from ROOT import *
from utils import *
from ROOT import *


chain = TChain("TreeMaker2/PreSelection")

'''
chain.Add('/eos/uscms//store/group/lpcsusyphotons/TreeMaker/2016/ZGGtonunuGG/*.root')
print "chain.GetEntries()", chain.GetEntries()
chain.Draw("MHT","MHT>80 && Photons[1].Pt()>75 && Photons_fullID[0]==1 && Photons_fullID[1]==1")


chain.Add('/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.ZGG*.root')
chain.Draw("HardMETPt","HardMETPt>90 && IsRandS==0")
print "chain.GetEntries()", chain.GetEntries()

'''

chain.Add('/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.GJets*.root')
chain.Draw("HardMETPt","HardMETPt>90 && IsRandS==1")
print "chain.GetEntries()", chain.GetEntries()

c1.Update()
pause()
