#!/usr/bin/env python

import os,sys
from ROOT import *
from string import *

# Physics processes
# !!! Maybe already match here the process names and histograms
procs = [
	'Signal',
	'Prompt',
	'Fake'
	]

#maindir = '/nfs/dust/cms/user/beinsam/LongLiveTheChi/Analyzer/CMSSW_10_1_0/src/analysis/interpretation/HistsBkgObsSig/TheWholeEnchilada/'
#maindir = '/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Piano/'

maindir = '/afs/desy.de/user/k/kutznerv/dust/public/disapptrk/interpretation/Histograms/Antimony/v1/'

fb = TFile(maindir+'Background/prediction137-mc.root')
#ffk = TFile(maindir+'Background/fake-bg-results-new-sideband.root')
#fo = TFile(maindir+'Background/prompt-bg-results.root')

# Get all bg histograms
#hprompt = fb.Get('hElBaselineZone3p4To6p0_BinNumberMethod')
hprompt = fb.Get('hPromptBaseline_BinNumberMethod')
hprompt.SetName('Prompt')
#hmu = fb.Get('hMuBaselineZone3p4To6p0_BinNumberMethod')
hfk = fb.Get('hFakeBaseline_BinNumberTruth')
hfk.SetName('Fake')
hobs = hprompt.Clone()
hobs.SetName('data_obs')
hobs.Add(hfk)

#signalname = sys.argv[1] 
#print 'Signal: '+signalname
signalname = 'T2btLL'
#signalname = 'T1qqqqLL'

signaldir = maindir+'Signal/'+signalname+'/*.root'
signalfiles = os.popen('ls '+signaldir).readlines()

outrootdir = 'sigbgobsroot/'+signalname+'/'
outdcdir = 'datacards/'+signalname+'/'

if not os.path.exists(outrootdir):
	os.system('mkdir '+outrootdir)

if not os.path.exists(outdcdir):
	os.system('mkdir '+outdcdir)

# DATACARD CONTENT

# Write the datacard beginning lines
cnt = '''imax 1 number of channels
jmax %s number of backgrounds
kmax * number of nuisance parameters
------------------------------------------------------------
observation     %s
------------------------------------------------------------
shapes * * %s $PROCESS $PROCESS_$SYSTEMATIC
------------------------------------------------------------
'''
# Number of background processes
nbg = str(len(procs) - 1)

for f in signalfiles:
	f = strip(f)
	signalhistofile = f
	signalname = ((f.split('/'))[-1])[:-5]
	frn = replace(signalname, "AnalysisHists", "limitinput") + '.root'
	fdn = replace(signalname, "AnalysisHists", "datacard") + '.txt'
	fs = TFile(signalhistofile)
	if signalname == 'T1qqqqLL' and '1075' in signalhistofile: continue
	print '*** Signal file:', signalhistofile
	# Get signal histograms
	hsig = fs.Get('hBaseline_BinNumberTruth')
	#hsig.Scale(35900.)
	hsig.SetName('Signal')
	# Make the output file
	fr = TFile(outrootdir+'/'+frn, 'RECREATE') 
	# Write histograms to the output file
	hsig.Write()
	hprompt.Write()
	hfk.Write()
	hobs.Write()
	#    sys.exit()
	fd = open(outdcdir+'/'+fdn, 'w')
	# Number of data events
	ndata = str(hobs.Integral())
	# Write the datacard header
	print nbg, ndata, frn
	fd.write(cnt % (nbg, ndata, outrootdir+frn))
	# Yields for processes
	yields = []
	for p in procs:
		yields.append(gDirectory.Get(p).Integral())
	print 'yields:', yields

	# Write processes and rates
	row = '%-15s ' % 'bin'
	for i in procs:
		row = row+'%-9s ' % 'DT'
	fd.write(row+'\n')
	row = '%-15s ' % 'process'
	for i in procs:
		row = row+'%-9s ' % i
	fd.write(row+'\n')
	row = '%-15s ' % 'process'
	for i in range(len(procs)):
		row = row+'%-9i ' % i
	fd.write(row+'\n')
	row = '%-15s ' % 'rate'
	for y in yields:
		row = row+'%9.3f ' % y
	fd.write(row+'\n')

	# Add random systematics
	cnt2 = ''''------------------------------------------------------------
	Lumi     lnN    1.025     1.025     1.025     1.025     1.025
	jes      lnN    0.98/1.03 -         -         -         -
	btag     lnN    1.02      -         -         -         -
	'''
#    Closure  shape  -         1.0       1.0       1.0


	fd.write(cnt2)

	print 'just wrote', fd
	fd.close()



