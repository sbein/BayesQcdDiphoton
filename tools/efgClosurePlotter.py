
#Welcome to the industrial age of Sam's rebalance and smear code. You're going to have a lot of fun!
import os,sys
from ROOT import *
from array import array
from glob import glob
from utils import *
import numpy as np
import time
gROOT.SetBatch(1)
gStyle.SetOptStat(0)
gStyle.SetTitleFont(100,"t");

'''
python tools/efgClosurePlotter.py

python tools/efgClosurePlotter.py GenMatchTrue
python tools/efgClosurePlotter.py GenMatchFalse

python tools/whiphtml.py "/uscms_data/d3/sbein/Diphoton/18Jan2019/CMSSW_10_1_0/src/SusyDiphoton/pngs/GenMatchTrue/*.png"
python tools/whiphtml.py "/uscms_data/d3/sbein/Diphoton/18Jan2019/CMSSW_10_1_0/src/SusyDiphoton/pngs/GenMatchFalse/*.png"

scp -r pngs/ ${DESY}:/afs/desy.de/user/b/beinsam/www/Diphoton/May2022
'''

try: extra = sys.argv[1]
except: extra = 'GenMatchFalse'


processes = {}
processes['wjets'] = ['W+Jets, W#rightarrow l#nu','efgoutput/efg-Summer16v3.WJetsToLNu_'+extra+'.root']
processes['ttjets'] = ['t#bar{t}+jets', 'efgoutput/efg-Summer16v3.TTJets_'+extra+'.root']
processes['dyjets'] = ['jets+Z#rightarrowLL', 'efgoutput/efg-Summer16v3.DYJetsToLL_M-50_'+extra+'.root']



if not os.path.exists('pngs/'+extra): os.system('mkdir -p pngs/'+extra)


fnew = TFile('efgplots_Summer2016_'+extra+'.root','recreate')

for pkey in processes:
	label, fname = processes[pkey]
	f = TFile(fname)
	keys = f.GetListOfKeys()
	f.ls()
	for key in keys:
		name = key.GetName()
		if not ('PhoMatched' in name or 'Truth' in name): continue

		hGenElePhoMatched = f.Get(name);hGenElePhoMatched.Rebin()
		hGenElePhoMatched.SetTitle('genE-matched recPho'); 
		if 'PhoMatched' in name: altname = name.replace('Pho','Ele')+'_weighted'
		else: altname = name.replace('Truth','Method')
		print 'grasping', altname
		hGenEleEleMatched_weighted = f.Get(altname); hGenEleEleMatched_weighted.Rebin()
		hGenEleEleMatched_weighted.SetTitle('weighted genE-matched recE'); #hGenEleEleMatched_weighted.Rebin()
		histoStyler(hGenEleEleMatched_weighted, kGreen+2)

		c1 = mkcanvas('c_'+pkey+'_'+name)
		hTf = hGenEleEleMatched_weighted.Clone()

		leg = mklegend(0.5, 0.55, 0.9, 0.8)
		hratio, hmethodsyst = FabDraw(c1,leg,hGenElePhoMatched,[hGenEleEleMatched_weighted],datamc='MC',lumi='n/a', title = 'testing', LinearScale=False, fractionthing='rec-pho / rec-el')
		hratio.SetLineColor(kBlack)
		hratio.SetMarkerColor(kBlack)
		hratio.GetXaxis().SetTitle('')
		pad1, pad2 = hmethodsyst[-2:]
		pad1.SetGridx()
		pad1.SetGridy()
		pad2.SetGridx(1)
		pad2.SetGridy(1)
		pad2.cd()
		#hratio.GetYaxis().SetRangeUser(0,0.05)
		#hratio.GetYaxis().SetNdivisions(5)
		hratio.GetXaxis().SetTitle(name[1:].replace('Truth',''))
		#hratio.Draw('hist text')
		pad2.Update()
		#hGenEleEleMatched_weighted.GetYaxis().SetRangeUser(0.1,1000000000)
		#hGenEleEleMatched_weighted.GetYaxis().SetTitle('entries/bin')
		#pad1.cd()
		#tl.DrawLatex(0.73, 0.5, label+', '+ centrality)
		#c1.Update()
		#pause()
		fnew.cd()
		c1.Write('c_'+pkey+'_'+name.replace('Truth',''))
		c1.Print('pngs/'+extra+'/closure'+pkey+'_'+name+'.png')
	f.Close()
	
print 'just created', fnew.GetName()
fnew.Close()
