#!/usr/bin/env python

import os,sys
from ROOT import *
from string import *

#execfile(os.environ['CMSSW_BASE']+'/src/BayesQcdDiphoton/tools/utils.py')
execfile('/uscms_data/d3/sbein/Diphoton/18Jan2019/CMSSW_10_1_0/src/BayesQcdDiphoton/tools/utils.py')

#/eos/uscms//store/group/lpcsusyphotons/hists_22June2021/ElectronBkgEst.root
#BinDivMET
#/eos/uscms//store/group/lpcsusyphotons/hists_22June2021/ZGGToNuNuGG_2016_hbdttwopsv.root
#hpred_mva_HardMET

lumi = 35.9
lumiscale = 1# 137./lumi

redoBinning = {}
redoBinning['HardMet'] = [130,150,185,250,500]


# Physics processes
# !!! Maybe already match here the process names and histograms
procs = [
    'Signal',
    'WJets',
    'ZGG',
    'FakeMet'
    ]

#fb = TFile('../BayesQcdDiphoton/plots_2016_data_phopho.root')
fb = TFile('../BayesQcdDiphoton/master.root')
#fb = TFile('../BayesQcdDiphoton/master_snuffmidlow.root')
#fb = TFile('../BayesQcdDiphoton/master_poolTheCats.root')
keys = fb.GetListOfKeys()
fb.ls()

datamc = 'data'

# Get all bg histograms
#hfakemet = fb.Get('hElBaselineZone3p4To6p0_BinNumberMethod')
hfakemet = fb.Get('R&S prediction')
hfakemet.SetName('FakeMet')
hfakemet.Scale(lumiscale)

#hwjets = fb.Get('Summer16v3.WGJets_MonoPhoton')
hwjets = fb.Get('e faking #gamma')
hwjets.SetName('WJets')
hwjets.Scale(lumiscale)

#hzgg = fb.Get('Summer16v3.ZGGToNuNuGG')
hzgg = fb.Get('#gamma#gamma Z,Z#rightarrow#nu#bar{#nu}')
hzgg.SetName('ZGG')
hzgg.Scale(lumiscale)


hobs = hfakemet.Clone('data_obs')
hobs.Add(hwjets)
hobs.Add(hzgg)
hobs.Scale(lumiscale)

try: model = sys.argv[1] 
except: 
	model = 'T5Wg'
	model = 'T6Wg'

#signaldir = '../BayesQcdDiphoton/output/signals/*Summer16v3Fast.SMS-'+model+'*.root'
#signalfiles = os.popen('ls '+signaldir).readlines()

outrootdir = 'sigbgobsroot/'+model+'/'
outdcdir = 'datacards/'+model+'/'

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

#for f in signalfiles:
for key in keys:
    name = key.GetName()
    if not model in name: continue
    #f = strip(f)
    #signalhistofile = f
    #model = ((f.split('/'))[-1])[:-5]


    frn = replace(name, "AnalysisHists", "limitinput") + '.root'
    fdn = replace(name, "AnalysisHists", "datacard") + '.txt'
    # Get signal histograms

    hsig = fb.Get(name)

    kinvar = 'HardMet'
    print 'redoing the binning', kinvar
    if len(redoBinning[kinvar])>3: ##this should be reinstated
            nbins = len(redoBinning[kinvar])-1
            print 'make sure', kinvar, 'is a key in'
            print redoBinning
            newxs = array('d',redoBinning[kinvar])
    else:
            newbinning = []
            stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
            for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
            nbins = len(newbinning)-1
            newxs = array('d',newbinning)


            
    #hsig = hsig.Rebin(nbins,'',newxs)
    hsig.SetDirectory(0)

        
    
    #hsig.Scale(1000*lumi)
    hsig.Scale(4.0)##########################################for BR
    hsig.Scale(lumiscale)

    #hsig.Scale(35900.)
    hsig.SetName('Signal')
    # Make the output file
    fr = TFile(outrootdir+'/'+frn, 'RECREATE') 
    print 'creating root file', fr.GetName()
    # Write histograms to the output file
    hsig.Write()
    hfakemet.Write()
    hwjets.Write()	
    hzgg.Write()
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
    '''
    bin             DT        DT        DT        DT        
    process         Signal    WJets     ZGG       FakeMet   
    process         0         1         2         3
    '''
    # Add random systematics
    cnt2 = ''''------------------------------------------------------------
    Lumi     lnN    1.025     1.025     1.025     1.025     1.025
    jes      lnN    0.98/1.03 -         -         -         -
    btag     lnN    1.02      -         -         -         -
    efakeg   lnN    -         1.1         -         -         -
    '''
#    Closure  shape  -         1.0       1.0       1.0


    fd.write(cnt2)

    print 'just wrote', fd
    fd.close()




