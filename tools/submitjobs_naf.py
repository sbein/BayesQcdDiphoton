import os, sys
from glob import glob
from random import shuffle 
from time import sleep

test = False

import argparse
parser = argparse.ArgumentParser()
defaultfkey = 'Summer16.WJetsToLNu_TuneCUETP8M1_13TeV-madgraphMLM-pythia8_ext2_28'
parser.add_argument("-v", "--verbosity", type=bool, default=False,help="analyzer script to batch")
parser.add_argument("-analyzer", "--analyzer", type=str,default='tools/ResponseMaker.py',help="analyzer")
parser.add_argument("-fin", "--fnamekeyword", type=str,default=defaultfkey,help="file")
parser.add_argument("-jersf", "--JerUpDown", type=str, default='Nom',help="JER scale factor (Nom, Up, ...)")
parser.add_argument("-dtmode", "--dtmode", type=str, default='PixAndStrips',help="PixAndStrips, PixOnly, PixOrStrips")
parser.add_argument("-pu", "--pileup", type=str, default='Nom',help="Nom, Low, Med, High")
parser.add_argument("-smearvar", "--smearvar", type=str, default='Nom',help="use gen-kappa")
parser.add_argument("-ps", "--analyzeskims", type=bool, default=False,help="use gen-kappa")
parser.add_argument("-nfpj", "--nfpj", type=int, default=1)
parser.add_argument("-outdir", "--outdir", type=str, default='output/smallchunks')
args = parser.parse_args()
nfpj = args.nfpj
fnamekeyword = args.fnamekeyword.strip()
filenames = fnamekeyword
analyzer = args.analyzer
analyzeskims = args.analyzeskims
analyzer = analyzer.replace('python/','').replace('tools/','')
JerUpDown = args.JerUpDown
smearvar = args.smearvar
outdir = args.outdir



#try: 
moreargs = ' '.join(sys.argv)
moreargs = moreargs.split('--fnamekeyword')[-1]
moreargs = ' '.join(moreargs.split()[1:])



args4name = moreargs.replace(' ','').replace('--','-')


moreargs = moreargs.strip()
print 'moreargs', moreargs

cwd = os.getcwd()
filelist = glob(filenames)
#shuffle(filelist)


filesperjob = nfpj

print 'len(filelist)', len(filelist)
print 'filesperjob', filesperjob

def main():
	ijob = 1
	files = ''
	jobcounter_ = 0
	for ifname, fname in enumerate(filelist):
		files += fname+','
		if (ifname)%filesperjob==0: jname = fname
		if (ifname)%filesperjob==filesperjob-1 or ifname==len(filelist)-1:
			jobname = analyzer.replace('.py','')+'_'+jname[jname.rfind('/')+1:]#.replace('.root','_'+str(ijob))
			if len(args4name.split())>0: 
				jobname = jobname+args4name.replace(' ','-').replace('---','-').replace('--','-')
			if os.path.isfile('jobs/'+jobname+'.sh'):
				print 'skipping', fname, 'since', 'jobs/'+jobname+'.sh', 'exists'
				continue
			fjob = open('jobs/'+jobname+'.sh','w')
			files = files[:-1]#this just drops the comma
			fjob.write(jobscript.replace('CWD',cwd).replace('FNAMEKEYWORD',files).replace('ANALYZER',analyzer).replace('MOREARGS',moreargs).replace('JOBNAME',jobname).replace('OUTDIR',outdir))
			fjob.close()
			os.chdir('jobs')
			command = 'condor_qsub -cwd '+jobname+'.sh &'
			jobcounter_+=1
			print 'command', command
			if not test: os.system(command)
			os.chdir('..')
			files = ''
			ijob+=1
			sleep(0.1)
			#import sys
			#print 'press the any key'
			#sys.stdout.flush() 
			#raw_input('')
	print 'submitted', jobcounter_, 'jobs'

jobscript = '''#!/bin/zsh
source /etc/profile.d/modules.sh
source /afs/desy.de/user/b/beinsam/.bash_profile
module use -a /afs/desy.de/group/cms/modulefiles/
module load cmssw
export THISDIR=$PWD
echo "$QUEUE $JOB $HOST"
source /afs/desy.de/user/b/beinsam/.bash_profile
cd CWD
cmsenv
cd $THISDIR
export timestamp=$(date +%Y%m%d_%H%M%S%N)
mkdir $timestamp
cd $timestamp
cp -r CWD/tools .
cp -r CWD/usefulthings .
echo doing a good old pwd:
pwd
python tools/ANALYZER --fnamekeyword FNAMEKEYWORD MOREARGS
mv *.root CWD/OUTDIR
mv *.json CWD/OUTDIR
cd ../
rm -rf $timestamp
'''

main()
