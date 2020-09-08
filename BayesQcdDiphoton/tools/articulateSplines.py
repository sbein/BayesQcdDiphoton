#this module should work just like hadd
from ROOT import *
import glob, os, sys
import numpy as np
from utils import *


try: newfile = sys.argv[1]
except: newfile = 'newtemplates.root'
try: bunchofiles = sys.argv[2]
except: bunchofiles = 'xx.root'

print 'hadd '+newfile+' '+bunchofiles

if len(newfile.split('/'))>1 or len(sys.argv)<3: 
    print 'dangerous to feed in that argument or missing target argument'
    exit(0)

os.system('rm '+newfile)
os.system('python tools/ahadd.py '+newfile+' '+bunchofiles)

f = TFile(newfile,'update')
keys = f.GetListOfKeys()
dir_ = f.mkdir('splines')
dir_.cd()
nsmooth = 5
for key in keys:
    name = key.GetName()
    if not ('hRTemplate(gPt' in name or 'hGenHardMet' in name or 'Significance' in name): continue
    print 'name'
    h = f.Get(name)
    print 'name=',name
    try: h.Scale(1.0/h.Integral(-1,9999),'width')
    except: pass
    h.Smooth(nsmooth)
    g = TGraph(h)
    s3 = TSpline3("s3",g.GetX(),g.GetY(),g.GetN())
    lowerbound = 0
    upperbound = 3.0
    if 'hRTemplate(gPt' in name and int(name[name.find('gPt')+3:name.find('.')])<17: upperbound = 4.0
    #if 'hRTemplate(gPt' in name and int(name[name.find('gPt')+3:name.find('.')])<30: upperbound = 4.5        
    if 'GenHardMetPhi' in name: 
        upperbound = 3.142
        lowerbound = -3.142
    if 'GenHardMetPt' in name: 
        upperbound = 800.0#1.0
    def splineFunc(x,p):
        return s3.Eval(x[0])
    func = TF1('func',splineFunc,lowerbound,upperbound,1)
    func.SetNpx(10000)
    if 'Pt' in name:
        a = 1
        #h.Draw('hist')
        #c1.SetLogy()
        #func.Draw('same')
        #c1.Update()
        #pause()
    g.Write(name+'_graph')
    #func.Write(name+'_spline')
print 'just created', f.GetName()
f.Close()
    
