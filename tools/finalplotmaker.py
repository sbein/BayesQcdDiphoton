from ROOT import *
from utils import *
import os,sys
gROOT.SetBatch(1)

datamc = 'data'

dolimitinputs = False

#datamc = 'mc'

os.system('rm pdfs/Validation/*.png')

version = 'mumu'
version = 'badphopho'
#version = 'phopho'
version = 'elel'


if version == 'mumu': chunk = 'bigchunks/bigmus'
if version == 'elel': chunk = 'bigchunks/bigels'    
if version == 'badphopho': chunk = 'bigchunks/bigbadpho'
if version == 'phopho': chunk = 'bigchunks/bigphotons'

prediction_sources = {}
if 'pho' in version: prediction_sources['FakeMet']         = 'output/'+chunk+'/Summer16v3.GJets.root'
else: prediction_sources['FakeMet']         = 'output/'+chunk+'/Summer16v3.DYJetsNoTau.root'
if datamc=='data':
    prediction_sources['#gamma#gamma+Z#rightarrow#nu#bar{#nu}'] = 'output/'+chunk+'/Summer16v3.ZGGToNuNuGG.root'
    prediction_sources['W#gamma+jets'] = 'output/'+chunk+'/Summer16v3.WGJets_MonoPhoton.root'
    prediction_sources['t#bar{t}+jets'] = 'output/'+chunk+'/Summer16v3.TTJets.root'
    prediction_sources['VV'] = 'output/'+chunk+'/Summer16v3.Diboson.root'    
    prediction_sources['W+jets'] = 'output/'+chunk+'/Summer16v3.WJetsToLNu.root'
    prediction_sources['Z^{*}#rightarrow#tau#bar{#tau}'] = 'output/'+chunk+'/Summer16v3.DYJetsWithTau.root'
    prediction_sources['t#bar{t}Z'] = 'output/'+chunk+'/Summer16v3.TTZ.root'
    
   

colors = [2,4, kTeal-5, kYellow+2, kOrange+1, kGreen-2, kGreen-1, kGreen, kGreen+1, kGreen+2]
if version=='elel' or version=='mumu':
    fkeys = [['Z^{*}#rightarrow#tau#bar{#tau}',kViolet],['t#bar{t}Z',kBlack],['VV',kRed+1],['t#bar{t}+jets',kTeal-5],['FakeMet',kOrange+1]]#,['WJets',kYellow+1]
if 'phopho' in version:
    fkeys = [['W#gamma+jets',kYellow+1],['Z^{*}#rightarrow#tau#bar{#tau}',kViolet],['#gamma#gamma+Z#rightarrow#nu#bar{#nu}',kViolet+2],['VV',kRed+1],['t#bar{t}+jets',kTeal-5],['FakeMet',kOrange+1]]#,['WJets',kYellow+1]


doblinding = False
blindall = False
userands = True

try: year = sys.argv[1]
except:
    year = '2017'
    year = '2016'


signals = ['output/signals/weightedHists_posterior-Summer16v3Fast.SMS-T5Wg_m1800.0d1650.0_RA2AnalysisTree_YesAcme.root',
           'output/signals/weightedHists_posterior-Summer16v3Fast.SMS-T6Wg_m1800.0d1000.0_RA2AnalysisTree_YesAcme.root',
           'output/signals/weightedHists_posterior-Summer16v3Fast.SMS-T6Wg_m1800.0d50.0_RA2AnalysisTree_YesAcme.root']
signals = []
sigcolors = [kBlue+1, kRed+1, kGray+1, kMagenta, kTeal-5]

if year=='2016':
    lumi = 35.9 # 2016 
    #lumi = 2.57 #lumi = 5.746 # B    
    if version=='mumu': datasource = 'output/'+chunk+'/Run2016_SingleMu.root'
    if version=='elel': datasource = 'output/'+chunk+'/Run2016_DoubleEG.root'
    if 'phopho' in version: datasource = 'output/'+chunk+'/Run2016_DoubleEG.root'
if year=='2017':
    datasource = 'output/'+chunk+'/Run2017_Photon.root'
    datasource = 'output/'+chunk+'/Run2017_DoubleEG.root'
    lumi = 41.52

if year=='2018':
    datasource = 'output/'+chunk+'/Run2018_DoubleEG.root'
    lumi = 54.52

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

redoBinning = {}

linscale = False

gStyle.SetOptStat(0)
gROOT.ForceStyle()

from random import shuffle
#shuffle(colors)

newfile = TFile('plots_'+year+'_'+datamc+'_'+version+'.root','recreate')



for key in keys:
    name = key.GetName()
    if 'Vs' in name: continue
    if not name[0]=='h': continue
    if not 'obs' in name: continue
    hObserved = fdata.Get(name)
    if datamc=='mc': hObserved.Scale(1000*lumi)
    print 'processing', name
    hObserved.SetTitle('Data ('+year+')')
    histoStyler(hObserved, 1)
    hpreds = []
    #fkeys.reverse()
    for fkey, color in fkeys:
        fname_pred = prediction_sources[fkey]
        print 'fkey', fkey
        if 'FakeMet' in fkey:          
            if userands: 
                #hpred = fpred.Get(name.replace('obs','rands'))
                fpred = TFile()
                hpred = fdata.Get(name.replace('obs','rands'))
                hpred.SetTitle('R&S prediction')
                hpred.Scale(1.16)

                ftt = TFile(prediction_sources['t#bar{t}+jets'])
                htt = ftt.Get(name.replace('obs','rands'))
                htt.Scale(1000*lumi)
                if version == 'mumu': htt.Scale(0.75)
                hpred.Add(htt,-1)
                ftt.Close()

                print 'jamming', name.replace('obs','rands'), 'from', fdata.GetName(), 'into the list'
                #fdata.ls()
                #exit(0)
            else:  
                fpred = TFile(fname_pred)
                hpred = fpred.Get(name)                            
                hpred.SetTitle('DY#rightarrow ee/#mu#mu, fake MET MC')#namewizard(fname_pred.split('/')[-1].replace('.root','')))                
            
            print 'getting from data file', name.replace('obs','rands')
            
        else:
            fname_pred = prediction_sources[fkey]
            fpred = TFile(fname_pred)
            print 'trying to get', name, 'from', fpred.GetName()
            hpred = fpred.Get(name)
            hpred.SetTitle(fkey)#namewizard(fname_pred.split('/')[-1].replace('.root','')))
            if version == 'mumu': hpred.Scale(0.75)
        
        if 'FakeMet' in fkey and (userands): 
            if datamc=='data': hpred.Scale(1)
            if datamc=='mc': hpred.Scale(1000*lumi)
        else: 
            hpred.Scale(1000*lumi)
        hpred.SetDirectory(0)
        #if 'ZGGToNuNuGG' in fkey: hpred.Scale(13.7)
        #if 'WGJets' in fkey: hpred.Scale(3)
        
        histoStyler(hpred, color)     
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
        if kinvar=='HardMet' and not 'LDP' in name:
            xax = hObserved.GetXaxis()
            for ibin in range(1,xax.GetNbins()+1):
                if hObserved.GetBinLowEdge(ibin)>200: hObserved.SetBinContent(ibin, -99)
        if ('BDT' in kinvar):
            xax = hObserved.GetXaxis()
            for ibin in range(1,xax.GetNbins()+1):
                if hObserved.GetBinLowEdge(ibin)>0.1: hObserved.SetBinContent(ibin, -99)                    

    if not linscale: hObserved.GetYaxis().SetRangeUser(max(0.001,min(0.05, 0.01*hObserved.GetMinimum())),max(700000, 10*hObserved.GetMaximum()))

    oldalign = tl.GetTextAlign()    
    tl.SetTextAlign(oldalign)
    leg = mklegend(x1=.65, y1=.48, x2=.987, y2=.8, color=kWhite)
    #hpreds = [hpreds[2], hpreds[0], hpreds[1]]
    newfile.cd() 
    if dolimitinputs:   
        hObserved.Write()
        for h in hpreds: h.Write(h.GetTitle().replace('(','').replace(')','').replace('&','').replace(' ',''))
    if blindall: hObserved.Reset()
    hratio, hmethodsyst = FabDrawSystyRatio(cGold,leg,hObserved,hpreds,datamc=datamc,lumi=str(lumi), title = '',LinearScale=linscale,fractionthing='observed/method')

    pad1, pad2 = hmethodsyst[-2], hmethodsyst[-1]
    
    for ih in range(len(hpreds)): 
        if linscale:            
            hpreds[ih].GetYaxis().SetRangeUser(0.0,2.0*hpreds[ih].GetMaximum())
        else:
            hpreds[ih].GetYaxis().SetRangeUser(0.04,5000)

    pad1.cd()
    sighists = []
    leg2 = mklegend(x1=.16, y1=.58, x2=.47, y2=.82, color=kWhite)
    for isig, fsigname in enumerate(signals):
        fsig = TFile(fsigname)
        hist = fsig.Get(name)
        hist.SetDirectory(0)
        hist.Scale(1000*lumi)
        histoStyler(hist, sigcolors[isig])
        hist.SetLineWidth(3)
        fsig.Close()
        sighists.append(hist)
        sighists[-1].Draw('hist same')
        leg2.AddEntry(hist, fsigname.split('SMS-')[-1].split('_RA2')[0])
    leg2.Draw('same')
    hratio.GetYaxis().SetRangeUser(0.0,2.0)
    print 'setting', kinvar, 'title to', kinvar.replace('mva_','(for MVA) ')
    hratio.GetXaxis().SetTitle(kinvar.replace('mva_','(for MVA) '))
    cname = 'c_'+name[1:]
    newfile.cd()
    cGold.Write(cname)
    #print 'trying:','pdfs/ClosureTests/'+selection+'_'+method+'And'+standard+'_'+kinvar+'.pdf'
    cGold.Print('pdfs/Validation/'+datasource.split('/')[-1].replace('.root','')+cname[1:]+'.png')


print 'just created', newfile.GetName()
'''
scp pdfs/Validation/ beinsam@naf-cms11.desy.de:/afs/desy.de/user/b/beinsam/www/Diphoton/Validation/23March2021/TwoElectrons/
'''






exit(0)




















