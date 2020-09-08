import os, sys
from ROOT import *
from utils import *
from glob import glob
gROOT.SetBatch(1)
gStyle.SetOptStat(0)

'''
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.QCD_HT200to300*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.QCD_HT300to500*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.QCD_HT1000to1500*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.QCD_HT500to700*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.QCD_HT700to1000*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.QCD_HT1500to2000*" 
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.QCD_HT2000toInf*" &

nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.GJets_DR-0p4_HT-100To200*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.GJets_DR-0p4_HT-200To400*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.GJets_DR-0p4_HT-400To600*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.GJets_DR-0p4_HT-600ToInf*" &

nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.ZGGToNuNuGG_5f_TuneCUET*.root"&

nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.WGJets_MonoPhoton_PtG-40to130*.root"&
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Summer16v3.WGJets_MonoPhoton_PtG-130*.root"&


python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016B-17Jul2018_ver2-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016C-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016D-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016E-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016F-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016G-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016H-17Jul2018-v1.SinglePhoton*" 

python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016B-17Jul2018_ver2-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016C-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016D-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016E-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016F-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016G-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2016H-17Jul2018-v1.DoubleEG*" 

python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2017B*SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2017C*SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2017D*SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2017E*SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS/*Run2017F*SinglePhoton*" 


python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_28July2020/*Run2018A*EGamma*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_28July2020/*Run2018B*EGamma*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_28July2020/*Run2018C*EGamma*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_28July2020/*Run2018D*EGamma*"

'''


'''

nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Summer16v3.GJets_DR-0p4_HT-100To200*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Summer16v3.GJets_DR-0p4_HT-200To400*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Summer16v3.GJets_DR-0p4_HT-400To600*" &
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Summer16v3.GJets_DR-0p4_HT-600ToInf*" &

nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Summer16v3.ZGGToNuNuGG_5f_TuneCUET*.root"&

nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Summer16v3.WGJets_MonoPhoton_PtG-40to130*.root"&
nohup python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Summer16v3.WGJets_MonoPhoton_PtG-130*.root"&


python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016B-17Jul2018_ver2-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016C-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016D-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016E-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016F-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016G-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016H-17Jul2018-v1.SinglePhoton*" 

python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016B-17Jul2018_ver2-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016C-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016D-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016E-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016F-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016G-17Jul2018-v1.SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016H-17Jul2018-v1.SinglePhoton*" 

python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2017B*SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2017C*SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2017D*SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2017E*SinglePhoton*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2017F*SinglePhoton*" 

python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016B-17Jul2018_ver2-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016C-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016D-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016E-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016F-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016G-17Jul2018-v1.DoubleEG*" &
python tools/DrawAnalyze.py "/eos/uscms//store/group/lpcsusyphotons/TreeMakerRandS_v2/*Run2016H-17Jul2018-v1.DoubleEG*" 



'''

try: fileskey = sys.argv[1]
except: fileskey = '/eos/uscms//store/user/sbein/RebalanceAndSmear/Run2ProductionV17/*Summer16v3.QCD*.root'

print 'fileskey', fileskey
if 'Run20' in fileskey: isdata = True
else: isdata = False

universalconstraint = ' abs(HardMetMinusMet)<80 && mva_Photons1Et>80'
acmestr = 'NoAcme' if 'NoAcme' in fileskey else 'YesAcme'

fins = glob(fileskey)
ccounter = TChain('tcounter')
for fname in fins: ccounter.Add(fname.replace('/eos/uscms/','root://cmsxrootd.fnal.gov//'))
nev_total = ccounter.GetEntries()

chain = TChain('TreeMaker2/PreSelection')
print 'fileskey', fileskey
for fname in fins: chain.Add(fname.replace('/eos/uscms/','root://cmsxrootd.fnal.gov//'))
chain.Show(0)
print 'nevents =', chain.GetEntries(), nev_total

chain.SetBranchStatus('NJets', 1)
chain.SetBranchStatus('HT', 1)
chain.SetBranchStatus('BTags', 1)
chain.SetBranchStatus('Jets', 1)

if isdata: evtweight = '1'
else: evtweight = 'CrossSection/'+str(nev_total)



promptname = 'Photons_nonPrompt'
#promptname = 'Photons_genMatched'
WP = 'Medium/2'
WP = 'Loose'



plotBundle = {}

#plotBundle['Baseline2Pho_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(32,0,3.2)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2',True]
plotBundle['Baseline2PhoLDP_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_HardMet'] = ['HardMETPt>>hadc(20,120,520)','NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_massGG'] = ['mass_GG>>hadc(40,50,850)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_mva_BDT'] = ['mva_BDT>>hadc(12,-1.2,1.2)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_Pho1Pt'] = ['mva_Photons0Et>>hadc(10,50,1050)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_Pho2Pt'] = ['mva_Photons1Et>>hadc(10,50,1050)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_mva_Pt_GG'] = ['mva_Pt_GG>>hadc(10,0,750)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_mva_ST_jets'] = ['mva_ST_jets>>hadc(16,0,800)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]

plotBundle['Baseline2PhoLDP_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(16,0,3.2)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2',True]##this appears twice
plotBundle['Baseline2PhoLDP_mva_dPhi_GGHardMET'] = ['mva_dPhi_GGHardMET>>hadc(18,-3.6,3.6)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLDP_mva_DPhi_GG'] = ['mva_dPhi_GG>>hadc(18,-3.6,3.6)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]

plotBundle['Baseline2PhoLDP_mva_ST'] = ['mva_ST>>hadc(10,100,2300)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_min_dPhi<0.3',True]
plotBundle['Baseline2PhoLowBDT_HardMet'] = ['HardMETPt>>hadc(20,120,520)','NPhotons'+WP+'==2 && mva_BDT<-0.2',True]
plotBundle['Baseline2PhoLowBDT_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_BDT<-0.2',True]
plotBundle['Baseline2PhoLowBDT_massGG'] = ['mass_GG>>hadc(40,50,850)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_BDT<-0.2',True]
plotBundle['Baseline2PhoLowBDT_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_BDT<-0.2',True]
plotBundle['Baseline2PhoLowBDT_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_BDT<-0.2',True]    

plotBundle['Baseline2PhoLowBDT_Pho1Pt'] = ['mva_Photons0Et>>hadc(10,50,1050)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_BDT<-0.2',True]
plotBundle['Baseline2PhoLowBDT_Pho2Pt'] = ['mva_Photons1Et>>hadc(10,50,1050)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_BDT<-0.2',True]
plotBundle['Baseline2PhoLowBDT_mva_Pt_GG'] = ['mva_Pt_GG>>hadc(10,0,750)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_BDT<-0.2',True]
plotBundle['Baseline2PhoLowBDT_mva_ST_jets'] = ['mva_ST_jets>>hadc(16,0,800)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_BDT<-0.2',True]
plotBundle['Baseline2PhoLowBDT_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(16,0,3.2)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2 && mva_BDT<-0.2',True]


if 'Summer' in fileskey:
    plotBundle['Baseline2PhoHDP_HardMet'] = ['HardMETPt>>hadc(20,120,520)','NPhotons'+WP+'==2 && mva_min_dPhi>0.3',True]
    plotBundle['Baseline2PhoHDP_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_min_dPhi>0.3',True]
    plotBundle['Baseline2PhoHDP_massGG'] = ['mass_GG>>hadc(40,50,850)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_min_dPhi>0.3',True]
    plotBundle['Baseline2PhoHDP_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_min_dPhi>0.3',True]
    plotBundle['Baseline2PhoHDP_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_min_dPhi>0.3',True]
    plotBundle['Baseline2PhoHDP_mva_BDT'] = ['mva_BDT>>hadc(12,-1.2,1.2)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_min_dPhi>0.3',True]
    plotBundle['Baseline2PhoHDP_dPhi_GGHardMET'] = ['mva_dPhi_GGHardMET>>hadc(18,-3.6,3.6)','HardMETPt>120  && NPhotons'+WP+'==2 && mva_min_dPhi>0.3',True]    

    plotBundle['Baseline2Pho_HardMet'] = ['HardMETPt>>hadc(20,120,520)','NPhotons'+WP+'==2',True]
    plotBundle['Baseline2Pho_NJets'] = ['mva_Ngoodjets>>hadc(12,-2,10)','HardMETPt>120  && NPhotons'+WP+'==2',True]
    plotBundle['Baseline2Pho_massGG'] = ['mass_GG>>hadc(40,50,850)','HardMETPt>120  && NPhotons'+WP+'==2',True]
    plotBundle['Baseline2Pho_Pho1_hadTowOverEM'] = ['Pho1_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>120  && NPhotons'+WP+'==2',True]
    plotBundle['Baseline2Pho_Pho2_hadTowOverEM'] = ['Pho2_hadTowOverEM>>hadc(16,0,0.08)','HardMETPt>120  && NPhotons'+WP+'==2',True]
    plotBundle['Baseline2Pho_mva_BDT'] = ['mva_BDT>>hadc(12,-1.2,1.2)','HardMETPt>120  && NPhotons'+WP+'==2',True]    

    plotBundle['Baseline2Pho_mva_dPhi_GGHardMET'] = ['mva_dPhi_GGHardMET>>hadc(18,-3.6,3.6)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2',True]
    plotBundle['Baseline2Pho_mva_DPhi_GG'] = ['mva_dPhi_GG>>hadc(18,-3.6,3.6)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2',True]    
    plotBundle['Basleine2Pho_mva_min_dPhi'] = ['mva_min_dPhi>>hadc(18,-0.2,3.4)','HardMETPt>120 && HardMETPt<200 && NPhotons'+WP+'==2',True]    

    


print 'fileskey', fileskey
infilekey = fileskey.split('/')[-1].replace('*','').replace('.root','')

fnew = TFile('output/mediumchunks/weightedHists_'+infilekey+'_'+acmestr+'.root', 'recreate')
print 'will make file', fnew.GetName()
c1 = mkcanvas()
c2 = mkcanvas('c2')

for key in plotBundle:
    drawarg, constraint, usernsvalue = plotBundle[key]
    obsweight = evtweight+'*('+constraint + ' && '+ universalconstraint + ' && IsRandS==0)'
    #puWeight
    print 'drawing', drawarg, ', with constraint:', obsweight
    chain.Draw(drawarg,obsweight, 'e')
    hobs = chain.GetHistogram().Clone(key+'_obs')
    hobs.GetYaxis().SetRangeUser(0.01,10000*hobs.GetMaximum())

    c1.cd()

    drawarg = drawarg
    randsconstraint = constraint
    methweight = evtweight+'/NSmearsPerEvent*('+ randsconstraint + ' && '+universalconstraint+ ' && IsRandS==1)'
    #puWeight
    print 'drawing', drawarg, ', with constraint:', methweight
    chain.Draw(drawarg, methweight, 'e')
    hrands = chain.GetHistogram().Clone(key+'_rands') 
    hrands.GetYaxis().SetRangeUser(0.01,10000*hrands.GetMaximum())
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
    hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,hobs,[hrands],datamc='MC',lumi='n/a', title = '', LinearScale=False, fractionthing='truth / method')
    c1.Update()
    c1.Write('c_'+key)
    hrands.Write('h'+hrands.GetName())
    hobs.Write('h'+hobs.GetName())
    c1.Print('pdfs/Closure/RawDoubleEmEnriched/'+key+'.pdf')        
     









print 'just created', fnew.GetName()
fnew.Close()




'''
hadd -f output/bigchunks/Summer16v3.QCD.root output/mediumchunks/weightedHists_Summer16v3.QCD_HT*.root

hadd -f output/bigchunks/Summer16v3.GJets.root output/mediumchunks/weightedHists_Summer16v3.GJets_DR-0p4_HT*.root &
hadd -f output/bigchunks/Summer16v3.ZGGToNuNuGG.root output/mediumchunks/weightedHists_Summer16v3.ZGGToNuNuGG*.root &
hadd -f output/bigchunks/Summer16v3.WGJets_MonoPhoton.root output/mediumchunks/weightedHists_Summer16v3.WGJets_MonoPhoton*.root &
hadd -f output/bigchunks/Run2016_SinglePhoton.root output/mediumchunks/weightedHists_Run2016*SinglePho*.root &
hadd -f output/bigchunks/Run2017_SinglePhoton.root output/mediumchunks/weightedHists_Run2017*SinglePho*.root &

hadd -f output/bigchunks/Run2016_DoubleEG.root output/mediumchunks/weightedHists_Run2016*DoubleEG*.root &
hadd -f output/bigchunks/Run2017_DoubleEG.root output/mediumchunks/weightedHists_Run2017*DoubleEG*.root &

'''
