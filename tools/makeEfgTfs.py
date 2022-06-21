
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
python tools/makeElectronFakingPhotonHists.py --fnamekeyword Summer16v3.WJetsToLNu_TuneCUETP8M1 --quickrun True
#ls /eos/uscms/store/group/lpcsusyPhotons/TreeMaker/Summer16v3.*
eosls /store/group/lpcsusyPhotons/TreeMaker/ |grep Summer16
'''

fname =  'efg-Summer16v3.WJetsToLNu_TuneCUETP8M1_part1.root'
fname = 'efg-Summer16v3.TTJets_Tune_part1.root'

processes = {}
processes['wjets'] = ['W+Jets, W#rightarrow l#nu','efgoutput/efg-Summer16v3.WJetsToLNu.root']
processes['ttjets'] = ['t#bar{t}+jets', 'efgoutput/efg-Summer16v3.TTJets.root']
processes['dyjets'] = ['jets+Z#rightarrowLL', 'efgoutput/efg-Summer16v3.DYJetsToLL_M-50.root']




fnew = TFile('efg_Summer2016.root','recreate')

for key in processes:
	label, fname = processes[key]
	f = TFile(fname)
	f.ls()
	for centrality in ['Barrel','Endcap']:

		hGenElPtPhoMatched = f.Get('hGenElPtPhoMatched_'+centrality); hGenElPtPhoMatched.Rebin()
		hGenElPtPhoMatched.SetTitle('gen-ele-matched rec-pho'); hGenElPtPhoMatched.Rebin()
		hGenElPtEleMatched = f.Get('hGenElPtEleMatched_'+centrality); hGenElPtEleMatched.Rebin()
		hGenElPtEleMatched.SetTitle('gen-ele-matched rec-ele'); hGenElPtEleMatched.Rebin()
		histoStyler(hGenElPtEleMatched, kGreen+2)

		c1 = mkcanvas('c_'+key+'_'+centrality)
		hTf = hGenElPtEleMatched.Clone()

		leg = mklegend(0.5, 0.55, 0.9, 0.8)
		hratio, hmethodsyst = FabDraw(c1,leg,hGenElPtPhoMatched,[hGenElPtEleMatched],datamc='MC',lumi='n/a', title = 'testing', LinearScale=False, fractionthing='rec-pho / rec-el')
		hratio.SetLineColor(kBlack)
		hratio.SetMarkerColor(kBlack)
		hratio.GetXaxis().SetTitle('')
		pad1, pad2 = hmethodsyst[-2:]
		pad1.SetGridx()
		pad1.SetGridy()
		pad2.SetGridx(1)
		pad2.SetGridy(1)
		pad2.cd()
		hratio.GetYaxis().SetRangeUser(0,0.05)
		hratio.GetYaxis().SetNdivisions(5)
		hratio.GetXaxis().SetTitle('generator electron p_{T} [GeV]')
		#hratio.Draw('hist text')
		pad2.Update()
		hGenElPtEleMatched.GetYaxis().SetRangeUser(0.1,1000000000)
		hGenElPtEleMatched.GetYaxis().SetTitle('entries/bin')
		pad1.cd()
		tl.DrawLatex(0.73, 0.5, label+', '+ centrality)
		c1.Update()
		#pause()
		fnew.cd()
		hratio.Write('htf_'+key+'_'+centrality)
		c1.Write('c_'+key+'_'+centrality)
		c1.Print('pngs/'+key+'_'+centrality+'.png')
	f.Close()
	
print 'just created', fnew.GetName()
fnew.Close()
