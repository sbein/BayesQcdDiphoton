# BayesQcd

This is the package for running a photon-friendly rebalance and smear implementation on Ra2/b-style ntuples while on an LPC machine. 
## Set up code in a nobackup area (modify appropriately if you forked the repo)

```
cmsrel CMSSW_10_1_0
cd CMSSW_10_1_0/src
cmsenv
git clone https://github.com/sbein/BayesQcd/
cd BayesQcd/
mkdir jobs
mkdir output
mkdir pdfs
mkdir pdfs/ClosureTests
```

### Run the rebalance and smear code
I'm skipping the steps needed to create the prior and smearing templates. This command will run rebalance and smear and create histograms for the "truth" and "method" distributions with 10,000 events in one GJets file:

```
python tools/MaximizePosteriorTM.py --fnamekeyword Summer16v3.GJets_DR-0p4_HT-600 --quickrun True
```

Generate plots overlaying observed and R&S histograms

```
python tools/closurePlotter.py <output file from previous step>
```

This creates pdfs and a root file with canvases. You'll notice your histograms will likely suffer from low statistics, which is why it's good to use the batch system heavily when doing this (iteration time can be about 20 minutes to an hour). 


### Submit jobs to the condor batch system

This script defaults to submitting one job per input file. Assuming you have a valid proxy, the following script will initiate a large submission. Notice the first command below cleans up the jobs directory. It is important to do this before you submit. The script also suggests you to delete the output directory where your root files are returned so it can have a clean start. 

```
bash tools/CleanJobs.sh
python tools/submitjobs.py --analyzer tools/MaximizePosteriorTM.py --fnamekeyword Summer16v3.GJets_DR-0p4_HT --quickrun True
```
The quickrun option set to true tells the script to only run over 10,000 events per file. This argument can be removed when you're ready to max out your statistics. Output files will be put in the local output/<keyword> directory matching the specified keyword for the filename. The status of the jobs can be checked with

```
condor_q |grep <your user name>
```

Once the jobs are done, a wrapper for the hadd routine can be called which also fits a spline to each response function:
```
python tools/mergeHistosFinalizeWeights.py output/<folder name>
```

This applies the 1/n(simulated) on top of your the lumi*xsec weights, the latter of which was applied in the analyzer script. mergeHistosFinalizeWeights.py has hard code keywords defining the different datasets, each one corresponding to a unique cross section. If you want to run over another set of datasets, like inclusive QCD samples, you'd have to change these keywords by giving one key word per desired unique cross section. It creates a single file on which you can run the closurePlotter.py script. 
