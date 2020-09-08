import os
'''with a grid proxy:
xrdfs root://hepxrd01.colorado.edu:1094/ ls /store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/scan/
'''

from ROOT import *
from utils import *
from glob import glob
gROOT.SetBatch(1)


isfast = True
isfull = not isfast

do2016 = True
do2017 = not do2016

if do2016: btagcut = 0.6324
if do2017: btagcut = 0.4941
#if is2018: BTAG_deepCSV = 0.4184


dosm = False


if isfast:
    ra2bspace = '/eos/uscms//store/group/lpcsusyhad/SusyRA2Analysis2015/Run2ProductionV17/scan/'
    flist = glob(ra2bspace+'*.root')
    chain = TChain('tree')
    if do2017: 
        if dosm: 
            shortfname = 'Fall17Fast.TTJets_SingleLeptFromT_Tune'
            chain = TChain('TreeMaker2/PreSelection')
            fnamefilename = 'usefulthings/filelistV17.txt'
            fnamefile = open(fnamefilename)
            flist = fnamefile.readlines()
            ra2bspace = 'root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/'
            for iflist in range(len(flist)): flist[iflist] = ra2bspace+flist[iflist]
                        
        else: 
            shortfname = 'T1bbbb_mMother-1500_mLSP-100_MC2017'
            #shortfname = 'T1bbbb_mMother-1800_mLSP-200_MC2017'
    if do2016: 
        if dosm: 
            shortfname = 'Summer16v3Fast.TTJets_SingleLeptFromTbar_Tune'
            chain = TChain('TreeMaker2/PreSelection')
            fnamefilename = 'usefulthings/filelistV17.txt'
            fnamefile = open(fnamefilename)
            flist = fnamefile.readlines()
            ra2bspace = 'root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/'
            for iflist in range(len(flist)): flist[iflist] = ra2bspace+flist[iflist]
        else: 
            filename = 'root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/scan/T1bbbb_mMother-1800_mLSP-200_MC2016_fast.root'
            chain.Add(filename)
            

if isfull:
    chain = TChain('TreeMaker2/PreSelection')
    if do2017: 
        if dosm: shortfname = 'Fall17.TTJets_SingleLeptFromTbar_Tune'
        else: shortfname = 'Fall17.SMS-T1bbbb_mGluino-1500_mLSP-100'
    if do2016: 
        if dosm:
            os.system('xrdfs root://hepxrd01.colorado.edu:1094/ ls /store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/Summer16/TT_TuneCUETP8M2T4_13TeV-powheg-isrup-pythia8_ext1/ > thefiles.txt')
            fflist = open('thefiles.txt')
            lines = fflist.readlines()
            fflist.close()
            for line in lines[:30]:
                filename = 'root://hepxrd01.colorado.edu:1094/'+line.strip()
                chain.Add(filename)
        else: 
            filename = 'root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/Summer16v3/SMS-T1bbbb_mGluino-1500_mLSP-100_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/1_RA2AnalysisTree.root'
            chain.Add(filename)
    #shortfname = 'Fall17.SMS-T1qqqq_mGluino-1400_mLSP-100'
    print 'going to check for ', filename

    


chain.Show(0)

newname = 'btageff.root'

if isfast: newname = newname.replace('.root', '_fast.root')
if isfull: newname = newname.replace('.root', '_full.root')
if do2016: newname = newname.replace('.root', '_2016.root')
if do2017: newname = newname.replace('.root', '_2017.root')

if dosm: newname = newname.replace('.root', '_ST.root')
else: newname = newname.replace('.root', '_T1bbbb.root')

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
hLeadJetPt  = TH1F('hLeadJetPt','hLeadJetPt', 100,0,2000)
histoStyler(hLeadJetPt, kBlack)


hGenBJetPt = TH1F('hGenBJetPt','hGenBJetPt',50,0,1500)
hGenBJetPtMatched = TH1F('hGenBJetPtMatched','hGenBJetPtMatched',50,0,1500)

hGenBJetEta = TH1F('hGenBJetEta','hGenBJetEta', 50,-5,5)

hBTags = TH1F('hBTags','hBTags',4,0,4)

for ientr in range(nevents):
    chain.GetEntry(ientr)
    if ientr%100==0: print 'processing', ientr, 'of', nevents
    fillth1(hMET, chain.MET, 137000*chain.CrossSection/nevents)
    fillth1(hHT, chain.HT, 137000*chain.CrossSection/nevents)
    fillth1(hLeadJetPt, chain.Jets[0].Pt(), 137000*chain.CrossSection/nevents)

    fillth1(hBTags, chain.BTags)
    
    for igjet, gjet in enumerate(chain.GenJets):
        gpt = gjet.Pt()
        if not gpt>15: continue
        if not abs(gjet.Eta())<2.4: continue
        #if not abs(gjet.Eta())<1.4: continue    #####barrel only!
        for ijet, jet in enumerate(chain.Jets):
            if not gjet.DeltaR(jet)<0.4: continue
            if chain.Jets_hadronFlavor[ijet]==5: 
                fillth1(hGenBJetPt, gpt) 
                fillth1(hGenBJetEta, gjet.Eta()) 
                fillth2(hResponseVsGenPt_b, gpt, jet.Pt()/gpt)
                if chain.Jets_bJetTagDeepCSVBvsAll[ijet]>btagcut: 
                    fillth1(hGenBJetPtMatched, gpt)
            elif chain.Jets_hadronFlavor[ijet]<5:  fillth2(hResponseVsGenPt_light, gpt, jet.Pt()/gpt)
            continue
            for ibinedge, binedge in enumerate(ptrange[:-1]):
                if not gpt>binedge and gpt<ptrange[ibinedge+1]:   
                    binedges = str(binedge)+'to'+str(ptrange[ibinedge+1])
                    if chain.Jets_hadronFlavor[ijet]==5:  fillth1(hresbs[binedges], jet.Pt()/gpt)
                    elif chain.Jets_hadronFlavor[ijet]<5: fillth1(hress[binedges], jet.Pt()/gpt)                        

                        
                
fnew.cd()
for ibinedge, binedge in enumerate(ptrange[:-1]):
    binedges = str(binedge)+'to'+str(ptrange[ibinedge+1])
    hress[binedges].Write()
    hresbs[binedges].Write()

hResponseVsGenPt_b.Write()
hResponseVsGenPt_light.Write()
hHT.Write()
hLeadJetPt.Write()
hMET.Write()

hGenBJetPt.Write()
hGenBJetPtMatched.Write()
heff = hGenBJetPtMatched.Clone('hBJetPt'+'_eff')
heff.Divide(hGenBJetPt)
heff.Write()
hGenBJetEta.Write()
hBTags.Write()
print 'just created', fnew.GetName()
exit(0)
