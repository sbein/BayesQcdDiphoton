import os, sys
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default='Summer16.SMS-T1tttt_mGluino-1200_mLSP-800',help="file")
parser.add_argument("-jersf", "--JerUpDown", type=str, default='Nom',help="JER scale factor (Nom, Up, ...)")
parser.add_argument("-bootstrap", "--Bootstrap", type=str, default='0',help="boot strapping (0,1of5,2of5,3of5,...)")
parser.add_argument("-smears", "--smears", type=int, default=20,help="number smears per event")
parser.add_argument("-quickrun", "--quickrun", type=bool, default=False,help="Quick practice run (True, False)")
parser.add_argument("-forcetemplates", "--forcetemplates", type=str, default=False,help="you can use this to override the template choice")
parser.add_argument("-hemcut", "--hemcut", type=str, default='',help="you can use this to override the template choice")
parser.add_argument("-branchonly", "--branchonly", type=bool, default=False,help="skip rebalancing and smearing")
parser.add_argument("-extended", "--extended", type=int, default=1,help="short run")
parser.add_argument("-deactivateAcme", "--deactivateAcme", type=str, default='False')
args = parser.parse_args()
deactivateAcme = args.deactivateAcme=='True'
extended = args.extended
branchonly = args.branchonly
hemcut = args.hemcut
fnamekeyword = args.fnamekeyword.strip()
analyzer = args.analyzer
JerUpDown = args.JerUpDown
Bootstrap = args.Bootstrap
smears = args.smears
quickrun = args.quickrun

if Bootstrap=='0': 
    bootstrapmode = False
else: 
    bootstrapmode = True
    
istest = False
skipFilesWithErrorFile = True


try: 
	moreargs = ' '.join(sys.argv)
	moreargs = moreargs.split('--fnamekeyword')[-1]	
	moreargs = ' '.join((moreargs.split()[1:]))
except: moreargs = ''

moreargs = moreargs.strip()
print 'moreargs', moreargs



if 'Summer16' in fnamekeyword or 'Fall17' in fnamekeyword or 'Autumn18' in fnamekeyword:
    isdata___ = False
else: 
    isdata___ = True
    
    
cwd = os.getcwd()
acme = bool(deactivateAcme)


fnamefilename = 'usefulthings/filelistDiphoton.txt'
fnamefilename = 'usefulthings/filelistDiphotonBig.txt'
if not 'DoubleEG' in fnamekeyword:
    if 'Summer16v3.QCD_HT' in fnamekeyword or 'Summer16v3.WGJets_MonoPhoton' in fnamekeyword: 
        fnamefilename = 'usefulthings/filelistV17.txt'
fnamefile = open(fnamefilename)


fnamelines = fnamefile.readlines()
fnamefile.close()
import random
random.shuffle(fnamelines)

def main():
    counter = 0    
    for fname_ in fnamelines:
        if not (fnamekeyword in fname_): continue
        fname = fname_.strip()
        job = analyzer.split('/')[-1].replace('.py','').replace('.jdl','')+'-'+fname.split('/')[-1].strip()+'Jer'+JerUpDown
        #from utils import pause
        #pause()
        job = job.replace('.root','')+'_part'+str(extended)+'_acme'+args.deactivateAcme
        job = job.replace('.root',Bootstrap+'.root')     
        #print 'creating jobs:',job
        jdlname = 'jobs/'+job+'.jdl'        
        newjdl = open(jdlname,'w')
        newjdl.write(jdltemplate.replace('CWD',cwd).replace('JOBKEY',job))
        newjdl.close()
        if skipFilesWithErrorFile:
            errfilename = 'jobs/'+job+'.err'
            if os.path.exists(errfilename): 
                print 'skipping you...', errfilename
                continue
        newsh = open('jobs/'+job+'.sh','w')
        newshstr = shtemplate.replace('ANALYZER',analyzer).replace('FNAMEKEYWORD',fname).replace('MOREARGS',moreargs)
        newsh.write(newshstr)
        newsh.close()
        if not os.path.exists('output/'+fnamekeyword.replace(' ','')): 
            os.system('mkdir output/'+fnamekeyword.replace(' ',''))
        os.chdir('output/'+fnamekeyword.replace(' ',''))
        cmd =  'condor_submit '+'../../jobs/'+job+'.jdl'        
        print cmd
        if not istest: os.system(cmd)
        counter+=1
        os.chdir('../../')
        

    print 'counter', counter
jdltemplate = '''
universe = vanilla
Executable = CWD/jobs/JOBKEY.sh
Output = CWD/jobs/JOBKEY.out
Error = CWD/jobs/JOBKEY.err
Log = CWD/jobs/JOBKEY.log
should_transfer_files = YES
when_to_transfer_output = ON_EXIT
transfer_input_files=CWD/tools, CWD/usefulthings, CWD/src
x509userproxy = $ENV(X509_USER_PROXY)
Queue 1
'''

shtemplate = '''#!/bin/bash
source /cvmfs/cms.cern.ch/cmsset_default.sh
export SCRAM_ARCH=slc6_amd64_gcc630
echo $PWD
ls
scram project CMSSW_10_1_0
cd CMSSW_10_1_0/src
eval `scramv1 runtime -sh`
cd ${_CONDOR_SCRATCH_DIR}
echo $PWD
export x509userproxy=/uscms/home/sbein/x509up_u47534
ls
python ANALYZER --fnamekeyword FNAMEKEYWORD MOREARGS

for f in *.root
do 
   xrdcp "$f" root://cmseos.fnal.gov//store/user/lpcsusyphotons/TreeMakerRandS_28July2020/
done
rm *.root
'''

main()
print 'done'
##   xrdcp "$f" root://cmseos.fnal.gov//store/user/lpcsusyphotons/TreeMakerRandS_v2/
##TreeMakerRandS/
