#/usr/bin/env python

import os,sys
from ROOT import *
from string import *


try: model = sys.argv[1] 
except: 
	model = 'T5Wg'
	model = 'T6Wg'

parents = {}
parents['T5Wg'] = 'glu'
parents['T6Wg'] = 'squ'
parents['T2'] = 'squ'
parents['T1'] = 'glu'

    
def getxsec(parent='glu'):
    xsecdict = {} # dict for xsecs
    xsecFile = parent+"_xsecs_13TeV.txt"#"glu_xsecs_13TeV

    with open(xsecFile,"r") as xfile:
        lines = xfile.readlines()
        print 'Found %i lines in %s' %(len(lines),xsecFile)
        for line in lines:
            if line[0] == '#': continue
            (mparent,xsec,err) = line.split()
            xsecdict[int(mparent)] = (float(xsec),float(err))

    return xsecdict


def writeTree(box, model, directory, mg, mchi, xsecULObs, xsecULExpPlus2, xsecULExpPlus, xsecULExp, xsecULExpMinus, xsecULExpMinus2, signif):
    #tmpFileName = "%s/%s_xsecUL_mg_%s_mchi_%s_%s.root" %("/tmp", model, mg, mchi, box)
    outputFileName = "%s/%s_xsecUL_mg_%s_mchi_%s_%s.root" %(directory, model, mg, mchi, box)
    print 'creating file', outputFileName
    fileOut = TFile.Open(outputFileName, "recreate")

    if 1==1:
        xsecTree = TTree("xsecTree", "xsecTree")
        try:
            from ROOT import MyStruct
        except ImportError:
            myStructCmd = "struct MyStruct{Double_t mg;Double_t mchi; Double_t x; Double_t y;"
            ixsecUL = 0
            myStructCmd+= "Double_t xsecUL%i;"%(ixsecUL+0)
            myStructCmd+= "Double_t xsecUL%i;"%(ixsecUL+1)
            myStructCmd+= "Double_t xsecUL%i;"%(ixsecUL+2)
            myStructCmd+= "Double_t xsecUL%i;"%(ixsecUL+3)
            myStructCmd+= "Double_t xsecUL%i;"%(ixsecUL+4)
            myStructCmd+= "Double_t xsecUL%i;"%(ixsecUL+5)
            ixsecUL+=6
            myStructCmd += "}"
            gROOT.ProcessLine(myStructCmd)
            from ROOT import MyStruct
        
        s = MyStruct()
        xsecTree.Branch("mg", AddressOf(s,"mg"),'mg/D')
        xsecTree.Branch("mchi", AddressOf(s,"mchi"),'mchi/D')
        xsecTree.Branch("x", AddressOf(s,"x"),'x/D')
        xsecTree.Branch("y", AddressOf(s,"y"),'y/D')    
    
    s.mg = mg
    s.mchi = mchi
    if 'T1x' in model:
        s.x = float(model[model.find('x')+1:model.find('y')].replace('p','.'))
        s.y = float(model[model.find('y')+1:].replace('p','.'))
    elif model == 'T1bbbb':
        s.x = 1
        s.y = 0
    elif model == 'T1tttt':
        s.x = 0
        s.y = 1
    else:
        s.x = -1
        s.y = -1

    if 1==1:
        ixsecUL = 0
        xsecTree.Branch("xsecULObs_%s"%box, AddressOf(s,"xsecUL%i"%(ixsecUL+0)),'xsecUL%i/D'%(ixsecUL+0))
        xsecTree.Branch("xsecULExpPlus2_%s"%box, AddressOf(s,"xsecUL%i"%(ixsecUL+1)),'xsecUL%i/D'%(ixsecUL+1))
        xsecTree.Branch("xsecULExpPlus_%s"%box, AddressOf(s,"xsecUL%i"%(ixsecUL+2)),'xsecUL%i/D'%(ixsecUL+2))
        xsecTree.Branch("xsecULExp_%s"%box, AddressOf(s,"xsecUL%i"%(ixsecUL+3)),'xsecUL%i/D'%(ixsecUL+3))
        xsecTree.Branch("xsecULExpMinus_%s"%box, AddressOf(s,"xsecUL%i"%(ixsecUL+4)),'xsecUL%i/D'%(ixsecUL+4))
        xsecTree.Branch("xsecULExpMinus2_%s"%box, AddressOf(s,"xsecUL%i"%(ixsecUL+5)),'xsecUL%i/D'%(ixsecUL+5))
        exec 's.xsecUL%i = xsecULObs[ixsecUL]'%(ixsecUL+0)
        exec 's.xsecUL%i = xsecULExpPlus2[ixsecUL]'%(ixsecUL+1)
        exec 's.xsecUL%i = xsecULExpPlus[ixsecUL]'%(ixsecUL+2)
        exec 's.xsecUL%i = xsecULExp[ixsecUL]'%(ixsecUL+3)
        exec 's.xsecUL%i = xsecULExpMinus[ixsecUL]'%(ixsecUL+4)
        exec 's.xsecUL%i = xsecULExpMinus2[ixsecUL]'%(ixsecUL+5)
        ixsecUL += 4
        
        xsecTree.Fill()
        
        fileOut.cd()
        xsecTree.Write()
        
        fileOut.Close()
        
        #outputFileName = "%s/%s_xsecUL_mg_%s_mchi_%s_%s.root" %(directory, model, mg, mchi, box)
        print "INFO: xsec UL values being written to %s"%outputFileName
        
        #special_call(["mv",tmpFileName,outputFileName],0)
        
    return outputFileName

#--------------

# Gt the cross sections
xsecdict = getxsec(parents[model])
box = 'diphoton'

dcdir = 'datacards/'+model+'/'
limitdir = 'limitsroot/'+model+'/'
limit2dir = 'limits2root/'+model+'/'
logdir = 'logfiles/'+model+'/'
if not os.path.exists(limitdir):
    os.system('mkdir '+limitdir)
if not os.path.exists(logdir):
    os.system('mkdir '+logdir)
if not os.path.exists(limit2dir):
    os.system('mkdir '+limit2dir)    

dcs = os.popen('ls '+dcdir+'*.txt').readlines()

# write results to a tree
xsecULObs	= 0.
xsecULExpMinus2 = 0.
xsecULExpMinus  = 0.
xsecULExp	= 0.
xsecULExpPlus   = 0.
xsecULExpPlus2  = 0.
signif          = 0.

for dc in dcs:
    dc = strip(dc)
    fln = replace(split(split(dc, '/')[2], '_RA2')[0], "datacard", "")
    #fln = dc.split('/')[-1]
    
    logfile = logdir+fln+'.log'
    print 'Running:', fln
    cmd = 'combine -M AsymptoticLimits '+dc+' --name '+fln+' >& '+logfile
    print cmd
    os.system(cmd)
    limitfln = limitdir+'higgsCombine'+fln+'.AsymptoticLimits.mH120.root'
    #os.system('mv *'+fln+'*.root '+limitfln)
    print 'grist', limitfln
    print 'gonna try to work with ', limitfln[limitfln.find('_m')+2:limitfln.find('.0d')+2]
    if 'T1' in model: mparent = 'glu', int(limitfln[limitfln.find('_m')+3:limitfln.find('_Chi')])
    elif 'T2' in model: mparent = 'squ', int(limitfln[limitfln.find('Stop')+4:limitfln.find('_Chi')])
    elif 'T6' in model or 'T5' in model: mparent = float(limitfln[limitfln.find('_m')+2:limitfln.find('.0d')+2])        
    #print 'dissecting', limitfln
    mLSP = float(limitfln[limitfln.find('.0d')+3:limitfln.find('.txt.As')])   
    print 'mparent, mchi', mparent, mLSP
    print 'cracking open', logfile
    log = open(logfile).readlines()
    print 'log file was:'
    print log
    print 'going to reference xsec with mparent'
    try: refXsec = xsecdict[int(5*round(float(mparent)/5))][0]
    except:
        print 'couldnt find', int(5*round(float(mparent)/5)), 'in', xsecdict
    print mparent, refXsec
    for line in log:
        if "Observed Limit:" in line:
            xsecULObs = refXsec*float(line.split()[4])
        elif "Expected  2.5%:" in line:
            xsecULExpMinus2 = refXsec*float(line.split()[4])
        elif "Expected 16.0%:" in line:
            xsecULExpMinus = refXsec*float(line.split()[4])
        elif "Expected 50.0%:" in line:
            xsecULExp = refXsec*float(line.split()[4])
        elif "Expected 84.0%:" in line:
            xsecULExpPlus = refXsec*float(line.split()[4])
        elif "Expected 97.5%:" in line:
            xsecULExpPlus2 = refXsec*float(line.split()[4])
        elif "Significance:" in line:
            signif = float(line.split()[1])

    writeTree(box, model, limit2dir, float(mparent), float(mLSP), [xsecULObs], [xsecULExpPlus2], [xsecULExpPlus], [xsecULExp], [xsecULExpMinus], [xsecULExpMinus2], 0)


