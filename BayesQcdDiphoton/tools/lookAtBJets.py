

from ROOT import *
from utils import *
from glob import glob
gROOT.SetBatch(1)

ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/scan/'
flist = glob(ra2bspace+'*.root')
shortfname = 'T1bbbb_mMother-1500_mLSP-100_MC2017'
#shortfname = 'T1qqqq_mMother-1400_mLSP-100_MC2017'
print 'going to check for ', shortfname
chainfast = TChain('tree')
for line in flist:
    if not shortfname in line: continue
    fname = line.strip()
    #fname = ra2bspace+fname
    fname = fname.replace('/eos/uscms/','root://cmseos.fnal.gov//')
    print 'adding fast', fname
    chainfast.Add(fname)


ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/'
fnamefilename = 'usefulthings/filelistV17.txt'
fnamefile = open(fnamefilename)
lines = fnamefile.readlines()
shortfname = 'Fall17.SMS-T1bbbb_mGluino-1500_mLSP-100'
#shortfname = 'Fall17.SMS-T1qqqq_mGluino-1400_mLSP-100'
print 'going to check for ', shortfname
fnamefile.close()

chain = TChain('TreeMaker2/PreSelection')
for line in lines:
    if not shortfname in line: continue
    fname = line.strip()
    fname = ra2bspace+fname
    fname = fname.replace('/eos/uscms/','root://cmseos.fnal.gov//')
    print 'adding full', fname
    chain.Add(fname)


nfast = chainfast.GetEntries()
nfull = chain.GetEntries()


chainfast.Draw('Jets[0].Pt()', 'CrossSection*1.0/'+str(nfast)+'*(Jets_bJetTagDeepCSVBvsAll[0]>0.84)')
hfast = chainfast.GetHistogram().Clone('hfast')
chain.Draw('Jets[0].Pt()', 'CrossSection*1.0/'+str(nfull)+'*(Jets_bJetTagDeepCSVBvsAll[0]>0.84)')
hfull = chain.GetHistogram().Clone()
print 'hfull.GetEntries()', hfull.GetEntries()

fnew = TFile('stored-btagstuff-ttjets.root', 'recreate')
hfast.Write('hfast')
hfull.Write('hfull')

print 'just created', fnew.GetName()
exit(0)
