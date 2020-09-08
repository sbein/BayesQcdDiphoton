#Welcome to the industrial age of Sam's rebalance and smear code. You're going to have a lot of fun!
import os,sys
from ROOT import *
from glob import glob
from utils import *
gROOT.SetBatch(1)
lumi = 'arbitrary'

fnew = TFile('plots.root', 'recreate')
c = TChain('PreSelection')
c.Add('output/Summer16v3.GJets_DR-0p4_HT/*.root')


histodim = '>>hadc2(6,150,750)'

#histodim = '>>hadc2(3,0,3)'

c1 = mkcanvas('c1')
c1.SetLogy()
c.Show(0)

c.Draw('MET'+histodim,'CrossSection*puWeight*(MET>100 && NJets>0 && NPhotonsLoose>0)')
h1 = c.GetHistogram().Clone('hobs')
c.Draw('HardMETPtRandSvec'+histodim,'CrossSection*puWeight/NSmearsPerEvent*(HardMETPtRandSvec>100 && NJetsRandSvec>0  && NPhotonsLoose>0 )')
h2 = c.GetHistogram().Clone('hest')
'''

c.Draw('NPhotonsLoose'+histodim,'CrossSection*puWeight*(MET>100 && NJets>0)')
h1 = c.GetHistogram().Clone('hobs')
c.Draw('NPhotonsLoose'+histodim,'CrossSection*puWeight/NSmearsPerEvent*(HardMETPtRandSvec>100 && NJetsRandSvec>0)')
h2 = c.GetHistogram().Clone('hest')
'''

histoStyler(h2, kTeal+2)
h2.SetFillStyle(1001)
h2.SetFillColor(h2.GetLineColor())

leg = mklegend()
hratio, hmethodsyst = FabDrawSystyRatio(c1,leg,h1,[h2],datamc='MC',lumi=lumi, title = '', LinearScale=False, fractionthing='truth / method')

c1.Update()
fnew.cd()
c1.Write()
print 'just created', os.getcwd()+'/'+fnew.GetName()
fnew.Close()
