from ROOT import *
from array import array

tl = TLatex()
tl.SetNDC()
cmsTextFont = 61
extraTextFont = 50
lumiTextSize = 0.6
lumiTextOffset = 0.2
cmsTextSize = 0.75
cmsTextOffset = 0.1
regularfont = 42
originalfont = tl.GetTextFont()
epsi = "#scale[1.3]{#font[122]{e}}"
epsilon = 0.0001

binning = {}
binning['Met']=[45,0,450]
binning['HardMet']=binning['Met']
binning['MetSignificance']=[0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7, 2.8, 2.9, 3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, 3.8, 3.9, 4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7, 4.8, 4.9, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7, 6.8, 6.9, 7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 8.0, 8.1, 8.2, 8.3, 8.4, 8.5, 8.6, 8.7, 8.8, 8.9, 9.0, 9.1, 9.2, 9.3, 9.4, 9.5, 9.6, 9.7, 9.8, 9.9, 10.0, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9, 11.0, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 12.0]
binning['NJets']=[10,0,10]
binning['NLeptons']=[5,0,5]
binning['NElectrons']=binning['NLeptons']
binning['NPhotons']=binning['NLeptons']
binning['NMuons']=binning['NLeptons']
binning['NTags']=[3,0,3]
binning['NPix']=binning['NTags']
binning['NPixStrips']=binning['NTags']
binning['BTags']=[4,0,4]
binning['Ht']=[10,0,2000]
binning['St']=binning['Ht']
binning['MinDPhiHardMetJets'] = [32,0,3.2]
binning['DPhiPhoPho'] = [8,0,3.2]
binning['DPhiGG'] = [8,0,3.2]
binning['DPhiPho1Met'] = [8,0,3.2]
binning['DPhiPho2Met'] = [8,0,3.2]
binning['DPhiPhoMet'] = [8,0,3.2]
binning['DPhi1']=[8,0,3.2]
binning['DPhi2']=[8,0,3.2]
binning['DPhi3']=[8,0,3.2]
binning['DPhi4']=[8,0,3.2]
binning['Track1MassFromDedx'] = [25,0,1000]
binning['BinNumber'] = [34,0,34]
binning['MinDeltaPhi'] = binning['DPhi1']
binning['PhoPt']=[20,0,800]
binning['Pho1Pt']=binning['PhoPt']
binning['Pho2Pt']=binning['PhoPt']

binningUser = dict(binning)
binningUser['HardMet'] = [0,10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160,170,180,200,250,450]
#binningUser['HardMet'] = [15,0,300]
#binningUser['HardMet'] = [30,20,920]

binning_templates = {}
binning_templates['HardMet']=[300,0,600]
binning_templates['HardMet']=[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,100,102,104,106,108,110,112,114,116,118,120,122,124,126,128,130,132,134,136,138,140,142,144,146,148,150,155,160,165,170,175,180,185,190,195,200,220,240,260,280,300,400,500,800]
binning_templates['Met']=binning_templates['HardMet']
binning_templates['MetSignificance']=binning['MetSignificance']
binning_templates['Ht']=[0,300,500,700,1000,1500,2000,10000]
binning_templates['Ht']=[0,200,300,500,700,1000,1500,2000,10000]#NOV2016 removed "400"
binning_templates['Ht']=[1,0,10000]# in delphes, no apparent dependence of gen-MHT on HT
binning_templates['St']=binning['Ht']
binning_templates['NJets']=[10,0,10]
binning_templates['BTags']=[0,1,2,5]
binning_templates['Jet1Pt']=[20,0,800]
binning_templates['Jet1Eta']=[20,-3,3]
binning_templates['Jet2Pt']=[20,0,800]
binning_templates['Jet2Eta']=[20,-3,3]
binning_templates['Jet3Pt']=[20,0,800]
binning_templates['Jet3Eta']=[20,-3,3]
binning_templates['Jet4Pt']=[20,0,800]
binning_templates['Jet4Eta']=[20,-3,3]
binning_templates['DPhi1']=[126,0,3.15]
#binning_templates['DPhi1']=[126,-3.15,3.15]
binning_templates['DPhi2']=binning_templates['DPhi1']
binning_templates['DPhi3']=binning_templates['DPhi1']
binning_templates['DPhi4']=binning_templates['DPhi1']
binning_templates['MaxHemJetPt']=[20,0,100]
binning_templates['DPhiPhoPho'] = [16,0,3.2]


def histoStyler(h,color=kBlack):
    h.SetLineWidth(2)
    h.SetLineColor(color)
    h.SetMarkerColor(color)
    #h.SetFillColor(color)
    size = 0.059
    font = 132
    h.GetXaxis().SetLabelFont(font)
    h.GetYaxis().SetLabelFont(font)
    h.GetXaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleFont(font)
    h.GetYaxis().SetTitleSize(size)
    h.GetXaxis().SetTitleSize(size)
    h.GetXaxis().SetLabelSize(size)   
    h.GetYaxis().SetLabelSize(size)
    h.GetXaxis().SetTitleOffset(1.0)
    h.GetYaxis().SetTitleOffset(1.05)
    if not h.GetSumw2N(): h.Sumw2()

def makeHist(name, title, nb, low, high, color):
    h = TH1F(name,title,nb,low,high)
    histoStyler(h,color)
    return h

def makeTh1(name, title, nbins, low, high, color=kBlack): 
    h = TH1F(name, title, nbins, low, high)
    histoStyler(h, color)
    return h


def makeTh1VB(name, title, nbins, arrayOfBins): 
    h = TH1F(name, title, nbins, np.asarray(arrayOfBins, 'd'))
    histoStyler(h, 1)
    return h

def makeTh2(name, title, nbinsx, lowx, highx, nbinsy, lowy, highy): 
    h = TH2F(name, title, nbinsx, lowx, highx, nbinsy, lowy, highy)
    histoStyler(h)
    return h

def makeTh2VB(name, title, nbinsx, arrayOfBinsx, nbinsy, arrayOfBinsy):
    h = TH2F(name, title, nbinsx, np.asarray(arrayOfBinsx, 'd'), nbinsy, np.asarray(arrayOfBinsy, 'd'))
    histoStyler(h)
    return h

def graphStyler(g,color):
    g.SetLineWidth(2)
    g.SetLineColor(color)
    g.SetMarkerColor(color)
    #g.SetFillColor(color)
    size = 0.055
    font = 132
    g.GetXaxis().SetLabelFont(font)
    g.GetYaxis().SetLabelFont(font)
    g.GetXaxis().SetTitleFont(font)
    g.GetYaxis().SetTitleFont(font)
    g.GetYaxis().SetTitleSize(size)
    g.GetXaxis().SetTitleSize(size)
    g.GetXaxis().SetLabelSize(size)   
    g.GetYaxis().SetLabelSize(size)
    g.GetXaxis().SetTitleOffset(1.0)
    g.GetYaxis().SetTitleOffset(1.05)

def mkcanvas(name='c1'):
    c1 = TCanvas(name,name,750,630)
    c1.SetBottomMargin(.15)
    c1.SetLeftMargin(.14)
    #c1.SetTopMargin(.13)
    #c1.SetRightMargin(.04)
    return c1

def mkcanvas_wide(name):
    c1 = TCanvas(name,name,1200,700)
    c1.Divide(2,1)
    c1.GetPad(1).SetBottomMargin(.14)
    c1.GetPad(1).SetLeftMargin(.14)
    c1.GetPad(2).SetBottomMargin(.14)
    c1.GetPad(2).SetLeftMargin(.14)    
    c1.GetPad(1).SetGridx()
    c1.GetPad(1).SetGridy()
    c1.GetPad(2).SetGridx()
    c1.GetPad(2).SetGridy()    
    #c1.SetTopMargin(.13)
    #c1.SetRightMargin(.04)
    return c1

def mklegend(x1=.22, y1=.66, x2=.69, y2=.82, color=kWhite):
    lg = TLegend(x1, y1, x2, y2)
    lg.SetFillColor(color)
    lg.SetTextFont(42)
    lg.SetBorderSize(0)
    lg.SetShadowColor(kWhite)
    lg.SetFillStyle(0)
    return lg

def mklegend_(x1=.22, y1=.66, x2=.69, y2=.82, color=kWhite):
    lg = TLegend(x1, y1, x2, y2)
    lg.SetFillColor(color)
    lg.SetTextFont(42)
    lg.SetBorderSize(0)
    lg.SetShadowColor(kWhite)
    lg.SetFillStyle(0)
    return lg

def fillth1(h,x,weight=1):
    h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon),weight)

def fillth2(h,x,y,weight=1):
    h.Fill(min(max(x,h.GetXaxis().GetBinLowEdge(1)+epsilon),h.GetXaxis().GetBinLowEdge(h.GetXaxis().GetNbins()+1)-epsilon), min(max(y,h.GetYaxis().GetBinLowEdge(1)+epsilon),h.GetYaxis().GetBinLowEdge(h.GetYaxis().GetNbins()+1)-epsilon),weight)

def findbin(thebins, value):
    for bin in thebins:
        if value>=bin[0] and value<=bin[1]:
            return bin
    if value>thebins[-1]: return thebins[-1]
    if value<thebins[0]: return thebins[0]	


def namewizard(name):
    if 'HardMet' == name:
        return r'E_{T}^{miss} [GeV]'
    if 'Met' == name:
        return r'E_{T}^{miss} [GeV]'
    if 'Ht' == name:
        return r'H_{T} [GeV]'
    if 'NJets' == name:
        return r'n_{j}'        
    if 'BTags' == name:
        return r'n_{b}'                
    if 'MinDPhiHardMetJets' == name:
        return r'#Delta#phi_{min}'                        
    if 'NLeptons' == name:
        return r'n_{#ell}'
    if 'NPhotons' == name:
        return r'n_{#gamma}'		
    if 'NMuons' == name:
        return r'n(#mu)'
    if 'NTags' == name:
        return r'n_{DT}'
    if 'SumTagPtOverMet' == name:
        return r'R^{*}'
    if 'DPhiMetSumTags' == name:
        return r'#Delta#phi^{*}'
    if 'St' == name:
        return r'H_{T}'
    name = name.replace('.ZGGToNuNuGG',' Z#gamma#gamma,Z#rightarrow#nu#nu')
    name = name.replace('.WGJets_MonoPhoton',' W#gamma,W#rightarrow e#nu')    
    return name


def Struct(*args, **kwargs):
    def init(self, *iargs, **ikwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)
        for i in range(len(iargs)):
            setattr(self, args[i], iargs[i])
        for k,v in ikwargs.items():
            setattr(self, k, v)

    name = kwargs.pop("name", "MyStruct")
    kwargs.update(dict((k, None) for k in args))
    return type(name, (object,), {'__init__': init, '__slots__': kwargs.keys()})



def mkHistoStruct(hname, binning):
    if '_' in hname: var = hname[hname.find('_')+1:]
    else: var =  hname
    histoStruct = Struct('Branch','Observed','GenSmeared','Gen','Rebalanced','RplusS')
    if len(binning[var])==3:
        nbins = binning[var][0]
        low = binning[var][1]
        high = binning[var][2]
        histoStruct.Branch = TH1F('h'+hname+'Branch',hname+'Branch',nbins,low,high)
        histoStruct.Observed = TH1F('h'+hname+'Observed',hname+'Observed',nbins,low,high)
        histoStruct.GenSmeared = TH1F('h'+hname+'GenSmeared',hname+'GenSmeared',nbins,low,high)
        histoStruct.Gen = TH1F('h'+hname+'Gen',hname+'Gen',nbins,low,high)
        histoStruct.Rebalanced = TH1F('h'+hname+'Rebalanced',hname+'Rebalanced',nbins,low,high)
        histoStruct.RplusS = TH1F('h'+hname+'RplusS',hname+'RplusS',nbins,low,high)
    else:
        nBin = len(binning[var])-1
        binArr = array('d',binning[var])
        histoStruct.Branch = TH1F('h'+hname+'Branch',hname+'Branch',nBin,binArr)
        histoStruct.Observed = TH1F('h'+hname+'Observed',hname+'Observed',nBin,binArr)
        histoStruct.GenSmeared = TH1F('h'+hname+'GenSmeared',hname+'GenSmeared',nBin,binArr)
        histoStruct.Gen = TH1F('h'+hname+'Gen',hname+'Gen',nBin,binArr)
        histoStruct.Rebalanced = TH1F('h'+hname+'Rebalanced',hname+'Rebalanced',nBin,binArr)
        histoStruct.RplusS = TH1F('h'+hname+'RplusS',hname+'RplusS',nBin,binArr)
    histoStyler(histoStruct.Branch,kRed)
    histoStyler(histoStruct.Observed,kRed)
    histoStyler(histoStruct.GenSmeared,kBlack)
    histoStyler(histoStruct.Gen,kGreen)
    histoStyler(histoStruct.Rebalanced,kBlue)
    histoStyler(histoStruct.RplusS,kBlack)
    return histoStruct

def writeHistoStruct(hStructDict):
    for key in hStructDict:
        #print 'writing histogram structure:', key
        hStructDict[key].Branch.Write()
        hStructDict[key].Observed.Write()
        hStructDict[key].GenSmeared.Write()
        hStructDict[key].Gen.Write()
        hStructDict[key].Rebalanced.Write()
        hStructDict[key].RplusS.Write()


def pause(str_='push enter key when ready'):
        import sys
        print str_
        sys.stdout.flush() 
        raw_input('')

def mkmet(metPt, metPhi):
    met = TLorentzVector()
    met.SetPtEtaPhiE(metPt, 0, metPhi, metPt)
    return met


datamc = 'Data'
def stamp(lumi='35.9', showlumi = False, WorkInProgress = True):    
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(0.98*tl.GetTextSize())
    tl.DrawLatex(0.135,0.915, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.SetTextSize(1.0/0.98*tl.GetTextSize())
    xlab = 0.213
    if WorkInProgress: tl.DrawLatex(xlab,0.915, ' Work in progress')
    else: tl.DrawLatex(xlab,0.915, ('MC' in datamc)*' simulation ')
    tl.SetTextFont(regularfont)
    tl.SetTextSize(0.81*tl.GetTextSize())    
    thingy = ''
    if showlumi: thingy+='#sqrt{s}=13 TeV ('+str(lumi)+' fb^{-1})'
    xthing = 0.6202
    if not showlumi: xthing+=0.13
    tl.DrawLatex(xthing,0.915,thingy)
    tl.SetTextSize(1.0/0.81*tl.GetTextSize())  

def stamp2(lumi,datamc='MC'):
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(1.6*tl.GetTextSize())
    tl.DrawLatex(0.152,0.82, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.DrawLatex(0.14,0.74, ('MC' in datamc)*' simulation'+' internal')
    tl.SetTextFont(regularfont)
    if lumi=='': tl.DrawLatex(0.62,0.82,'#sqrt{s} = 13 TeV')
    else: tl.DrawLatex(0.47,0.82,'#sqrt{s} = 13 TeV, L = '+str(lumi)+' fb^{-1}')
    #tl.DrawLatex(0.64,0.82,'#sqrt{s} = 13 TeV')#, L = '+str(lumi)+' fb^{-1}')	
    tl.SetTextSize(tl.GetTextSize()/1.6)

def calcTrackIso(trk, tracks):
    ptsum =  -trk.pt()
    for track in tracks:
        dR = TMath.Sqrt( (trk.eta()-track.eta())**2 + (trk.phi()-track.phi())**2)
        if dR<0.3: ptsum+=track.pt()
    return ptsum/trk.pt()

def calcTrackJetIso(trk, jets):
    for jet in jets:
        if not jet.pt()>30: continue
        if  TMath.Sqrt( (trk.eta()-jet.eta())**2 + (trk.phi()-jet.phi())**2)<0.5: return False
    return True

'''
def calcMiniIso(trk, tracks):
    pt = trk.pt()
    ptsum = -pt
    if pt<=50: R = 0.2
    elif pt<=200: R = 10.0/pt
    else: R = 0.05
    for track in tracks:
        dR = TMath.Sqrt( (trk.eta()-track.eta())**2 + (trk.phi()-track.phi())**2)
        if dR<R: ptsum+=track.pt()
    return ptsum/trk.pt()


def calcSumPt(jets, obj, conesize=0.6, thresh=10):
    sumpt_ = 0
    for jet in jets:
        if not jet.Pt()>thresh:
            continue
        if not (obj.DeltaR(jet)<conesize):
            continue
        sumpt_+=jet.Pt()
    return sumpt_	


def getDPhis(metvec,jetvec):
    dphilist = []
    for j in range(4):
        try:dphilist.append(abs(metvec.DeltaPhi(jetvec[j].tlv)))
        except: dphilist.append(-5)
    return dphilist

def isMatched(obj, col, dR=0.02, verbose = False):
    matchedIdx = -1
    bigDR = inf
    for ic, thing in enumerate(col):
        dr = thing.DeltaR(obj)
        if verbose: print 'dr=',dr
        if dr<dR:
            ismatched = True
            return thing
    return False

def isMatched_(obj, col, dR=0.02, verbose = False):
    matchedIdx = -1
    bigDR = inf
    for ic, thing in enumerate(col):
        dr = thing[0].DeltaR(obj[0])
        if verbose: print 'dr=',dr
        if dr<dR:
            ismatched = True
            return thing
    return False

def getLeadingGenBJet(GenJets, RecoJets, BTAG_CSV):
    for gjet in GenJets:
        for rjet in RecoJets:
            dR_ = gjet.tlv.DeltaR(rjet.tlv)
            if dR_<0.4 and rjet.csv>BTAG_CSV: return gjet
    emptyvec = UsefulJet()
    return emptyvec

def getLeadingBJet(RecoJets, CsvVec, BTAG_CSV):
    for ireco in range(len(RecoJets)):
        if not RecoJets[ireco].Pt()>30: continue
        if CsvVec[ireco]>BTAG_CSV: return [ireco,RecoJets[ireco]]
    emptyvec = TLorentzVector()
    return [-1,emptyvec]
'''




def FabDraw(cGold,leg,hTruth,hComponents,datamc='MC',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
    cGold.cd()
    pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
    pad1.SetBottomMargin(0.0)
    pad1.SetLeftMargin(0.12)
    if not LinearScale:
        pad1.SetLogy()

    pad1.SetGridx()
    #pad1.SetGridy()
    pad1.Draw()
    pad1.cd()
    for ih in range(1,len(hComponents[1:])+1):
        hComponents[ih].Add(hComponents[ih-1])
    hComponents.reverse()        
    if abs(hComponents[0].Integral(-1,999)-1)<0.001:
        hComponents[0].GetYaxis().SetTitle('Normalized')
    else: hComponents[0].GetYaxis().SetTitle('Events/bin')
    cGold.Update()
    hTruth.GetYaxis().SetTitle('Normalized')
    hTruth.GetYaxis().SetTitleOffset(1.15)
    hTruth.SetMarkerStyle(20)
    histheight = 1.5*max(hComponents[0].GetMaximum(),hTruth.GetMaximum())
    if LinearScale: low, high = 0, histheight
    else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hTruth.GetMinimum())), 1000*histheight

    title0 = hTruth.GetTitle()
    if datamc=='MC':
        for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
        leg.AddEntry(hTruth,hTruth.GetTitle(),'lpf')        
    else:
        for ihComp, hComp in enumerate(hComponents):
            leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
        leg.AddEntry(hTruth,title0,'lp')    
    hTruth.SetTitle('')
    hComponents[0].SetTitle('')
    if LinearScale: hComponents[0].GetYaxis().SetRangeUser(0, 1.5*hTruth.GetMaximum())
    else: hComponents[0].GetYaxis().SetRangeUser(0.001, 100*hTruth.GetMaximum())
    hComponents[0].Draw('hist')

    for h in hComponents[1:]: 
        h.Draw('hist same')
        cGold.Update()
        print 'updating stack', h
    hComponents[0].Draw('same') 
    hTruth.Draw('p same')
    hTruth.Draw('e same')    
    cGold.Update()
    hComponents[0].Draw('axis same')           
    leg.Draw()        
    cGold.Update()
    stamp2(lumi,datamc)
    cGold.Update()
    cGold.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.3)
    pad2.SetLeftMargin(0.12)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    hTruthCopy = hTruth.Clone('hTruthClone'+hComponents[0].GetName())
    hRatio = hTruthCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
    hRatio.SetMarkerStyle(20)
    #hFracDiff = hComponents[0].Clone('hFracDiff')
    #hFracDiff.SetMarkerStyle(20)
    hTruthCopy.SetMarkerStyle(20)
    hTruthCopy.SetMarkerColor(1) 
    #histoStyler(hFracDiff, 1)
    histoStyler(hTruthCopy, 1)
    #hFracDiff.Add(hTruthCopy,-1)
    #hFracDiff.Divide(hTruthCopy)
    #hRatio.Divide(hTruthCopy)
    hRatio.Divide(hComponents[0])
    hRatio.GetYaxis().SetRangeUser(0.0,.1)###
    hRatio.SetTitle('')
    if 'prediction' in title0: hFracDiff.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
    else: hRatio.GetYaxis().SetTitle(fractionthing)
    hRatio.GetXaxis().SetTitleSize(0.12)
    hRatio.GetXaxis().SetLabelSize(0.11)
    hRatio.GetYaxis().SetTitleSize(0.12)
    hRatio.GetYaxis().SetLabelSize(0.12)
    hRatio.GetYaxis().SetNdivisions(5)
    hRatio.GetXaxis().SetNdivisions(10)
    hRatio.GetYaxis().SetTitleOffset(0.5)
    hRatio.GetXaxis().SetTitleOffset(1.0)
    hRatio.GetXaxis().SetTitle(hTruth.GetXaxis().GetTitle())
    hRatio.Draw()
    hRatio.Draw('e0')    
    pad1.cd()
    hComponents.reverse()
    hTruth.SetTitle(title0)
    return hRatio, [pad1, pad2]



'''
def FabDraw(cGold,leg,hObserved,hComponents,datamc='mc',lumi='arbitrary', title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
    cGold.cd()
    pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
    pad1.SetBottomMargin(0.0)
    pad1.SetLeftMargin(0.12)
    if not LinearScale:
        pad1.SetLogy()

    pad1.SetGridx()
    #pad1.SetGridy()
    pad1.Draw()
    pad1.cd()
    for ih in range(1,len(hComponents[1:])+1):
        hComponents[ih].Add(hComponents[ih-1])
    hComponents.reverse()        
    if abs(hComponents[0].Integral(-1,999)-1)<0.001:
        hComponents[0].GetYaxis().SetTitle('Normalized')
    else: hComponents[0].GetYaxis().SetTitle('Events/GeV')
    cGold.Update()
    hObserved.GetYaxis().SetTitle('Normalized')
    hObserved.GetYaxis().SetTitleOffset(1.15)
    hObserved.SetMarkerStyle(20)
    histheight = 1.5*max(hComponents[0].GetMaximum(),hObserved.GetMaximum())
    if LinearScale: low, high = 0, histheight
    else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hObserved.GetMinimum())), 1000*histheight

    title0 = hObserved.GetTitle()
    if datamc=='MC':
        for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
        leg.AddEntry(hObserved,hObserved.GetTitle(),'lpf')        
    else:
        for ihComp, hComp in enumerate(hComponents):
            leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
        leg.AddEntry(hObserved,title0,'lp')    
    hObserved.SetTitle('')
    hComponents[0].SetTitle('')	
    hComponents[0].Draw('hist')
    for h in hComponents[1:]: 
        h.Draw('hist same')
        cGold.Update()
        print 'updating stack', h
    hComponents[0].Draw('same') 
    hObserved.Draw('p same')
    hObserved.Draw('e same')    
    cGold.Update()
    hComponents[0].Draw('axis same')           
    leg.Draw()        
    cGold.Update()
    stampFab(lumi,datamc)
    cGold.Update()
    cGold.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.3)
    pad2.SetLeftMargin(0.12)
    pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    hObservedCopy = hObserved.Clone('hObservedClone'+hComponents[0].GetName())
    hRatio = hObservedCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
    hRatio.SetMarkerStyle(20)
    #hFracDiff = hComponents[0].Clone('hFracDiff')
    #hFracDiff.SetMarkerStyle(20)
    hObservedCopy.SetMarkerStyle(20)
    hObservedCopy.SetMarkerColor(1) 
    #histoStyler(hFracDiff, 1)
    histoStyler(hObservedCopy, 1)
    #hFracDiff.Add(hObservedCopy,-1)
    #hFracDiff.Divide(hObservedCopy)
    #hRatio.Divide(hObservedCopy)
    hRatio.Divide(hComponents[0])
    hRatio.GetYaxis().SetRangeUser(0.0,.1)###
    hRatio.SetTitle('')
    if 'prediction' in title0: hFracDiff.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
    else: hRatio.GetYaxis().SetTitle(fractionthing)
    hRatio.GetXaxis().SetTitleSize(0.12)
    hRatio.GetXaxis().SetLabelSize(0.11)
    hRatio.GetYaxis().SetTitleSize(0.12)
    hRatio.GetYaxis().SetLabelSize(0.12)
    hRatio.GetYaxis().SetNdivisions(5)
    hRatio.GetXaxis().SetNdivisions(10)
    hRatio.GetYaxis().SetTitleOffset(0.5)
    hRatio.GetXaxis().SetTitleOffset(1.0)
    hRatio.GetXaxis().SetTitle(hObserved.GetXaxis().GetTitle())
    hRatio.Draw()
    hRatio.Draw('e0')    
    pad1.cd()
    hComponents.reverse()
    hObserved.SetTitle(title0)
    return hRatio
'''


def FabDrawSystyRatio(cGold,leg,hTruth,hComponents,datamc='MC',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
    cGold.cd()
    pad1 = TPad("pad1", "pad1", 0, 0.45, 1, 1.0)
    pad1.SetBottomMargin(0.0)
    pad1.SetLeftMargin(0.12)
    if not LinearScale:
        pad1.SetLogy()

    #pad1.SetGridx()
    #pad1.SetGridy()
    pad1.Draw()
    pad1.cd()
    for ih in range(1,len(hComponents[1:])+1):
        hComponents[ih].Add(hComponents[ih-1])
    hComponents.reverse()        
    if abs(hComponents[0].Integral(-1,999)-1)<0.001:
        hComponents[0].GetYaxis().SetTitle('Normalized')
    else: hComponents[0].GetYaxis().SetTitle('Events/bin')
    cGold.Update()
    hTruth.GetYaxis().SetTitle('Normalized')
    hTruth.GetYaxis().SetTitleOffset(1.2)
    hTruth.SetMarkerStyle(20)
    histheight = 1.5*max(hComponents[0].GetMaximum(),hTruth.GetMaximum())
    if LinearScale: low, high = 0, histheight
    else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hTruth.GetMinimum())), 1000*histheight

    title0 = hTruth.GetTitle()
    if datamc=='MC':
        for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
        leg.AddEntry(hTruth,hTruth.GetTitle(),'p')        
    else:
        for ihComp, hComp in enumerate(hComponents):
            leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
        leg.AddEntry(hTruth,title0,'p')    
    hTruth.SetTitle('')
    hComponents[0].SetTitle('')	
    xax = hComponents[0].GetXaxis()
    hComponentsUp = hComponents[0].Clone(hComponents[0].GetName()+'UpVariation')
    hComponentsUp.SetLineColor(kWhite)	
    hComponentsDown = hComponents[0].Clone(hComponents[0].GetName()+'DownVariation')	
    hComponentsDown.SetFillColor(10)
    hComponentsDown.SetFillStyle(1001)
    hComponentsDown.SetLineColor(kWhite)
    for ibin in range(1, xax.GetNbins()+1):
        hComponentsUp.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)+hComponents[0].GetBinError(ibin))
        hComponentsDown.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)-hComponents[0].GetBinError(ibin))		

    hComponentsUp.GetYaxis().SetTitleSize(0.11)
    hComponentsUp.GetYaxis().SetTitleOffset(0.5)
    hComponentsUp.GetYaxis().SetLabelSize(0.095)
    #hComponentsUp.Draw('hist')
    hComponents[0].SetLineColor(kGray+1)
    hComponents[0].SetLineWidth(2)
    hComponents[0].Draw('hist e')
    #hComponentsDown.Draw('hist same')
    for h in hComponents[1:]: 
        #h.SetFillStyle(3244)
        print 'there are actually components here!'
        h.Draw('hist same')
    ErrorHistogram = hComponents[0].Clone('ErrorHistogram')
    ErrorHistogram.SetFillStyle(3244)
    ErrorHistogram.SetFillColor(kGray)
    ErrorHistogram.Draw('e2 sames')		
    cGold.Update()
    #hComponents[0].Draw('same') 
    hTruth.Draw('p same')
    hTruth.Draw('e same')    
    cGold.Update()
    hComponents[0].Draw('axis same')           
    leg.Draw()        
    cGold.Update()
    stampFab(lumi,datamc)
    cGold.Update()
    cGold.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.45)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.3)
    pad2.SetLeftMargin(0.12)
    #pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    hTruthCopy = hTruth.Clone('hTruthClone'+hComponents[0].GetName())
    hRatio = hTruthCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
    hRatio.SetMarkerStyle(20)
    #hFracDiff = hComponents[0].Clone('hFracDiff')
    #hFracDiff.SetMarkerStyle(20)
    hTruthCopy.SetMarkerStyle(20)
    hTruthCopy.SetMarkerColor(1) 
    #histoStyler(hFracDiff, 1)
    histoStyler(hTruthCopy, 1)
    #hFracDiff.Add(hTruthCopy,-1)
    #hFracDiff.Divide(hTruthCopy)
    #hRatio.Divide(hTruthCopy)
    histoByWhichToDivide = hComponents[0].Clone()
    for ibin in range(1, xax.GetNbins()+1): histoByWhichToDivide.SetBinError(ibin, 0)
    hRatio.Divide(histoByWhichToDivide)
    hRatio.GetYaxis().SetRangeUser(0.0,.1)###
    hRatio.SetTitle('')
    if 'prediction' in title0: hFracDiff.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
    else: hRatio.GetYaxis().SetTitle(fractionthing)
    hRatio.GetXaxis().SetTitleSize(0.13)
    hRatio.GetXaxis().SetLabelSize(0.13)
    hRatio.GetYaxis().SetTitleSize(0.13)
    hRatio.GetYaxis().SetLabelSize(0.13)
    hRatio.GetYaxis().SetNdivisions(5)
    hRatio.GetXaxis().SetNdivisions(10)
    hRatio.GetYaxis().SetTitleOffset(0.4)
    hRatio.GetXaxis().SetTitleOffset(1.0)
    hRatio.GetXaxis().SetTitle(hTruth.GetXaxis().GetTitle())
    hRatio.Draw()


    histoMethodFracErrorNom = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystNom')
    histoMethodFracErrorNom.SetLineColor(kBlack)
    histoMethodFracErrorNom.SetFillStyle(1)
    histoMethodFracErrorUp = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystUp')
    histoMethodFracErrorUp.SetFillStyle(3001)
    histoMethodFracErrorUp.SetLineColor(kWhite)	
    histoMethodFracErrorUp.SetFillColor(kGray)#hComponents[0].GetFillColor())	
    histoMethodFracErrorUp.SetFillStyle(3244)
    histoMethodFracErrorDown = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystDown')
    histoMethodFracErrorDown.SetLineColor(kWhite)
    #histoMethodFracErrorDown.SetFillStyle(1001)
    histoMethodFracErrorDown.SetFillColor(10)
    for ibin in range(1, xax.GetNbins()+1): 
        content = histoMethodFracErrorUp.GetBinContent(ibin)
        if content>0: err = histoMethodFracErrorUp.GetBinError(ibin)/content
        else: err = 0
        histoMethodFracErrorUp.SetBinContent(ibin, 1+err)
        histoMethodFracErrorUp.SetBinError(ibin, 0)
        histoMethodFracErrorDown.SetBinContent(ibin, 1-err)
        histoMethodFracErrorDown.SetBinError(ibin, 0)		
        histoMethodFracErrorNom.SetBinContent(ibin, 1)		
        histoMethodFracErrorNom.SetBinError(ibin, 0)
    hRatio.GetYaxis().SetRangeUser(-0.2,2.7)	
    hRatio.Draw('e0')
    histoMethodFracErrorUp.Draw('same hist')	
    histoMethodFracErrorNom.Draw('same')
    histoMethodFracErrorDown.Draw('same hist')
    hRatio.Draw('e0 same')
    hRatio.Draw('axis same')
    pad1.cd()
    hComponents.reverse()
    hTruth.SetTitle(title0)
    pad1.Update()

    return hRatio, [histoMethodFracErrorNom, histoMethodFracErrorUp, histoMethodFracErrorDown, hComponentsUp, hComponentsDown, ErrorHistogram,pad1, pad2]

def FabDrawSystyRatio(cGold,leg,hObserved,hComponents,datamc='mc',lumi=35.9, title = '', LinearScale=False, fractionthing='(bkg-obs)/obs'):
    cGold.cd()
    pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
    pad1.SetBottomMargin(0.0)
    pad1.SetLeftMargin(0.12)
    if not LinearScale:
        pad1.SetLogy()

    #pad1.SetGridx()
    #pad1.SetGridy()
    pad1.Draw()
    pad1.cd()
    for ih in range(1,len(hComponents[1:])+1):
        hComponents[ih].Add(hComponents[ih-1])
    hComponents.reverse()        
    if abs(hComponents[0].Integral(-1,999)-1)<0.001:
        hComponents[0].GetYaxis().SetTitle('Normalized')
    else: hComponents[0].GetYaxis().SetTitle('Events/bin')
    cGold.Update()
    hObserved.GetYaxis().SetTitle('Normalized')
    hObserved.GetYaxis().SetTitleOffset(1.15)
    hObserved.SetMarkerStyle(20)
    histheight = 1.5*max(hComponents[0].GetMaximum(),hObserved.GetMaximum())
    if LinearScale: low, high = 0, histheight
    else: low, high = max(0.001,max(hComponents[0].GetMinimum(),hObserved.GetMinimum())), 1000*histheight

    title0 = hObserved.GetTitle()
    if datamc=='MC':
        for hcomp in hComponents: leg.AddEntry(hcomp,hcomp.GetTitle(),'lf')
        leg.AddEntry(hObserved,hObserved.GetTitle(),'lpf')        
    else:
        for ihComp, hComp in enumerate(hComponents):
            leg.AddEntry(hComp, hComp.GetTitle(),'lpf')      
        leg.AddEntry(hObserved,title0,'lp')    
    hObserved.SetTitle('')
    hComponents[0].SetTitle('')	
    xax = hComponents[0].GetXaxis()
    hComponentsUp = hComponents[0].Clone(hComponents[0].GetName()+'UpVariation')
    hComponentsUp.SetLineColor(kWhite)	
    hComponentsDown = hComponents[0].Clone(hComponents[0].GetName()+'DownVariation')	
    hComponentsDown.SetFillColor(10)
    hComponentsDown.SetFillStyle(1001)
    hComponentsDown.SetLineColor(kWhite)
    for ibin in range(1, xax.GetNbins()+1):
        hComponentsUp.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)+hComponents[0].GetBinError(ibin))
        hComponentsDown.SetBinContent(ibin, hComponents[0].GetBinContent(ibin)-hComponents[0].GetBinError(ibin))		

    hComponents[0].Draw('hist e1')
    #hComponentsUp.Draw('hist')
    #hComponentsDown.Draw('hist same')
    for h in hComponents[1:]: 
        print 'there are actually components here!'
        h.Draw('hist same')
        cGold.Update()
        print 'updating stack', h
    #hComponents[0].Draw('same') 
    hError = hComponents[0].Clone(hComponents[0].GetName()+'_err')
    hError.SetFillStyle(3244)
    hError.SetFillColor(kRed)    
    hError.Draw("E2 sames")
    hObserved.Draw('p same')
    hObserved.Draw('e same')    
    cGold.Update()
    hComponents[0].Draw('axis same')           
    leg.Draw()        
    cGold.Update()
    stampFab(lumi,datamc)
    cGold.Update()
    cGold.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
    pad2.SetTopMargin(0.0)
    pad2.SetBottomMargin(0.3)
    pad2.SetLeftMargin(0.12)
    #pad2.SetGridx()
    pad2.SetGridy()
    pad2.Draw()
    pad2.cd()
    hObservedCopy = hObserved.Clone('hObservedClone'+hComponents[0].GetName())
    hRatio = hObservedCopy.Clone('hRatioClone')#hComponents[0].Clone('hRatioClone')#+hComponents[0].GetName()+'testing
    hRatio.SetMarkerStyle(20)
    #hFracDiff = hComponents[0].Clone('hFracDiff')
    #hFracDiff.SetMarkerStyle(20)
    hObservedCopy.SetMarkerStyle(20)
    hObservedCopy.SetMarkerColor(1) 
    #histoStyler(hFracDiff, 1)
    histoStyler(hObservedCopy, 1)
    #hFracDiff.Add(hObservedCopy,-1)
    #hFracDiff.Divide(hObservedCopy)
    #hRatio.Divide(hObservedCopy)
    histoByWhichToDivide = hComponents[0].Clone()
    for ibin in range(1, xax.GetNbins()+1): histoByWhichToDivide.SetBinError(ibin, 0)
    hRatio.Divide(histoByWhichToDivide)
    hRatio.GetYaxis().SetRangeUser(0.0,.1)###
    hRatio.SetTitle('')
    if 'prediction' in title0: hFracDiff.GetYaxis().SetTitle('(RS-#Delta#phi)/#Delta#phi')
    else: hRatio.GetYaxis().SetTitle(fractionthing)
    hRatio.GetXaxis().SetTitleSize(0.12)
    hRatio.GetXaxis().SetLabelSize(0.11)
    hRatio.GetYaxis().SetTitleSize(0.12)
    hRatio.GetYaxis().SetLabelSize(0.12)
    hRatio.GetYaxis().SetNdivisions(5)
    hRatio.GetXaxis().SetNdivisions(10)
    hRatio.GetYaxis().SetTitleOffset(0.5)
    hRatio.GetXaxis().SetTitleOffset(1.0)
    hRatio.GetXaxis().SetTitle(hObserved.GetXaxis().GetTitle())
    hRatio.Draw()


    histoMethodFracErrorNom = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystNom')
    histoMethodFracErrorNom.SetLineColor(kBlack)
    histoMethodFracErrorNom.SetFillStyle(1)
    histoMethodFracErrorUp = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystUp')
    histoMethodFracErrorUp.SetFillStyle(3001)
    histoMethodFracErrorUp.SetLineColor(kWhite)	
    histoMethodFracErrorUp.SetFillColor(hComponents[0].GetFillColor())	
    histoMethodFracErrorDown = hComponents[0].Clone(hComponents[0].GetName()+'hMethodSystDown')
    histoMethodFracErrorDown.SetLineColor(kWhite)
    #histoMethodFracErrorDown.SetFillStyle(1001)
    histoMethodFracErrorDown.SetFillColor(10)
    for ibin in range(1, xax.GetNbins()+1): 
        content = histoMethodFracErrorUp.GetBinContent(ibin)
        if content>0: err = histoMethodFracErrorUp.GetBinError(ibin)/content
        else: err = 0
        histoMethodFracErrorUp.SetBinContent(ibin, 1+err)
        histoMethodFracErrorUp.SetBinError(ibin, 0)
        histoMethodFracErrorDown.SetBinContent(ibin, 1-err)
        histoMethodFracErrorDown.SetBinError(ibin, 0)		
        histoMethodFracErrorNom.SetBinContent(ibin, 1)		
        histoMethodFracErrorNom.SetBinError(ibin, 0)
    hRatio.GetYaxis().SetRangeUser(-0.2,3.2)	
    hRatio.Draw('e0')    
    histoMethodFracErrorUp.Draw('same hist')	
    histoMethodFracErrorNom.Draw('same')
    histoMethodFracErrorDown.Draw('same hist')
    hRatio.Draw('e0 same')
    hRatio.Draw('axis same')
    pad1.cd()
    hComponents.reverse()
    hObserved.SetTitle(title0)
    pad1.Update()

    return hRatio, [histoMethodFracErrorNom, histoMethodFracErrorUp, histoMethodFracErrorDown, hComponentsUp, hError, hComponentsDown,pad1,pad2]

def stampFab(lumi = 'n/a',datamc='MC'):
    tl.SetTextFont(cmsTextFont)
    tl.SetTextSize(1.6*tl.GetTextSize())
    tl.DrawLatex(0.152,0.82, 'CMS')
    tl.SetTextFont(extraTextFont)
    tl.DrawLatex(0.25,0.82, ('MC' in datamc)*' simulation'+' internal')    
    #tl.DrawLatex(0.14,0.74, ('MC' in datamc)*' simulation'+' internal')
    tl.SetTextFont(regularfont)
    if lumi=='': tl.DrawLatex(0.62,0.82,'#sqrt{s} = 13 TeV')
    else: tl.DrawLatex(0.56,0.82,str(lumi)+' fb^{-1}'+'(13 TeV)')
    #tl.DrawLatex(0.64,0.82,'#sqrt{s} = 13 TeV')#, L = '+str(lumi)+' fb^{-1}')	
    tl.SetTextSize(tl.GetTextSize()/1.6)



units = {}
units['HardMet']='GeV'
units['Met']=units['HardMet']
units['Ht']='GeV'
units['St']='GeV'
units['NJets']='bin'
units['BTags']='bin'
units['Jet1Pt']='GeV'
units['Jet1Eta']='bin'
units['Jet2Pt']='GeV'
units['Jet2Eta']='bin'
units['Jet3Pt']='GeV'
units['Jet3Eta']='bin'
units['Jet4Pt']='GeV'
units['Jet4Eta']='bin'
units['HardMetPhi']='rad'
units['DPhi1']='rad'
units['DPhi2']='rad'
units['DPhi3']='rad'
units['DPhi4']='rad'
units['SearchBins']='bin'
units['MvaLowHardMet']='bin'
units['MvaLowHt']='bin'
units['Odd']='modulo false'
units['csvAve']=''
units['BestDijetMass']='GeV'
units['MinDeltaM']='GeV'
units['MaxDPhi']='rad'
units['MaxForwardPt'] = 'GeV'
units['MaxHemJetPt'] = 'GeV'
units['HtRatio'] = 'bin'
units['MinDeltaPhi'] = 'bin'
units['NPhotons'] = 'bin'
units['DPhiPhoPho'] = 'bin'


baseline = {}
baseline['HardMet'] = 300
baseline['Ht'] = 300
baseline['NJets'] = 2
baseline['BTags'] = 0
baseline['DPhi1'] = 0.5
baseline['DPhi2'] = 0.5
baseline['DPhi3'] = 0.3
baseline['DPhi4'] = 0.3

baselineStr = {}
baselineStr['HardMet']='E_{T}^{miss} > '+str(baseline['HardMet'])+' GeV'
baselineStr['Ht']='H_{T} > '+str(baseline['Ht'])+' GeV'
baselineStr['NJets']='N_{jets} #geq '+str(baseline['NJets'])
baselineStr['BTags']=''
baselineStr['DPhi1']='#Delta#phi_{1}'
baselineStr['DPhi2']='#Delta#phi_{2}'
baselineStr['DPhi3']='#Delta#phi_{3}'
baselineStr['DPhi4']='#Delta#phi_{4}'

def mkCutsLabel(kinvar,regionselect='', baselineStr_ = baselineStr):
    str_ = ''
    for key in baselineStr:
        if kinvar in key: continue
        if baselineStr_[key]=='': continue
        if kinvar=='Met' and 'miss' in baselineStr_[key]: continue
        if 'Phi' in key and 'LowDeltaPhi' in regionselect: continue
        if 'Jet' in kinvar and 'Jets' not in kinvar and 'HardMet' in key: continue
        str_+= baselineStr_[key]+', '
    if len(str_)>1:
        if str_[-2:]==', ':
            str_=str_[:-2]
    if 'LowDeltaPhi' in regionselect: str_+= ', #Delta#phi(inv.)'
    return str_

def mkLabel(str_,kinvar,selection=''):
    newstr = str_
    if newstr[0]=='h':newstr = newstr[1:]
    newstr = newstr.replace('GenSmeared',' gen-smeared ')
    newstr = newstr.replace('Rebalanced',' rebalanced ')
    newstr = newstr.replace('RplusS','QCD R&S')
    newstr = newstr.replace('Observed','QCD Observed')
    newstr = newstr.replace(kinvar,'')
    newstr = newstr.replace('_b','').replace('_','')
    newstr = newstr.replace(selection+' ','')
    return newstr


def nicelabel(label):
    label_ = label
    label_ = label_.replace('Vs',' vs ')
    label_ = label_.replace('HardMet','E_{T}^{miss}')
    label_ = label_.replace('St','H_{T}')    
    label_ = label_.replace('Met','E_{T}^{miss}')
    label_ = label_.replace('Ht','H_{T}')
    label_ = label_.replace('NJets','N_{jets}')
    label_ = label_.replace('BTags','N_{b-jets}')
    label_ = label_.replace('Pt',' p_{T}')
    label_ = label_.replace('Eta',' #eta')
    if 'DPhi' in label_:
        label_ = label_.replace('DPhi','#Delta#phi(H^{miss}_{T}, jet')
        label_ = label_+')'
        numberloc = max(label_.find('1'),label_.find('2'),label_.find('3'),label_.find('4'))+1
        label_ = label_[:numberloc]+', '+label_[numberloc:]
        label_ = label_.replace(', )',')')
    return label_    

def passQCDHighMETFilter(t):
    metvec = mkmet(t.MET, t.METPhi)
    for ijet, jet in enumerate(t.Jets):
        if not (jet.Pt() > 200): continue
        if not (t.Jets_muonEnergyFraction[ijet]>0.5):continue 
        jetvec = TLorentzVector()
        jetvec.SetPtEtaPhiE(t.Jets[0].Pt(), t.Jets[0].Eta(), t.Jets[0].Phi(), t.Jets[0].E())
        if (abs(jetvec.DeltaPhi(metvec)) > (3.14159 - 0.4)): return False
    return True


def passQCDHighMETFilter2(t):
    if len(t.Jets)>0:
        metvec = TLorentzVector()
        metvec.SetPtEtaPhiE(t.MET, 0, t.METPhi,0)
        jetvec = TLorentzVector()
        jetvec.SetPtEtaPhiE(t.Jets[0].Pt(), t.Jets[0].Eta(), t.Jets[0].Phi(), t.Jets[0].E())
        if abs(jetvec.DeltaPhi(metvec))>(3.14159-0.4) and t.Jets_neutralEmEnergyFraction[0]<0.03:
            return False
    return True


def passesUniversalSelectionFast(t, verbose=True):
    if not ( t.NVtx>0): return -1
    return True
        
def passesUniversalSelection(t, verbose=True):
    if not ( t.NVtx>0): 
        return -1 #bool(t.JetID) and 
    #featuring:
    #if not t.globalTightHalo2016Filter: return False ##this alone was good # only these comments weren't saved on last submission
    if not bool(t.globalSuperTightHalo2016Filter): 
        return -5
    if not bool(t.HBHENoiseFilter): 
        return -6    
    if not bool(t.HBHEIsoNoiseFilter): 
        return -7
    if not bool(t.eeBadScFilter): 
        return -8      
    if not bool(t.BadChargedCandidateFilter): 
        return -9
    if not bool(t.BadPFMuonFilter): 
        return -10
    if not bool(t.CSCTightHaloFilter): 
        return -11
    if not bool(t.EcalDeadCellTriggerPrimitiveFilter): 
        return -12     ##I think this one makes a sizeable difference    
    if not bool(t.ecalBadCalibReducedExtraFilter): 
        return -13
    if not bool(t.ecalBadCalibReducedFilter): 
        return -14
    '''#first half filters up edge    
    #first half filters low edge           
    ####if not t.ecalBadCalibFilter: return False #this says it's deprecated

    '''#second half filters low edge               

    if not  passQCDHighMETFilter(t): 
        return -2
    if not passQCDHighMETFilter2(t): 
        return -3
    if not t.PFCaloMETRatio<5:         
        return -4    
    return True

def passesHadronicSusySelection(t):
    if not (t.NElectrons==0 and t.NMuons==0 and t.isoElectronTracks==0 and t.isoMuonTracks==0 and t.isoPionTracks==0): return False
    return True
