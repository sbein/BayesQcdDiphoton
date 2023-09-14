from array import *

class sms():

    def __init__(self, modelname):
        if modelname.find("SIG-HL-T1tttt") != -1:
            self.T1tttt()
            #self.Zmin = 1e-2
            #self.Zmax = 5e2
            self.Zmin = 0
            self.Zmax = 10
            self.Xmax = 3000
        elif modelname.find("SIG-HL-T5ttcc") != -1:
            self.T5ttcc()
            #self.Zmin = 1e-2
            #self.Zmax = 5e2
            self.Zmin = 0
            self.Zmax = 10
            self.Xmax = 3000
        elif modelname.find("SIG-HL-T2tt") != -1:
            self.T2tt()
            #self.Xmax = 1250
            self.Xmax = 2000
            self.Ymax = 925
            #self.Zmin = 1e-2
            #self.Zmax = 5e2
            self.Zmin = 0
            self.Zmax = 10
            #self.diagX = array('d',[-35,   900,   self.Xmin])
        elif modelname.find("HL-T1tttt") != -1:
            self.T1tttt()
            self.Xmax = 3000
            self.Zmin = 1.e-5
        elif modelname.find("HL-T5ttcc") != -1:
            self.T5ttcc()
            self.Xmax = 3000
        elif modelname.find("HL-T2tt") != -1:
            self.T2tt()
            self.Zmin = 1.e-5
            self.Xmax = 2000
        elif modelname.find("SIG-HE-T1tttt") != -1:
            self.T1tttt()
            self.Zmin = 1e-2
            self.Zmax = 1e4
            #self.Zmin = 0
            #self.Zmax = 10
            self.Xmax = 3500
        elif modelname.find("SIG-HE-T5ttcc") != -1:
            self.T5ttcc()
            self.Zmin = 1e-2
            self.Zmax = 1e4
            #self.Zmin = 0
            #self.Zmax = 10
            self.Xmax = 3500
        elif modelname.find("SIG-HE-T2tt") != -1:
            self.T2tt()
            self.Zmin = 1e-2
            self.Zmax = 1e4
            #self.Zmin = 0
            #self.Zmax = 10
            self.Ymax = 925
            self.Xmax = 2000
        elif modelname.find("HE-T1tttt") != -1:
            self.T1tttt()
            self.label= "#splitline{pp #rightarrow #tilde{g}#tilde{g},}{#tilde{g} #rightarrow t#bar{t}#tilde{#chi}^{0}_{1}}"
            self.Zmin = 1.e-5
            #self.Zmax = 2.e-1
            self.Ymax = 1650
            self.Xmax = 3500
        elif modelname.find("HE-T5ttcc") != -1:
            self.T5ttcc()
            self.label= "#splitline{pp #rightarrow #tilde{g}#tilde{g},}{#tilde{g} #rightarrow t#bar{c}#tilde{#chi}^{0}_{1}}"
            #self.Zmin = 1.e-5
            #self.Zmax = 2.e-1
            self.Ymax = 1450
            self.Xmax = 3500
        elif modelname.find("HE-T2tt") != -1:
            self.T2tt()
            self.Zmin = 1.e-5
            #self.Zmax = 2.
            self.Ymax = 800
            self.Xmax = 2000
        elif modelname.find("T1tttt") != -1: self.T1tttt()
        elif modelname.find("T5ttcc") != -1: self.T5ttcc()
        elif modelname.find("T5ttttDM175") != -1: self.T5ttttDM175()
        elif modelname.find("T5qqqqVV") != -1: self.T5qqqqVV()
        elif modelname.find("T1tbbb") != -1: self.T1tbbb()
        elif modelname.find("T1ttbb") != -1: self.T1ttbb()
        elif modelname.find("T1tttb") != -1: self.T1tttb()
        elif modelname.find("T1bbbb") != -1: self.T1bbbb()
        elif modelname.find("T1x0p25y0p25") != -1: self.T1x0p25y0p25()
        elif modelname.find("T1x0p50y0p00") != -1: self.T1x0p50y0p00()
        elif modelname.find("T1x0p00y0p50") != -1: self.T1x0p00y0p50()
        elif modelname.find("T1x0p00y0p00") != -1: self.T1x0p00y0p00()
        elif modelname.find("T1x1p00y0p00") != -1: self.T1x1p00y0p00()
        elif modelname.find("T1x0p50y0p25") != -1: self.T1x0p50y0p25()
        elif modelname.find("T1x0p25y0p50") != -1: self.T1x0p25y0p50()
        elif modelname.find("T1x0p50y0p50") != -1: self.T1x0p50y0p50()
        elif modelname.find("T1bri") != -1: self.T1bri()
        #elif modelname.find("T1qqqq") != -1: self.T1qqqq()
        elif modelname.find("T1qqqqLL") != -1: self.T1qqqqLL()
        elif modelname.find("T6Wg") != -1: self.T6Wg()
        elif modelname.find("T5Wg") != -1: self.T5Wg()            
        elif modelname.find("T2bb") != -1: self.T2bb()
        elif modelname.find("T2qq") != -1: self.T2qq()
        elif modelname.find("T6bbHH") != -1: self.T6bbHH()            
        elif modelname.find("T2ttGluino") != -1: self.T2ttGluino()
        elif modelname.find("T2tt") != -1: self.T2tt()
        elif modelname.find("T2btLL") != -1: self.T2btLL()
        elif modelname.find("T2tb") != -1: self.T2tb()
        elif modelname.find("T2bw") != -1: self.T2bw()
        elif modelname.find("T2bH") != -1: self.T2bH()


    def T2bH(self):
        # model name
        self.modelname = "T2bH"
        # decay chain
        self.label= "pp #rightarrow #tilde{b}#tilde{b}, #tilde{b} #rightarrow b#tilde{#chi}^{0}_{2} #rightarrow  bH#tilde{#chi}^{0}_{1}"
        self.masslabel = "m_{#tilde{#chi}^{0}_{2}}-m_{#tilde{#chi}^{0}_{1}}=130 GeV"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 250
        self.Xmax = 500
        self.Ymin = 0
        self.Ymax = 400
        self.Zmax = 10
        self.Zmin = 1
        # produce sparticle
        self.sParticle = "m_{#tilde{b}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mSbotton - 150
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-150, 20000-150,self.Xmax])
        #self.divX = 407
        self.divX = 407
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1tttt(self):
        # model name
        self.modelname = "T1tttt"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow t#bar{t}#tilde{#chi}^{0}_{1}"
        self.masslabel = ""
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 2300
        self.Ymin = 0
        self.Ymax = 2300
        self.Zmax = 2
        self.Zmin = 5.e-6
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])  
        self.divX = 404 #408
        self.divY = 408
        self.optX = True
        self.optY = True

    def T5qqqqVV(self):
        # model name
        self.modelname = "T5qqqqVV"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow q#bar{q}#tilde{#chi}^{0}_{1}V"
        self.masslabel = ""
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 2300
        self.Ymin = 0
        self.Ymax = 2000
        self.Zmax = 2
        self.Zmin = 5.e-4
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position 
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25, 20000-25,self.Xmax])  
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True

    def T5ttcc(self):
        # model name
        self.modelname = "T5ttcc"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow t#bar{c}#tilde{#chi}^{0}_{1}"
        self.masslabel = ""
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 2300
        self.Ymin = 0
        self.Ymax = 2125
        self.Zmax = 2
        self.Zmin = 1.e-5
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop 
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-110, 20000-110,self.Xmax])  
        self.divX = 404
        self.divY = 408
        self.optX = True
        self.optY = True

    def T5ttttDM175(self):
        # model name
        self.modelname = "T5ttttDM175"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow t#tilde{t} #rightarrow t#bar{t}#tilde{#chi}^{0}_{1}"
        self.masslabel = "m_{#tilde{t}}-m_{#tilde{#chi}^{0}_{1}}=175 GeV"
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 1700
        self.Ymin = 0
        self.Ymax = 1400
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 275
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])  
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1x0p25y0p25(self):
        # model name                                                                                                                           
        self.modelname = "T1x0p25y0p25"
        # decay chain                                                                      
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1} / tt#tilde{#chi}^{0}_{1} / bb#tilde{#chi}^{0}_{1} (x=#frac{1}{4},y=#frac{1}{4})"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # scan range to plot                                                                                                                   
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle                                                                                                                    
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP                                         
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop                                                                                            
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1x0p25y0p50(self):
        # model name                                                                                                                           
        self.modelname = "T1x0p25y0p50"
        # decay chain                                                                      
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1} / tt#tilde{#chi}^{0}_{1} / bb#tilde{#chi}^{0}_{1} (x=#frac{1}{4},y=#frac{1}{2})"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # scan range to plot                                                                                                                   
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle                                                                                                                    
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop                                                                                            
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1x0p50y0p25(self):
        # model name                                                                                                                           
        self.modelname = "T1x0p50y0p25"
        # decay chain                                                                      
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1} / tt#tilde{#chi}^{0}_{1} / bb#tilde{#chi}^{0}_{1} (x=#frac{1}{2},y=#frac{1}{4})"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # scan range to plot                                                                                                                   
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle                                                                                                                    
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop                                                                                            
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True        
        
        
    def T1x0p50y0p50(self):
        # model name                                                                                                                           
        self.modelname = "T1x0p50y0p50"
        # decay chain                                                                      
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tt#tilde{#chi}^{0}_{1} / bb#tilde{#chi}^{0}_{1} (x=#frac{1}{2},y=#frac{1}{2})"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # scan range to plot                                                                                                                   
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle                                                                                                                    
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop                                                                                            
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1x0p00y0p00(self):
        # model name                                                                                                                           
        self.modelname = "T1x0p00y0p00"
        # decay chain                                                                      
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1} (x=0,y=0)"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # scan range to plot                                                                                                                   
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle                                                                                                                    
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop                                                                                            
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1x0p50y0p00(self):
        # model name                                                                                                                           
        self.modelname = "T1x0p50y0p00"
        # decay chain                                                                      
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1} / bb#tilde{#chi}^{0}_{1} (x=#frac{1}{2},y=0)"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # scan range to plot                                                                                                                   
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle                                                                                                                    
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop                                                                                            
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1x0p00y0p50(self):
        # model name                                                                                                                           
        self.modelname = "T1x0p50y0p00"
        # decay chain                                                                      
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1} / tt#tilde{#chi}^{0}_{1} (x=0,y=#frac{1}{2})"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # scan range to plot                                                                                                                   
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle                                                                                                                    
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop                                                                                            
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1x1p00y0p00(self):
        # model name                                                                                                                           
        self.modelname = "T1x1p00y0p00"
        # decay chain                                                                      
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow bb#tilde{#chi}^{0}_{1} (x=1,y=0)"
        self.masslabel = ""
        # scan range to plot                                                                                                                   
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle                                                                                                                    
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop                                                                                            
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1bri(self):
        # model name                                                                                                                           
        self.modelname = "T1bri"
        # decay chain                                                                      
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1} / tt#tilde{#chi}^{0}_{1} / bb#tilde{#chi}^{0}_{1} (BR indep.)"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # scan range to plot                                                                                                                   
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle                                                                                                                    
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop                                                                                            
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
                
    def T1bbbb(self):
        # model name
        self.modelname = "T1bbbb"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow b#bar{b}#tilde{#chi}^{0}_{1}"
        self.masslabel = ""
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600
        self.Xmax = 2300
        self.Ymin = 0
        self.Ymax = 2200
        self.Zmax = 2
        self.Zmin = 1.e-4
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25, 20000-25,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
        
    def T1qqqq(self):
        # model name
        self.modelname = "T1qqqq"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow q#bar{q}#tilde{#chi}^{0}_{1}"
        self.masslabel = ""
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1600
        self.Zmax = 2
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25, 20000-25,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True

    def T1qqqqLL(self):
        # model name
        self.modelname = "T1qqqqLL"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow q#bar{q}#tilde{#chi}^{#pm}_{1}"
        self.masslabel = "c#tau(#tilde{#chi}^{#pm}) = 200 cm"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 1000
        self.Xmax = 2800
        self.Ymin = 1
        #self.Ymax = 3300
        self.Ymax = 2775
        self.Zmax = 10.
        self.Zmin = 1.e-5
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25, 20000-25,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True


    def T6Wg(self):
        # model name
        self.modelname = "T1qqqqLL"
        # decay chain
        self.label= "pp #rightarrow #tilde{q}#tilde{#bar{q}}, #tilde{q} #rightarrow q#tilde{#chi}^{0}_{1}, #tilde{#chi}^{0}_{1}#rightarrow #gamma #tilde{G}"#/#tilde{#chi}^{#pm}_{1}, #tilde{#chi}^{0}_{1}#rightarrow #gamma #tilde{G}/#tilde{#chi}^{#pm}_{1}#rightarrow W^{#pm} #tilde{G}"
        self.masslabel = ""
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 610
        self.Xmax = 1800
        self.Ymin = 1
        #self.Ymax = 3300
        self.Ymax = 2250
        self.Zmax = 0.0013
        self.Zmin = 0.0002
        
        # produce sparticle
        self.sParticle = "m_{#tilde{q}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25, 20000-25,self.Xmax])
        self.divX = 204
        self.divY = 204
        self.optX = True
        self.optY = True


    def T5Wg(self):
        # model name
        self.modelname = "T1qqqqLL"
        # decay chain
        #self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow q#bar{q}#tilde{#chi}^{0}_{1}/#tilde{#chi}^{#pm}_{1}, #tilde{#chi}^{0}_{1}#rightarrow #gamma #tilde{G}/#tilde{#chi}^{#pm}_{1}#rightarrow W^{#pm} #tilde{G}"
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow q#bar{q}#tilde{#chi}^{0}_{1}, #tilde{#chi}^{0}_{1}#rightarrow #gamma #tilde{G}"
        self.masslabel = ""
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 675
        self.Xmax = 1900
        self.Ymin = 100     
        #self.Ymax = 3300
        self.Ymax = 2450
        self.Zmax = 2.e-3
        self.Zmin = 2.e-4
        
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25, 20000-25,self.Xmax])
        self.divX = 306
        self.divY = 306
        self.optX = True
        self.optY = True
        

    def T2qq(self):
        # model name
        self.modelname = "T2qq"
        # decay chain
        self.label= "pp #rightarrow #tilde{q}#tilde{q}, #tilde{q} #rightarrow q#tilde{#chi}^{0}_{1}"
        self.masslabel = ""
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 150
        self.Xmax = 1100
        self.Ymin = 0
        self.Ymax = 800
        self.Zmax = 10
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{q}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25,20000-25,self.Xmax])
        #self.divX = 407
        self.divX = 409
        self.divY = 408
        self.optX = True
        self.optY = True

        
    def T2bb(self):
        # model name
        self.modelname = "T2bb"
        # decay chain
        self.label= "pp #rightarrow #tilde{b}#tilde{b}, #tilde{b} #rightarrow b#tilde{#chi}^{0}_{1}"
        self.masslabel = ""
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 150
        self.Xmax = 1400
        self.Ymin = 0
        self.Ymax = 900
        self.Zmax = 10
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{b}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25,20000-25,self.Xmax])
        #self.divX = 407
        self.divX = 409
        self.divY = 408
        self.optX = True
        self.optY = True

        
    def T2tt(self):
        # model name
        self.modelname = "T2tt"
        # decay chain
        self.label= "pp #rightarrow #tilde{t}#tilde{t}, #tilde{t} #rightarrow t#tilde{#chi}^{0}_{1}"
        self.masslabel = ""
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 100
        self.Xmax = 1500
        self.Ymin = 0
        self.Ymax = 1200
        self.Zmax = 200
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{t}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,   1000,   self.Xmin])
        self.diagY = array('d',[-75, 1000-75,self.Ymax])
        
        self.diagXtop = array('d',[0,    275,     0])
        self.diagYtop = array('d',[-175, 275-175, -175])
        
        self.fillXtop = array('d',[0,       275+12.5,       275-12.5,       0])
        self.fillYtop = array('d',[-175-25, 275-175-25+12.5,275-175+25-12.5,-175+25])
        
        #self.divX = 407
        self.divX = 409
        self.divY = 408
        self.optX = True
        self.optY = True

        
    def T2ttGluino(self):
        # model name
        self.modelname = "T2ttGluino"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow t#tilde{t} #rightarrow t#tilde{#chi}^{0}_{1}+invisible"
        self.masslabel = "m_{#tilde{t}} #approx m_{#tilde{#chi}^{0}_{1}}"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 100
        self.Xmax = 900
        self.Ymin = 0
        self.Ymax = 700
        self.Zmax = 200
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-75, 20000-75,self.Xmax])
        
        self.diagXtop = array('d',[0,20000,self.Xmin])
        self.diagYtop = array('d',[-175, 20000-175,self.Xmax])
        
        #self.fillXtop = array('d',[0,20000,20000,0])
        #self.fillYtop = array('d',[-175-25, 20000-175-25,20000-175+25,-175+25])
        
        #self.divX = 407
        self.divX = 409
        self.divY = 408
        self.optX = True
        self.optY = True

        
    def T2btLL(self):
        # model name
        self.modelname = "T2btLL"
        # decay chain
        self.label= "pp #rightarrow #tilde{t}#tilde{t}, #tilde{t} #rightarrow t#tilde{#chi}^{0}_{1} / b#tilde{#chi}^{#pm}_{1}"
        #self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        self.masslabel = "ctau = 200"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 400
        self.Xmax = 2500
        self.Ymin = 0
        self.Ymax = 2000
        self.Zmax = 0.1
        self.Zmin = 1.e-5
        # produce sparticle
        self.sParticle = "m_{#tilde{t}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25, 20000-25,self.Xmax])
        #self.divX = 407
        self.divX = 509#409
        self.divY = 508#408
        self.optX = True
        self.optY = True

    def T2tb(self):
        # model name
        self.modelname = "T2tb"
        # decay chain
        self.label= "pp #rightarrow #tilde{t}#tilde{t}, #tilde{t} #rightarrow t#tilde{#chi}^{0}_{1} / b#tilde{#chi}^{#pm}_{1}"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 150
        self.Xmax = 2500
        self.Ymin = 0
        self.Ymax = 600
        self.Zmax = 10
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{t}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-100, 20000-100,self.Xmax])
        #self.divX = 407
        self.divX = 409
        self.divY = 408
        self.optX = True
        self.optY = True
        
        
    def T2bw(self):
        # model name
        self.modelname = "T2bw"
        # decay chain
        self.label= "pp #rightarrow #tilde{t}#tilde{t}, #tilde{t} #rightarrow b#tilde{#chi}^{#pm}_{1}"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 150
        self.Xmax = 900
        self.Ymin = 0
        self.Ymax = 600
        self.Zmax = 10
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{t}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-100, 20000-100,self.Xmax])
        #self.divX = 407
        self.divX = 409
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1tbbb(self):
        # model name
        self.modelname = "T1tbbb"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1} / bb#tilde{#chi}^{0}_{1}"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 400
        self.Xmax = 1500
        self.Ymin = 0
        self.Ymax = 1200
        self.Zmax = 1
        self.Zmin = 5.e-4
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-100, 20000-100,self.Xmax])
        self.divX = 406
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1ttbb(self):
        # model name
        self.modelname = "T1ttbb"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1}"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600
        self.Xmax = 2100
        self.Ymin = 0
        self.Ymax = 2000
        self.Zmax = 2
        self.Zmin = 5.e-4
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-100, 20000-100,self.Xmax])
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True
        
    def T1tttb(self):
        # model name
        self.modelname = "T1tttb"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow tb#tilde{#chi}^{#pm}_{1} / tt#tilde{#chi}^{0}_{1}"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 400
        self.Xmax = 1500
        self.Ymin = 0
        self.Ymax = 1200
        self.Zmax = 1
        self.Zmin = 5.e-4
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} (GeV)"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-200, 20000-200,self.Xmax])
        self.divX = 406
        self.divY = 408
        self.optX = True
        self.optY = True

        
    def T6bbHH(self):
        # model name
        self.modelname = "T6bbHH"
        # decay chain
        self.label= "pp #rightarrow #tilde{b}#tilde{b}, #tilde{b}#rightarrow bH#tilde{#chi}^{0}_{1}"
        self.masslabel = "m_{#tilde{#chi}_{2}} = #frac{m_{#tilde{#chi}_{1}}+m_{#tilde{b}}}{2}"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 300
        self.Xmax = 700
        self.Ymin = 0
        self.Ymax = 45 
        # produce sparticle
        self.sParticle = "m_{sbottom} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"
        # diagonal position: mLSP = mgluino - 2mhiggs
        self.diagX = array('d',[0,20000, self.Xmin])
        self.diagY = array('d',[-300, 20000-300, self.Xmax])
        self.divX = 404
        self.divY = 409
        self.optX = True
        self.optY = True
