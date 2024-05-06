
import os, sys
from ROOT import *
from utils import *
from glob import glob
gROOT.SetBatch(1)
gStyle.SetOptStat(0)

dopred = False

'''
#/eos/uscms//store/group/lpcsusyphotons/SinglePhoRandS_skimsv8
rm output_mopho/mediumchunks/*
rm output_mopho/smallchunks/*
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.GJets_DR-0p4_HT-100To200" & 
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.GJets_DR-0p4_HT-200To400" & 
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.GJets_DR-0p4_HT-400To600" & 
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.GJets_DR-0p4_HT-600ToInf" &
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.TTJets_Tune*.root" 
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.ZGTo2NuG_Tune*.root" 
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.WJetsToLNu_HT-70To*.root" &
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.WJetsToLNu_HT-100To*.root" &
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.WJetsToLNu_HT-200To*.root" &
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.WJetsToLNu_HT-400To*.root" 
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.WJetsToLNu_HT-600To*.root" &
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.WJetsToLNu_HT-800To*.root" &
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.WJetsToLNu_HT-1200To*.root" &
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "Autumn18.WJetsToLNu_HT-2500To*.root" &
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "pMSSM_MCMC_106_19786-SUS-RunIIAutumn18*.root" 
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "pMSSM_MCMC_473_54451-SUS-RunIIAutumn18*.root" 
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "pMSSM_MCMC_86_7257-SUS-RunIIAutumn18*.root" 
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "pMSSM_MCMC_70_90438-SUS-RunIIAutumn18*.root"
python3 tools/submitjobs_fnal.py --analyzer tools/DrawAnalyzeSinglePho.py --fnamekeyword "pMSSM_MCMC_399_10275-SUS-RunIIAutumn18*.root" 

python3 tools/mergeHistosFinalizeWeights.py

rm output_mopho/bigchunks/*
hadd -f output_mopho/bigchunks/Autumn18.GJets.root output_mopho/mediumchunks/weightedHists_Autumn18.GJets_DR-0p4_HT*.root 
hadd -f output_mopho/bigchunks/Autumn18.TTJets.root output_mopho/mediumchunks/weightedHists_Autumn18.TTJets_Tune*.root 
hadd -f output_mopho/bigchunks/Autumn18.ZGTo2NuG.root output_mopho/mediumchunks/weightedHists_Autumn18.ZGTo2NuG_Tune*.root 
hadd -f output_mopho/bigchunks/Autumn18.WJetsToLNu.root output_mopho/mediumchunks/weightedHists_Autumn18.WJetsToLNu_*.root 
hadd -f output_mopho/bigchunks/Run2018_DoubleEG.root output_mopho/mediumchunks/weightedHists_Autumn18.GJets_DR-0p4_HT*.root
hadd -f output_mopho/bigchunks/Run2018_DoubleEG.root output_mopho/mediumchunks/weightedHists_Autumn18.*.root
rm output_mopho/signals/*
cp output_mopho/smallchunks/weightedHists_pMSSM_MCMC*Autumn18_SR.root output_mopho/signals/


#python tools/DrawAnalyzeSinglePho.py "/eos/uscms//store/group/lpcsusyphotons/SinglePhoRandS_skimsv8/*pMSSM_MCMC_399_10275-SUS-RunIIAutumn18*.root" 
'''

import argparse
parser = argparse.ArgumentParser()
defaultfkey = 'Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_28'
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultfkey,help="file")
parser.add_argument("-jersf", "--JerUpDown", type=str, default='Nom',help="JER scale factor (Nom, Up, ...)")
parser.add_argument("-dtmode", "--dtmode", type=str, default='PixAndStrips',help="PixAndStrips, PixOnly, PixOrStrips")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
parser.add_argument("-smearvar", "--smearvar", type=str, default='Nom',help="use gen-kappa")
parser.add_argument("-ps", "--analyzeskims", type=bool, default=False,help="use gen-kappa")
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
parser.add_argument("-outdir", "--outdir", type=str, default='output_mopho/smallchunks')
args = parser.parse_args()
nfpj = args.nfpj
fnamekeyword = args.fnamekeyword.strip()
fileskey = fnamekeyword
analyzer = args.analyzer
analyzeskims = args.analyzeskims
analyzer = analyzer.replace('python/','').replace('tools/','')
JerUpDown = args.JerUpDown
smearvar = args.smearvar
outdir = args.outdir


print ('fileskey', fileskey)
if 'Run20' in fileskey: isdata = True
else: isdata = False




pixelseedstring = "&& (analysisPhotons_hasPixelSeed[0]==0)"
#showershapestring = "&& (Pho1_passLooseSigmaIetaIeta==1)"
universalconstraint = ' abs(HardMetMinusMet)<100 && mva_Photons1Et>20 && mva_Ngoodjets>1'# + showershapestring
universalconstraint += pixelseedstring

if ',' in fileskey: fins = fileskey.split(',')
elif ' ' in fileskey: fins = fileskey.split(' ')
else: fins = glob(fileskey)
if not isdata:
    ccounter = TChain('tcounter')
    for fname in fins: ccounter.Add(fname.replace('/eos/uscms/','root://cmseos.fnal.gov//'))
    nev_local = ccounter.GetEntries()
    print ('nevents in total =', nev_local)
    
chain = TChain('TreeMaker2/PreSelection')
print ('fileskey', fileskey)
for fname in fins: chain.Add(fname.replace('/eos/uscms/','root://cmseos.fnal.gov//'))
chain.Show(0)
print ('nevents in skim =', chain.GetEntries())


isprivatesignal = bool('pMSSM' in fins)
if isprivatesignal:
    xsecdict = {'pMSSM_MCMC_106_19786': 1.26100000e-01, 'pMSSM_MCMC_399_10275': 3.98200000e-02, 'pMSSM_MCMC_473_54451': 9.87200000e-01, 'pMSSM_MCMC_86_7257': 2.99100000e-03, 'pMSSM_MCMC_70_90438':7.52100000e-01}
    thekey = 'pMSSM'+fname.split('pMSSM')[-1].split('-SUS')[0]
    xsec = xsecdict[thekey]
    evtweight = str(xsec)#+'/'+str(nev_local)
elif isdata: evtweight = '1'
else: evtweight = 'CrossSection'

promptname = 'Photons_nonPrompt'
#promptname = 'Photons_genMatched'
WP = 'Medium/2'
WP = 'Loose'

plotBundle = {}

#2d plots
plotBundle['OnePho_HardMet'] = ['min(HardMETPt,999)>>hadchadc(20,0,1000)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_NJets'] = ['min(mva_Ngoodjets,9)>>hadc(11,-1,10)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_Pho1Pt'] = ['min(analysisPhotons[0].Pt(),499.9)>>hadc(100,0,500)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_Eta1Pt'] = ['min(analysisPhotons[0].Eta(),499.9)>>hadc(25,-5,5)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_Pho2Pt'] = ['min(analysisPhotons[1].Pt(),499.9)>>hadc(100,0,500)','HardMETPt>200 && NPhotons>=2',False]
plotBundle['OnePho_Eta2Pt'] = ['min(analysisPhotons[1].Eta(),499.9)>>hadc(25,-5,5)','HardMETPt>200 && NPhotons>=2',False]
plotBundle['OnePho_ST_jets'] = ['mva_ST_jets>>hadc(16,0,800)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_ST'] = ['mva_ST>>hadc(10,100,2300)','HardMETPt>200 && NPhotons>=1',False]
plotBundle['OnePho_nPhotons'] = ['NPhotons>>hadc(3,1,4)','HardMETPt>200 && NPhotons>=1',False]


infilekey = fileskey.split('/')[-1].replace('*','').replace('.root','')
newfilename = 'output_mopho/smallchunks/hists_'+infilekey+'.root'
if 'T5' in infilekey or 'T6' in infilekey: newfilename = newfilename.replace('smallchunks','sphognals')

    
fnew = TFile(newfilename, 'recreate')
print ('will make file', fnew.GetName())
hHt = TH1F('hHt','hHt',1,0,2); hHt.Sumw2()
for i in range(nev_local): hHt.Fill(1)
hHt.Write()
c1 = mkcanvas()
c2 = mkcanvas('c2')

for key in plotBundle:
    drawarg, constraint, blinding = plotBundle[key]
    obsweight = evtweight+'*('+constraint + ' && '+ universalconstraint + ' && IsRandS==0)'
    #puWeight
    print ('drawing', drawarg, ', with constraint:', obsweight)
    chain.Draw(drawarg,obsweight, 'e')
    hobs = chain.GetHistogram().Clone(key+'_obs')
    if not ('Vs' in key): hobs.GetYaxis().SetRangeUser(0.01,10000*hobs.GetMaximum())

    c1.cd()

    drawarg = drawarg
    randsconstraint = constraint
    methweight = evtweight+'/NSmearsPerEvent*('+ randsconstraint + ' && '+universalconstraint+ ' && IsRandS==1 && rebalancedHardMet<120)'
    #puWeight
    print ('drawing', drawarg, ', with constraint:', methweight)
    chain.Draw(drawarg, methweight, 'e')
    hrands = chain.GetHistogram().Clone(key+'_rands') 
    if blinding and 'Run20' in fileskey: hobs = hrands.Clone(key+'_obs')
    if not ('Vs' in drawarg): hrands.GetYaxis().SetRangeUser(0.01,10000*hrands.GetMaximum())
    if 'ZGG' in fileskey: histoStyler(hrands, kViolet+1)
    else: histoStyler(hrands, kAzure-8)
    hrands.SetFillColor(hrands.GetLineColor())
    hrands.SetFillStyle(1001)

    leg = mklegend(x1=.45, y1=.57, x2=.95, y2=.74, color=kWhite)
    if 'ZGG' in fileskey: hobs.SetTitle('Summer16 ZGG')
    else: hobs.SetTitle('observed')
    hobs.GetXaxis().SetTitle(key.split('_')[-1])
    hrands.GetXaxis().SetTitle(key.split('_')[-1])
    hrands.SetTitle('rebalance and smeared')
    if dopred: 
        hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,hobs,[hrands],datamc='MC',lumi='n/a', title = '', LinearScale=False, fractionthing='observed / method')
        c1.Update()
        c1.Write('c_'+key)
        c1.Print('pdfs/Closure/'+key+'.pdf')        
    hrands.Write('h'+hrands.GetName())
    hobs.Write('h'+hobs.GetName())





print ('just created', fnew.GetName())
fnew.Close()

