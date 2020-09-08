#this module should work just like hadd
from ROOT import *
import glob, os, sys
import numpy as np
from utils import *

istest = False
try: folder = sys.argv[1]
except:
    print 'please give folder name as first argument'
    exit(0)
    
keywords = [\
            'GJets_DR-0p4_HT-100To200', \
            'GJets_DR-0p4_HT-200To400', \
            'GJets_DR-0p4_HT-400To600', \
            'GJets_DR-0p4_HT-600ToInf'
            ]

for keyword in keywords:
    command = 'python tools/ahadd.py -f unwghtd'+keyword+'.root '+folder+'/posterior*'+keyword+'*.root'
    print command
    if not istest: os.system(command)    
    fuw = TFile('unwghtd'+keyword+'.root')
    fw = TFile('wghtd'+keyword+'.root', 'recreate')
    hHt = fuw.Get('hHt')
    nentries = hHt.GetEntries()
    keys = fuw.GetListOfKeys()
    for key in keys:
        name = key.GetName()
        if not len(name.split('/'))>0: continue
        hist = fuw.Get(name)
        hist.Scale(1.0/nentries)
        fw.cd()
        hist.Write()
    fuw.Close()
    command = 'rm unwghtd'+keyword+'.root'
    print command
    if not istest: os.system(command)
    fw.Close()

command = 'hadd -f '+keywords[0].split('_')[0]+ '.root wghtd'+keywords[0].split('_')[0]+'_*'
print command
if not istest: os.system(command)

command = 'rm wghtd'+keywords[0].split('_')[0]+'_*'
print command
if not istest: os.system(command)
