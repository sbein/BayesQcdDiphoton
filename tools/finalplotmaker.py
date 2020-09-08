from ROOT import *
from utils import *
import os,sys
gROOT.SetBatch(1)

datamc = 'data'

#datamc = 'mc'

mcsources = {}
mcsources['QCD']         = ['output/bigchunks/Summer16v3.QCD.root']
if datamc=='data':
    mcsources['ZGGToNuNuGG'] = ['output/bigchunks/Summer16v3.ZGGToNuNuGG.root']
    mcsources['WGJets'] = ['output/bigchunks/Summer16v3.WGJets_MonoPhoton.root']

doblinding = True


try: year = sys.argv[1]
except:
    year = '2017'
    year = '2016'


datasource = 'output/mediumchunks/weightedHists_Run2016C-17Jul2018-v1.SinglePhoton_YesAcme.root'
datasource = 'output/mediumchunks/weightedHists_Run2016B-17Jul2018_ver2-v1.SinglePhoton_YesAcme.root'
datasource = 'output/mediumchunks/weightedHists_Run2018AEGamma_YesAcme.root'###need to check it out
datasource = 'output/mediumchunks/weightedHists_Run2018DEGamma_YesAcme.root'###need to check it out
datasource = 'output/mediumchunks/weightedHists_Run2018CEGamma_YesAcme.root'###need to check it out



if year=='2016':
    lumi = 35.9 # 2016 
    #lumi = 2.57
    #lumi = 5.746 # B    
    datasource = 'output/bigchunks/Run2016_Photon.root'
    datasource = 'output/bigchunks/Run2016_DoubleEG.root'
if year=='2017':
    datasource = 'output/bigchunks/Run2017_Photon.root'
    lumi = 41.52

if year=='2018A':
	lumi = 13.95
if year=='2018D':
	lumi = 31.74
if year=='2018C':
	lumi = 6.89

if datamc=='mc':
    datasource = 'output/bigchunks/Summer16v3.QCD.root'
    doblinding = False
    
fdata = TFile(datasource)
fdata.ls()
keys = fdata.GetListOfKeys()
keys = sorted(keys,key=lambda thing: thing.GetName())

redoBinning = {}#binningUser
#redoBinning['Pho1Pt'] = [25,50,550]
#redoBinning['Pho2Pt'] = [25,50,550]
#redoBinning['HardMet'] = [20,120,520]
#redoBinning['mva_BDT'] = [12,-1.1,1.1]

linscale = False

gStyle.SetOptStat(0)
gROOT.ForceStyle()
colors = [2,4, kTeal-5, kYellow+2, kOrange+1, kGreen-2, kGreen-1, kGreen, kGreen+1, kGreen+2]
colors = [kTeal-5, kGreen+2,kOrange+1]
from random import shuffle
#shuffle(colors)

newfile = TFile('plots_'+year+'_'+datamc+'.root','recreate')

userands = True


for key in keys:
    name = key.GetName()
    if not name[0]=='h': continue
    if not 'obs' in name: continue
    hObserved = fdata.Get(name)
    if datamc=='mc': hObserved.Scale(1000*lumi)
    print 'processing', name
    hObserved.SetTitle('Data ('+year+')')
    histoStyler(hObserved, 1)
    hpreds = []
    fkeys = mcsources.keys()
    #fkeys.reverse()
    for ifname, fkey in enumerate(fkeys):
        fnamemc = mcsources[fkey][0]
        if 'QCD' in fnamemc:
            print 'part 1'            
            if userands: 
                #hpred = fpred.Get(name.replace('obs','rands'))
                hpred = fdata.Get(name.replace('obs','rands'))
                hpred.SetTitle('R&S prediction ('+year+')')
                print 'jamming', name.replace('obs','rands'), 'from', fdata.GetName(), 'into the list'
                
                
            else:  
                fnamemc = mcsources[fkey][0]
                fpred = TFile(fnamemc)                            
                fnamemc = mcsources[fkey][0]
                fpred = TFile(fnamemc)                   
                hpred = fpred.Get(name)                            
                hpred.SetTitle(fnamemc.split('/')[-1].replace('.root',''))
            
            print 'getting from data file', name.replace('obs','rands')
            
        else:
            fnamemc = mcsources[fkey][0]
            fpred = TFile(fnamemc)
            print 'trying to get', name, 'from', fpred.GetName()
            hpred = fpred.Get(name)
            hpred.SetTitle(fnamemc.split('/')[-1].replace('.root',''))
        
        if 'QCD' in fnamemc and (userands): 
            if datamc=='data': hpred.Scale(1)
            if datamc=='mc': hpred.Scale(1000*lumi)                
        else: hpred.Scale(1000*lumi)
        hpred.SetDirectory(0)
        
        histoStyler(hpred, colors[ifname])     
        hpred.SetFillColor(hpred.GetLineColor())
        hpreds.append(hpred)   
        hpreds[-1].SetDirectory(0)        
        fpred.Close()
    if 'mva' in name: kinvar = '_'.join(name.split('_')[1:]).replace('_obs','')
    elif 'hadTowOverEM' in name: kinvar = 'hadTowOverEM'
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

    if doblinding:
        if (kinvar=='MinDPhiHardMetJets' or kinvar=='mva_min_dPhi') and not 'LowBDT' in name:
            xax = hObserved.GetXaxis()
            for ibin in range(1,xax.GetNbins()+1):
                if hObserved.GetBinLowEdge(ibin)>0.5: hObserved.SetBinContent(ibin, -99)
        if kinvar=='xHardMet':
            xax = hObserved.GetXaxis()
            for ibin in range(1,xax.GetNbins()+1):
                if hObserved.GetBinLowEdge(ibin)>199: hObserved.SetBinContent(ibin, -99)

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
    print 'setting', kinvar, 'title to', kinvar.replace('mva_','(for MVA) ')
    hratio.GetXaxis().SetTitle(kinvar.replace('mva_','(for MVA) '))
    cname = 'c_'+name[1:]
    newfile.cd()
    cGold.Write(cname)
    #print 'trying:','pdfs/ClosureTests/'+selection+'_'+method+'And'+standard+'_'+kinvar+'.pdf'
    cGold.Print('pdfs/Validation/'+datasource.split('/')[-1].replace('.root','')+cname[1:]+'.pdf')


print 'just created', newfile.GetName()






exit(0)




















