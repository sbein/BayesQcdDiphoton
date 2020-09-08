

from ROOT import *
from utils import *
from glob import glob
gROOT.SetBatch(1)


'''with a grid proxy:
xrdfs root://hepxrd01.colorado.edu:1094/ ls /store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/scan/
'''

isfast = True
isfull = not isfast

do2016 = False
do2017 = not do2016

dosm = True

#fname = fname.replace('root://cmsxrootd.fnal.gov///store/group/lpcsusyhad','root://hepxrd01.colorado.edu:1094//store/user/aperloff')

undojec = False

if isfast:
    ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/scan/'
    flist = glob(ra2bspace+'*.root')



    #flist = usefulthings/filelistAlexScan.txt
    
    chain = TChain('tree')
    if do2017: 
        if dosm: 
            shortfname = 'Fall17Fast.TTJets_SingleLeptFromT_Tune'
            chain = TChain('TreeMaker2/PreSelection')
            #fnamefilename = 'usefulthings/filelistV17.txt'
            fnamefilename = 'usefulthings/filelistAlexx.txt'            
            fnamefile = open(fnamefilename)
            flist = fnamefile.readlines()
            ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/'
            ra2bspace = ''
            for iflist in range(len(flist)): flist[iflist] = ra2bspace+flist[iflist]
            fnamefile.close()
                        
        else: 
            shortfname = 'T1bbbb_mMother-1500_mLSP-100_MC2017'
            #shortfname = 'T1bbbb_mMother-1800_mLSP-200_MC2017'
    if do2016: 
        if dosm: 
            shortfname = 'Summer16v3Fast.TTJets_SingleLeptFromTbar_Tune'
            chain = TChain('TreeMaker2/PreSelection')
            #fnamefilename = 'usefulthings/filelistV17.txt'
            fnamefilename = 'usefulthings/filelistAlexx.txt'
            fnamefile = open(fnamefilename)
            flist = fnamefile.readlines()
            ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/'
            ra2bspace = ''
            for iflist in range(len(flist)): flist[iflist] = ra2bspace+flist[iflist]
            fnamefile.close()
        else: shortfname = 'T1bbbb_mMother-1500_mLSP-100_MC2016'
    print 'going to check for ', shortfname
    
    for line in flist:
        if not shortfname in line: continue
        fname = line.strip()
        #fname = ra2bspace+fname
        if do2017 or True: fname = fname.replace('/store/user/','root://hepxrd01.colorado.edu:1094//store/user/')
        else: fname = fname.replace('/eos/uscms/','root://cmseos.fnal.gov//')
        print 'adding fast', fname
        chain.Add(fname)

if isfull:
    ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/'
    fnamefilename = 'usefulthings/filelistV17.txt'
    fnamefile = open(fnamefilename)
    lines = fnamefile.readlines()
    if do2017: 
        if dosm: shortfname = 'Fall17.TTJets_SingleLeptFromTbar_Tune'
        else: shortfname = 'Fall17.SMS-T1bbbb_mGluino-1500_mLSP-100'
    if do2016: 
        if dosm: shortfname = 'Summer16v3.TTJets_SingleLeptFromT_Tune'
        else: shortfname = 'Summer16v3.SMS-T1bbbb_mGluino-1500_mLSP-100_Tune'
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


chain.Show(0)

newname = 'jetres.root'

if isfast: newname = newname.replace('.root', '_fast.root')
if isfull: newname = newname.replace('.root', '_full.root')
if do2016: newname = newname.replace('.root', '_2016.root')
if do2017: newname = newname.replace('.root', '_2017.root')

if dosm: newname = newname.replace('.root', '_ST.root')
else: newname = newname.replace('.root', '_T1bbbb.root')

if undojec: newname = newname.replace('.root', '_NoJec.root')
fnew = TFile(newname, 'recreate')


nevents = min(1000000,chain.GetEntries())
print 'will process', nevents

hress = {}
hresbs= {}

ptrange = range(0,1000,30)
for ibinedge, binedge in enumerate(ptrange[:-1]):
    binedges = str(binedge)+'to'+str(ptrange[ibinedge+1])
    hress[binedges] = TH1F('hres_'+binedges,'hres_'+binedges,100,0,4)
    hresbs[binedges] = TH1F('hresb_'+binedges,'hresb_'+binedges,100,0,4) 

hResponseVsGenPt_b = TH2F('hResponseVsGenPt_b','hResponseVsGenPt_b',40,0,1200,100,0,4)
hResponseVsGenPt_light = TH2F('hResponseVsGenPt_light','hResponseVsGenPt_light',40,0,1200,100,0,4)
    

hHT = TH1F('hHT','hHT', 40,0,4000)
hMET = TH1F('hMET','hMET', 40,0,1600)


for ientr in range(nevents):
    chain.GetEntry(ientr)
    if ientr%100==0: print 'processing', ientr, 'of', nevents
    fillth1(hMET, chain.MET, 137000*chain.CrossSection/nevents)
    fillth1(hHT, chain.HT, 137000*chain.CrossSection/nevents)
    for igjet, gjet in enumerate(chain.GenJets):
        gpt = gjet.Pt()
        if not gpt>15: continue
        
        for ijet, jet in enumerate(chain.Jets):
            if not gjet.DeltaR(jet)<0.4: continue
            rpt = jet.Pt()
            if undojec: rpt*=1./chain.Jets_jecFactor[ijet]
            if chain.Jets_hadronFlavor[ijet]==5:  fillth2(hResponseVsGenPt_b, rpt, rpt/gpt)
            elif chain.Jets_hadronFlavor[ijet]<5:  fillth2(hResponseVsGenPt_light, rpt, rpt/gpt)                
            for ibinedge, binedge in enumerate(ptrange[:-1]):
                if not gpt>binedge and gpt<ptrange[ibinedge+1]:   
                    binedges = str(binedge)+'to'+str(ptrange[ibinedge+1])
                    if chain.Jets_hadronFlavor[ijet]==5:  fillth1(hresbs[binedges], rpt/gpt)
                    elif chain.Jets_hadronFlavor[ijet]<5: fillth1(hress[binedges], rpt/gpt)                        

                        
                
fnew.cd()
for ibinedge, binedge in enumerate(ptrange[:-1]):
    binedges = str(binedge)+'to'+str(ptrange[ibinedge+1])
    hress[binedges].Write()
    hresbs[binedges].Write()

hResponseVsGenPt_b.Write()
hResponseVsGenPt_light.Write()
hHT.Write()
hMET.Write()
print 'just created', fnew.GetName()
exit(0)
