from array import *

class sms():

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        if modelname.find("T5ttcc") != -1: self.T5ttcc()
        if modelname.find("T5tttt") != -1: self.T5tttt()
        if modelname.find("T5ttttDM175") != -1: self.T5ttttDM175()
        if modelname.find("T5qqqqVV") != -1: self.T5qqqqVV()
        if modelname.find("T1tbbb") != -1: self.T1tbbb()
        if modelname.find("T1ttbb") != -1: self.T1ttbb()
        if modelname.find("T1tttb") != -1: self.T1tttb()
        if modelname.find("T1bbbb") != -1: self.T1bbbb()
        if modelname.find("T1x0p25y0p25") != -1: self.T1x0p25y0p25()
        if modelname.find("T1x0p50y0p00") != -1: self.T1x0p50y0p00()
        if modelname.find("T1x0p00y0p50") != -1: self.T1x0p00y0p50()
        if modelname.find("T1x0p00y0p00") != -1: self.T1x0p00y0p00()
        if modelname.find("T1x1p00y0p00") != -1: self.T1x1p00y0p00()
        if modelname.find("T1x0p50y0p25") != -1: self.T1x0p50y0p25()
        if modelname.find("T1x0p25y0p50") != -1: self.T1x0p25y0p50()
        if modelname.find("T1x0p50y0p50") != -1: self.T1x0p50y0p50()
        if modelname.find("T1bri") != -1: self.T1bri()
        if modelname.find("T1qqqq") != -1: self.T1qqqq()
        if modelname.find("T1qqqqLL") != -1: self.T1qqqqLL()
        if modelname.find("T2bb") != -1: self.T2bb()
        if modelname.find("T2qq") != -1: self.T2qq()
        if modelname.find("T6bbHH") != -1: self.T6bbHH()            
        if modelname.find("T2ttGluino") != -1: self.T2ttGluino()
        elif modelname.find("T2tt") != -1: self.T2tt()
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
        self.sParticle = "m_{#tilde{b}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
        # diagonal position: mLSP = mSbotton - 150
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-150, 20000-150,self.Xmax])
        #self.divX = 407
        self.divX = 409
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
        self.Xmax = 2100
        self.Ymin = 0
        self.Ymax = 2000
        self.Zmax = 2
        self.Zmin = 5.e-4
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 225
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])  
        self.divX = 408
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.Ymax = 2000
        self.Zmax = 2
        self.Zmin = 1.e-4
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25, 20000-25,self.Xmax])  
        self.divX = 408
        self.divY = 408
        self.optX = True
        self.optY = True

    def T5tttt(self):
        # model name
        self.modelname = "T5tttt"
        # decay chain
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow t#tilde{t} #rightarrow t#bar{t}#tilde{#chi}^{0}_{1}"
        self.masslabel = "m_{#tilde{t}}-m_{#tilde{#chi}^{0}_{1}}=175 GeV"
        # scan range to plot
        self.Xmin = 600
        self.Xmax = 2300
        self.Ymin = 0
        self.Ymax = 2000
        self.Zmax = 2
        self.Zmin = 1.e-4
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 275
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-mW, 20000-mW,self.Xmax])  
        self.divX = 408
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP                                         
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP                                                                                                                                  
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.label= "pp #rightarrow #tilde{g}#tilde{g}, #tilde{g} #rightarrow q#bar{q}#tilde{#chi}^{0}_{1}"
        self.masslabel = ""
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 1000
        self.Xmax = 2800
        self.Ymin = 1
        self.Ymax = 2775
        self.Zmax = 20
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-25, 20000-25,self.Xmax])
        self.divX = 408
        self.divY = 408
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
        self.sParticle = "m_{#tilde{q}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{b}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.Xmax = 1200
        self.Ymin = 0
        self.Ymax = 900
        self.Zmax = 200
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{t}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000,self.Xmin])
        self.diagY = array('d',[-75, 20000-75,self.Xmax])
        
        self.diagXtop = array('d',[0,20000,self.Xmin])
        self.diagYtop = array('d',[-175, 20000-175,self.Xmax])
        
        self.fillXtop = array('d',[0,20000,20000,0])
        self.fillYtop = array('d',[-175-25, 20000-175-25,20000-175+25,-175+25])
        
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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

        
    def T2tb(self):
        # model name
        self.modelname = "T2tb"
        # decay chain
        self.label= "pp #rightarrow #tilde{t}#tilde{t}, #tilde{t} #rightarrow t#tilde{#chi}^{0}_{1} / b#tilde{#chi}^{#pm}_{1}"
        self.masslabel = "m_{#tilde{#chi}^{#pm}_{1}}-m_{#tilde{#chi}^{0}_{1}} = 5 GeV"
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 150
        self.Xmax = 900
        self.Ymin = 0
        self.Ymax = 600
        self.Zmax = 10
        self.Zmin = 1.e-3
        # produce sparticle
        self.sParticle = "m_{#tilde{t}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{t}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}^{0}_{1}} [GeV]"
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
        self.sParticle = "m_{sbottom} [GeV]"
        # LSP
        self.LSP = "m_{LSP} [GeV]"
        # diagonal position: mLSP = mgluino - 2mhiggs
        self.diagX = array('d',[0,20000, self.Xmin])
        self.diagY = array('d',[-300, 20000-300, self.Xmax])
        self.divX = 404
        self.divY = 409
        self.optX = True
        self.optY = True
