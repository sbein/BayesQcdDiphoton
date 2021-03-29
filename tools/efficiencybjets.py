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


print 'hello?'
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
        print "aaa"
        if dosm: 
            shortfname = 'Summer16v3Fast.TTJets_SingleLeptFromTbar_Tune'
            chain = TChain('TreeMaker2/PreSelection')
            fnamefilename = 'usefulthings/filelistV17.txt'
            fnamefile = open(fnamefilename)
            flist = fnamefile.readlines()
            ra2bspace = 'root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/'
            for iflist in range(len(flist)): flist[iflist] = ra2bspace+flist[iflist]
        else: 
            print "bbb"
            filename = 'root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/scan/T1bbbb_mMother-1800_mLSP-200_MC2016_fast.root'
            filename = 'root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/scan/T1bbbb_mMother-1300_mLSP-1100_MC2016_fast.root'
            filename = 'root://hepxrd01.colorado.edu:1094//store/user/aperloff/SusyRA2Analysis2015/Run2ProductionV17/scan/T2bb_mMother-1000_mLSP-100_MC2016_fast.root'
            print 'adding', filename
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


nevents = min(10000,chain.GetEntries())
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
hLeadJetPt  = TH1F('hLeadJetPt','hLeadJetPt', 50,0,2000)
histoStyler(hLeadJetPt, kBlack)

hLeadGenJetPt  = TH1F('hLeadGenJetPt','hLeadGenJetPt', 50,0,2000)
histoStyler(hLeadGenJetPt, kBlack)


hGenBJetPt = TH1F('hGenBJetPt','hGenBJetPt',50,0,2000)
hGenBJetPtMatched = TH1F('hGenBJetPtMatched','hGenBJetPtMatched',50,0,2000)

hGenBJetPtBarrel = TH1F('hGenBJetPtBarrel','hGenBJetPtBarrel',50,0,2000)
hGenBJetPtBarrelMatched = TH1F('hGenBJetPtBarrelMatched','hGenBJetPtBarrelMatched',50,0,2000)
hGenBJetPtEndcap = TH1F('hGenBJetPtEndcap','hGenBJetPtEndcap',50,0,2000)
hGenBJetPtEndcapMatched = TH1F('hGenBJetPtEndcapMatched','hGenBJetPtEndcapMatched',50,0,2000)

hGenBJetEta = TH1F('hGenBJetEta','hGenBJetEta', 50,-5,5)

hBTags = TH1F('hBTags','hBTags',4,0,4)


hNbFlavor = TH1F('hNbFlavor','hNbFlavor',4,0,4)
hNbParton = TH1F('hNbParton','hNbParton',4,0,4)

for ientr in range(nevents):
    chain.GetEntry(ientr)
    if ientr%100==0: print 'processing', ientr, 'of', nevents
    fillth1(hMET, chain.MET, 137000*chain.CrossSection/nevents)
    fillth1(hHT, chain.HT, 137000*chain.CrossSection/nevents)

    
    if len(chain.Jets)>0:
        fillth1(hLeadJetPt, chain.Jets[0].Pt())

    if chain.MHT>300: fillth1(hBTags, chain.BTags)


    partons = []
    for igen, gp in enumerate(chain.GenParticles):
        if not (abs(chain.GenParticles_PdgId[igen])>500 and abs(chain.GenParticles_PdgId[igen])<600): continue
        partons.append([gp,chain.GenParticles_PdgId[igen]])
    
    nb = 0
    nbcustom = 0
    for ijet, jet in enumerate(chain.Jets):
        if not jet.Pt()>30: continue
        if not abs(jet.Eta())<2.4: continue
        if chain.Jets_partonFlavor[ijet]==5: 
            nb+=1
        flav = -1
        for part in partons:
            if jet.DeltaR(part[0])<0.4:
                flav = abs(part[1])
                break
        print 'found parton', flav
        if flav==5: nbcustom+=1
                
    fillth1(hNbParton,nbcustom)
    fillth1(hNbFlavor, nb)

    continue
    for igjet, gjet in enumerate(chain.GenJets):
        gpt = gjet.Pt()
        if igjet==0: 
            fillth1(hLeadGenJetPt, gpt)
        #continue
        if not gpt>20: continue
        if not abs(gjet.Eta())<2.4: continue
        #if not abs(gjet.Eta())<1.4: continue    #####barrel only!
        for ijet, jet in enumerate(chain.Jets):
            if not gjet.DeltaR(jet)<0.4: continue
            if chain.Jets_partonFlavor[ijet]==5: 
                fillth1(hGenBJetPt, gpt) 
                fillth1(hGenBJetEta, gjet.Eta()) 
                if gpt>30 and gjet.Eta()<2.4: nb+=1
                if abs(gjet.Eta())<1.5: fillth1(hGenBJetPtBarrel, gpt) 
                else: fillth1(hGenBJetPtEndcap, gpt) 
                fillth2(hResponseVsGenPt_b, gpt, jet.Pt()/gpt)
                if chain.Jets_bJetTagDeepCSVBvsAll[ijet]>btagcut: 
                    fillth1(hGenBJetPtMatched, gpt)
                    if abs(gjet.Eta())<1.5: fillth1(hGenBJetPtBarrelMatched, gpt) 
                    else: fillth1(hGenBJetPtEndcapMatched, gpt) 
            elif chain.Jets_partonFlavor[ijet]<5:  fillth2(hResponseVsGenPt_light, gpt, jet.Pt()/gpt)
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

heffB = hGenBJetPtBarrelMatched.Clone('hBJetPt'+'_effBarrel')
heffB.Divide(hGenBJetPtBarrel)
heffB.Write()

heffE = hGenBJetPtEndcapMatched.Clone('hBJetPt'+'_effEndcap')
heffE.Divide(hGenBJetPtEndcap)
heffE.Write()

hGenBJetEta.Write()
hBTags.Write()
hLeadGenJetPt.Write()
hNbFlavor.Write()
hNbParton.Write()
print 'just created', fnew.GetName()
exit(0)
