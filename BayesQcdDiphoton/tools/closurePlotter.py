from ROOT import *
from utils import *
import os,sys
gROOT.SetBatch(1)


year = '2016'
linscale = False

try: filenameA = sys.argv[1]
except: filenameA = 'Vault/QCD_Summer16.root'

redoBinning = binningUser
redoBinning = {}

gStyle.SetOptStat(0)
gROOT.ForceStyle()

lumi = 35.9

fileA = TFile(filenameA)
fileA.ls()
keys = fileA.GetListOfKeys()
keys = sorted(keys,key=lambda thing: thing.GetName())
namestem = filenameA.split('/')[-1].replace('.root','').replace('posterior-','')
newfile = TFile('closure_rands'+namestem+'.root','recreate')
norm = 1.0

for key in keys:
    name = key.GetName()
    if not name[0]=='h': continue
    if not 'obs' in name: continue
    hObserved = fileA.Get(name)
    if datamc=='mc': hObserved.Scale(1000*lumi)
    print 'processing', name
    hObserved.SetTitle('Summer16 GJets')

    histoStyler(hObserved, 1)
    hpred = fileA.Get(name.replace('obs','rands'))
    hpred.SetTitle('R&S prediction (Summer16)')
    
    hObserved.Scale(1000*lumi)  
    hpred.Scale(1000*lumi)                
        
    histoStyler(hpred, kBlue-7)     
    hpred.SetFillColor(hpred.GetLineColor())

    hpreds = []
    hpreds.append(hpred)    
    
    if 'mva' in name: kinvar = '_'.join(name.split('_')[1:]).replace('_obs','')
    else: kinvar = name.split('_')[1]
    
    print 'found kinvar', kinvar, 'from', name
    cGold = TCanvas('cEnchilada','cEnchilada', 800, 800)
    if kinvar in redoBinning.keys():
        if len(redoBinning[kinvar])>3: ##this should be reinstated
            nbins = len(redoBinning[kinvar])-1
            newxs = array('d',redoBinning[kinvar])
        else:
            newbinning = []
            stepsize = round(1.0*(redoBinning[kinvar][2]-redoBinning[kinvar][1])/redoBinning[kinvar][0],4)
            for ibin in range(redoBinning[kinvar][0]+1): newbinning.append(redoBinning[kinvar][1]+ibin*stepsize)
            nbins = len(newbinning)-1
            newxs = array('d',newbinning)


        hObserved = hObserved.Rebin(nbins,'',newxs)
        for ih in range(len(hpreds)):  hpreds[ih] = hpreds[ih].Rebin(nbins,'',newxs)

    if not linscale: hObserved.GetYaxis().SetRangeUser(max(0.0001,min(0.01, 0.01*hObserved.GetMinimum())),max(700000, 10*hObserved.GetMaximum()))

    oldalign = tl.GetTextAlign()    
    tl.SetTextAlign(oldalign)
    leg = mklegend(x1=.4, y1=.58, x2=.92, y2=.8, color=kWhite)
    hratio, hmethodsyst = FabDrawSystyRatio(cGold,leg,hObserved,hpreds,datamc=datamc,lumi=str(lumi), title = '',LinearScale=linscale,fractionthing='observed/method')

    
    for ih in range(len(hpreds)): 
        if linscale:            
            hpreds[ih].GetYaxis().SetRangeUser(0.0,80)
        else:
            hpreds[ih].GetYaxis().SetRangeUser(0.04,500)
        
    hratio.GetYaxis().SetRangeUser(-0.2,2.2)
    hratio.GetXaxis().SetTitle(kinvar.replace('mva_','(for MVA) '))
    cname = 'c_'+name[1:]
    newfile.cd()
    cGold.Write(cname)
    #print 'trying:','pdfs/ClosureTests/'+selection+'_'+method+'And'+standard+'_'+kinvar+'.pdf'
    cGold.Print('pdfs/Closure/'+year+cname[1:]+'.pdf')


print 'just created', newfile.GetName()
