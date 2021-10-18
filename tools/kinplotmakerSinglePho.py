from ROOT import *
from utils import *
import os,sys
from glob import glob
gROOT.SetBatch(1)

datamc = 'data'
datamc = 'mc'

dolimitinputs = False
from random import shuffle
#datamc = 'mc'


#/eos/uscms//store/group/lpcsusyphotons/hists_20July2021/ElectronBkgEst_BDTcut.root
#BinDivMET
#/eos/uscms//store/group/lpcsusyphotons/hists_22June2021/ZGGToNuNuGG_2016_hbdttwopsv.root
#hpred_mva_HardMET

#os.system('rm pdfs/Validation/*.png')

finalstate = 'mumu'
finalstate = 'badphopho'
finalstate = 'elel'
finalstate = 'phopho'
finalstate = 'pho'


try: year = sys.argv[1]
except:
    year = '2017'
    year = '2016'
    year = '2018'    

mcstring = {}
mcstring['2016'] = 'Summer16v3'
#mcstring['2017'] = 'Fall17'
mcstring['2017'] = 'Summer16v3'
mcstring['2018'] = 'Autumn18'
#mcstring['2018'] = 'Summer16v3'
mcstring['Run2'] = 'Summer16v3'


bdtselection = 'inverted'
bdtselection = 'nominal'
#bdtselection = 'allbdt' # this may only be suitable for MC version


if finalstate == 'mumu': chunk = 'bigchunks/bigmus'
if finalstate == 'elel': chunk = 'bigchunks/bigels'
if finalstate == 'badphopho': chunk = 'bigchunks/bigbadpho'
if finalstate == 'phopho': chunk = 'bigchunks/bigphotons'
if finalstate == 'pho': chunk = 'bigsphonks/bigphotons'

prediction_sources = {}
histOfFile = {}
if 'pho' in finalstate: prediction_sources['FakeMet']         = 'output/'+chunk+'/'+mcstring[year]+'.GJets.root'
else: prediction_sources['FakeMet']         = 'output/'+chunk+'/'+mcstring[year]+'.DYJetsNoTau.root'

if datamc=='mc':
    prediction_sources['t#bar{t}+jets'] = 'output/'+chunk+'/'+mcstring[year]+'.TTJets.root'
    prediction_sources['W+jets'] = 'output/'+chunk+'/'+mcstring[year]+'.WJetsToLNu.root'
    prediction_sources['G+jets'] = 'output/'+chunk+'/'+mcstring[year]+'.GJets.root'
    prediction_sources['ZG+Jets'] = 'output/'+chunk+'/'+mcstring[year]+'.ZGTo2NuG.root'    
elif datamc=='data':
    
    if bdtselection=='nominal':
        prediction_sources['e faking #gamma'] = '/eos/uscms//store/group/lpcsusyphotons/hists_20July2021/ElectronBkgEst_BDTcut.root'
        prediction_sources['#gamma#gamma+Z#rightarrow#nu#bar{#nu}'] = '/eos/uscms//store/group/lpcsusyphotons/hists_20July2021/ZGGToNuNuGG_2016_hbdttwopsv.root'
        histOfFile['#gamma#gamma+Z#rightarrow#nu#bar{#nu}'] = 'hObs_mva_HardMET'
        histOfFile['e faking #gamma'] = 'ScaledMETBins_nobindiv'
        
    else:
        prediction_sources['e faking #gamma'] = '/eos/uscms//store/group/lpcsusyphotons/hists_20July2021/ElectronBkgEst_BDTinv.root'
        prediction_sources['#gamma#gamma+Z#rightarrow#nu#bar{#nu}'] = '/eos/uscms//store/group/lpcsusyphotons/hists_20July2021/ZGGToNuNuGG_2016_lbdttwopsv.root'
        histOfFile['#gamma#gamma+Z#rightarrow#nu#bar{#nu}'] = 'hObs_mva_HardMET'
        histOfFile['e faking #gamma'] = 'ScaledMETBins_nobindiv'
        
        
      
    
else: exit()

colors = [2,4, kTeal-5, kYellow+2, kOrange+1, kGreen-2, kGreen-1, kGreen, kGreen+1, kGreen+2]
if finalstate=='elel' or finalstate=='mumu':
    fkeys = [['Z^{*}#rightarrow#tau#bar{#tau}',kViolet],['t#bar{t}Z',kBlack],['VV',kRed+1],['t#bar{t}+jets',kTeal-5],['FakeMet',kOrange+1]]#,['WJets',kYellow+1]
if 'phopho' in finalstate:
    if datamc=='mc': fkeys = [['W#gamma+jets',kYellow+1],['t#bar{t}+jets',kTeal-5],['FakeMet',kOrange+1],['Z^{*}#rightarrow#tau#bar{#tau}',kViolet],['#gamma#gamma+Z#rightarrow#nu#bar{#nu}',kViolet+2],['VV',kRed+1]]#,['WJets',kYellow+1]
    else: fkeys = [['e faking #gamma',kYellow+1],['FakeMet',kOrange+1],['#gamma#gamma+Z#rightarrow#nu#bar{#nu}',kViolet+2],['t#bar{t}+jets',kTeal-5]]#,['WJets',kYellow+1]

if finalstate=='pho':
    if datamc=='mc': fkeys = [['W+jets',kYellow+1],['FakeMet',kOrange+1], ['t#bar{t}+jets',kTeal-5], ['ZG+Jets', kViolet+2]]#,['WJets',kYellow+1]


doblinding = False

if bdtselection=='inverted': doblinding = False
blindall = True
userands = False


if finalstate=='pho':
    signals = glob('output/sphognals/weighted*.root')
    #signals = ['output/sphognals/weightedHists_pMSSM_MCMC_106_19786-SUS-RunIIAutumn18_SR.root',
    #       'output/sphognals/weightedHists_pMSSM_MCMC_399_10275-SUS-RunIIAutumn18_SR.root',
    #       'output/sphognals/weightedHists_pMSSM_MCMC_473_54451-SUS-RunIIAutumn18_SR.root',
    #        'output/sphognals/weightedHists_pMSSM_MCMC_86_7257-SUS-RunIIAutumn18_SR.root']
    
else: 
    signals = ['output/signals/weightedHists_posterior-'+mcstring[year]+'Fast.SMS-T6Wg_m1800.0d900.0_RA2AnalysisTree_SR.root',
           'output/signals/weightedHists_posterior-'+mcstring[year]+'Fast.SMS-T5Wg_m1300.0d1200.0_RA2AnalysisTree_SR.root',
           'output/signals/weightedHists_posterior-'+mcstring[year]+'Fast.SMS-T5Wg_m1700.0d100.0_RA2AnalysisTree_SR.root']
#signals = []
#signals = glob('output/signals/*.root')
#shuffle(signals)
#signals = signals[:5]
sigcolors = [kBlue+1, kRed+1, kGray+1, kMagenta, kTeal-5]

if year=='2016':
    lumi = 35.9 # 2016 
    #lumi = 2.57 #lumi = 5.746 # B    
    if finalstate=='mumu': datasource = 'output/'+chunk+'/Run2016_SingleMu.root'
    if finalstate=='elel': datasource = 'output/'+chunk+'/Run2016_DoubleEG.root'
    if 'phopho' in finalstate: datasource = 'output/'+chunk+'/Run2016_DoubleEG.root'
if year=='2017':
    datasource = 'output/'+chunk+'/Run2017_Photon.root'
    datasource = 'output/'+chunk+'/Run2017_DoubleEG.root'
    lumi = 41.52
if year=='2018':
    datasource = 'output/'+chunk+'/Run2018_DoubleEG.root'
    lumi = 54.52

if year=='Run2':
    datasource = 'output/'+chunk+'/Run2_DoubleEG.root'
    lumi = 131.94

if year=='2018A':
	lumi = 13.95
if year=='2018D':
	lumi = 31.74
if year=='2018C':
	lumi = 6.89

if datamc=='mc' and False:# this would be used also for some closure stuff, but maybe we're trying to turn in this script
    datasource = 'output/bigchunks/'+mcstring[year]+'.QCD.root'
    doblinding = False
    
fdata = TFile(datasource)
fdata.ls()
keys = fdata.GetListOfKeys()
keys = sorted(keys,key=lambda thing: thing.GetName())

redoBinning = {}
#redoBinning['HardMet'] = [130,150,185,250,500]
#/uscms_data/d3/sbein/Diphoton/18Jan2019/CMSSW_10_1_0/src/limitcode

linscale = False

gStyle.SetOptStat(0)
gROOT.ForceStyle()

#shuffle(colors)

newfile = TFile('plots_'+year+'_'+datamc+'_'+finalstate+'_BDT'+bdtselection+'.root','recreate')

fkeys.reverse()

for key in keys:
    name = key.GetName()
    if 'Vs' in name: continue
    if not name[0]=='h': continue
    if not 'obs' in name: continue
    hObserved = fdata.Get(name).Clone()
    if datamc=='mc': hObserved.Scale(1000*lumi)
    print 'here we are', name

    hObserved.SetTitle('Data ('+year+')')
    histoStyler(hObserved, 1)
    hpreds = []
    
    for fkey, color in fkeys:
        fname_pred = prediction_sources[fkey]
        print 'fkey', fkey
        if datamc=='data' and fkey=='t#bar{t}+jets': continue            
        if 'FakeMet' in fkey:
            if userands: 
                #hpred = fpred.Get(name.replace('obs','rands'))
                fpred = TFile()
                hpred = fdata.Get(name.replace('obs','rands'))
                hpred.SetTitle('R&S prediction')
                hpred.Scale(1.16)
                if datamc=='mc': hpred.Scale(1000*lumi)
                

                ftt = TFile(prediction_sources['t#bar{t}+jets'])
                print 'looking in ', prediction_sources['t#bar{t}+jets'], 'for', name.replace('obs','rands')
                #htt = ftt.Get(name.replace('obs','rands'))
                #if datamc=='mc': htt.Scale(1000*lumi)
                #if finalstate == 'mumu': htt.Scale(0.75)
                #hpred.Add(htt,-1)
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
            if datamc=='mc': thename = name
            elif datamc=='data': thename = histOfFile[fkey]
                
            print 'trying to get', thename, 'from', fpred.GetName()
            hpred = fpred.Get(thename)
            hpred.SetTitle(fkey)#namewizard(fname_pred.split('/')[-1].replace('.root',''))            
            #if finalstate == 'mumu': hpred.Scale(0.75)
        
        if 'FakeMet' in fkey and (userands): 
            if datamc=='data': hpred.Scale(1)
            ###if datamc=='mc': hpred.Scale(1000*lumi)
        else: 
            if datamc=='mc': hpred.Scale(1000*lumi)
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
    #if not kinvar=='HardMet': continue
    
    print 'found kinvar', kinvar, 'from', name
    cGold = TCanvas('cEnchilada','cEnchilada', 800, 800)
    if kinvar in redoBinning.keys():
        print 'redoing the binning', kinvar
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
                if hObserved.GetBinLowEdge(ibin)>0.3: hObserved.SetBinContent(ibin, -99)
        if kinvar=='HardMet' and (not 'LDP' in name) and (not 'LowBDT' in name):
            xax = hObserved.GetXaxis()
            for ibin in range(1,xax.GetNbins()+1):
                if hObserved.GetBinLowEdge(ibin)>=100: hObserved.SetBinContent(ibin, -99)
        if ('BDT' in kinvar):
            xax = hObserved.GetXaxis()
            for ibin in range(1,xax.GetNbins()+1):
                if hObserved.GetBinLowEdge(ibin)>-0.2: hObserved.SetBinContent(ibin, -99)                    

    if not linscale: hObserved.GetYaxis().SetRangeUser(max(0.0005,min(0.001, 0.01*hObserved.GetMinimum())),max(700000, 10*hObserved.GetMaximum()))

    newfile.cd()
    ##hObserved.Write('hobs_'+name+'_'+kinvar)
    ##for ih in range(len(hpreds)):  hpreds[ih].Write(hpreds[ih].GetTitle()+'_'+name+'_'+kinvar)
        
    oldalign = tl.GetTextAlign()    
    tl.SetTextAlign(oldalign)
    leg = mklegend(x1=.62, y1=.5, x2=.9, y2=.8, color=kWhite)
    #hpreds = [hpreds[2], hpreds[0], hpreds[1]]
    newfile.cd() 
    if dolimitinputs:   
        ##hObserved.Write()
        for h in hpreds: h.Write(h.GetTitle().replace('(','').replace(')','').replace('&','').replace(' ',''))
    #if doblinding and blindall: hObserved.Reset()
    hratio, hmethodsyst = FabDrawSystyRatio(cGold,leg,hObserved,hpreds,datamc=datamc,lumi=str(lumi), title = '',LinearScale=linscale,fractionthing='observed/method')

    pad1, pad2 = hmethodsyst[-2], hmethodsyst[-1]
    
    for ih in range(len(hpreds)): 
        if linscale:            
            hpreds[ih].GetYaxis().SetRangeUser(0.0,2.0*hpreds[ih].GetMaximum())
        else:
            hpreds[ih].GetYaxis().SetRangeUser(0.01,20000000)

    pad1.cd()
    sighists = []
    leg2 = mklegend(x1=.16, y1=.58, x2=.5, y2=.82, color=kWhite)
    for isig, fsigname in enumerate(signals):
        print 'looking for', name, 'in', fsigname
        fsig = TFile(fsigname)
        hist = fsig.Get(name)
        hist.Scale(1000*lumi)
        if kinvar in redoBinning.keys(): hist = hist.Rebin(nbins,'',newxs)
        hist.SetDirectory(0)        
        histoStyler(hist, sigcolors[isig])
        #histoStyler(hist, kBlue+isig)
        hist.SetLineWidth(3)
        fsig.Close()
        sighists.append(hist)
        sighists[-1].Draw('hist same')
        leg2.AddEntry(hist, fsigname.split('/')[-1].split('weightedHists_')[-1].split('-SUS')[0].split('SMS-')[-1].split('_RA2')[0].replace('.root',''))
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




















