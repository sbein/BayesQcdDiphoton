from glob import glob


fname = 'usefulthings/filelistDiphotonBigV2.txt'
flist = glob('/eos/uscms//store/group/lpcsusyphotons/TreeMaker/*.root')
flistf = open(fname,'w')
for f in flist:
    flistf.write(f+'\n')

print 'just created'
print fname
flistf.close()
