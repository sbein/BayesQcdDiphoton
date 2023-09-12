import sys
import ROOT as rt

class inputFile():

    def __init__(self, fileName):
        self.HISTOGRAM = self.findHISTOGRAM(fileName)
        self.EXPECTED = self.findEXPECTED(fileName)
        self.EXPECTED2 = self.findEXPECTED2(fileName)
        self.OBSERVED = self.findOBSERVED(fileName)
        self.SYST0 = self.findSYST0(fileName)
        self.SYST1 = self.findSYST1(fileName)
        self.SYST2 = self.findSYST2(fileName)
        self.SYST3 = self.findSYST3(fileName)
        self.SYST4 = self.findSYST4(fileName)
        self.SIG1 = self.findSIG1(fileName)
        self.SIG2 = self.findSIG2(fileName)
        self.SIG3 = self.findSIG3(fileName)
        self.SIG4 = self.findSIG4(fileName)
        self.LUMI = self.findATTRIBUTE(fileName, "LUMI")
        self.ENERGY = self.findATTRIBUTE(fileName, "ENERGY")
        self.PRELIMINARY = self.findATTRIBUTE(fileName, "PRELIMINARY")
        self.BOXES = self.findATTRIBUTE(fileName, "BOXES")

    def findATTRIBUTE(self, fileName, attribute):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != attribute: continue
            fileIN.close()
            return tmpLINE[1]

    def findHISTOGRAM(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "HISTOGRAM": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            hist = rootFileIn.Get(tmpLINE[2])
            hist.SetDirectory(rt.gROOT)
            return {'histogram': hist}
            
    def findEXPECTED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "EXPECTED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            plus = rootFileIn.Get(tmpLINE[3])
            minus = rootFileIn.Get(tmpLINE[4])
            return {'nominal': nominal,
                    'plus': plus,
                    'minus': minus,
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

    def findEXPECTED2(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "EXPECTED2": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])            
            nominal = rootFileIn.Get(tmpLINE[2])
            plus2 = rootFileIn.Get(tmpLINE[3])
            minus2 = rootFileIn.Get(tmpLINE[4])
            return {'nominal': nominal,
                    'plus2': plus2,
                    'minus2': minus2,
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}
        
    def findOBSERVED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "OBSERVED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            plus = rootFileIn.Get(tmpLINE[3])
            minus = rootFileIn.Get(tmpLINE[4])
            return {'nominal': nominal,
                    'plus': plus,
                    'minus': minus,
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

    def findSYST0(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "SYST0": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            plus = rootFileIn.Get(tmpLINE[3])
            minus = rootFileIn.Get(tmpLINE[4])
            return {'nominal': nominal,
                    'plus': plus,
                    'minus': minus,
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

    def findSYST1(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "SYST1": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            plus = rootFileIn.Get(tmpLINE[3])
            minus = rootFileIn.Get(tmpLINE[4])
            return {'nominal': nominal,
                    'plus': plus,
                    'minus': minus,
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

    def findSYST2(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "SYST2": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            plus = rootFileIn.Get(tmpLINE[3])
            minus = rootFileIn.Get(tmpLINE[4])
            return {'nominal': nominal,
                    'plus': plus,
                    'minus': minus,
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

    def findSYST3(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "SYST3": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            plus = rootFileIn.Get(tmpLINE[3])
            minus = rootFileIn.Get(tmpLINE[4])
            return {'nominal': nominal,
                    'plus': plus,
                    'minus': minus,
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

    def findSYST4(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "SYST4": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            plus = rootFileIn.Get(tmpLINE[3])
            minus = rootFileIn.Get(tmpLINE[4])
            return {'nominal': nominal,
                    'plus': plus,
                    'minus': minus,
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

    def findSIG1(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "SIG1": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            return {'nominal': nominal,
                    'colorLine': tmpLINE[3],
                    'colorArea': tmpLINE[4]}

    def findSIG2(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "SIG2": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            return {'nominal': nominal,
                    'colorLine': tmpLINE[3],
                    'colorArea': tmpLINE[4]}

    def findSIG3(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "SIG3": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            return {'nominal': nominal,
                    'colorLine': tmpLINE[3],
                    'colorArea': tmpLINE[4]}

    def findSIG4(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "SIG4": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            nominal = rootFileIn.Get(tmpLINE[2])
            return {'nominal': nominal,
                    'colorLine': tmpLINE[3],
                    'colorArea': tmpLINE[4]}
