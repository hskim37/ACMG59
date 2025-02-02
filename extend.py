from __future__ import print_function
from collections import OrderedDict
import sys
from outputCoords import outputCoords
import os
from log import log

def extend(gene):
    existingPaths = outputCoords(gene) # ['1-100_0.3-0.5','1-100_0.5-0.5',...]

    existingRegions = [] # [(1,100),(101,200),(201,300),...]

    ruleSatisfied = OrderedDict() # {(1,100):0.3,(201,300):0.5,...}

    with open('/home/rg252/setup/ACMG_MasterList.csv') as f:
        for line in f:
            split = line.split(',')
            if split[0]==gene:
                geneLen = int(split[2])

    for path in existingPaths:
        start = int((path.split('_')[0]).split('-')[0])
        end = int((path.split('_')[0]).split('-')[-1])
        bit = float((path.split('_')[-1]).split('-')[0])

        region = (start,end)

        if region not in existingRegions:
            existingRegions.append(region)

        try:
            csv = '/n/scratch2/rg252/ACMG59_NEW/{}/{}/align/{}_alignment_statistics.csv'.format(gene,path,path)
            with open(csv) as f:
                stats = ((f.readlines())[1]).split(',')
            path,mincov,nseqs,seqlen,ncov,nlc,perc,fuc,luc,lencov,nlcov,neff = stats

            if float(neff) >= 4.5*int(seqlen): # Leaves only the maximum threshold
                ruleSatisfied[region] = bit # Replaces threshold value if already there

        except IOError:
            print('ERROR')
            return

    tuples = []

    for key1 in ruleSatisfied: # Only regions(keys) that satisfy the 5x rule
        start1,end1 = key1
        thresh1 = ruleSatisfied[key1]
        filteredDict = {x:y for x,y in ruleSatisfied.items() if x[0]==end1+1}

        if len(filteredDict)==0:
            filteredDict = {key1:thresh1}

        for key2 in filteredDict:
            start2,end2 = key2
            thresh2 = ruleSatisfied[key2]
            start = start1
            end = end2
            maxThresh = max(thresh1,thresh2)

            # runThresh = [x for x in thresholdList if x<=maxThresh]

            if (start,end) not in existingRegions:
                tuples.append((start,end,maxThresh))
                existingRegions.append((start,end))

        else:
            start = start1-50
            end = end2+50

            if start<1:
                start = 1
            if end>geneLen:
                end = geneLen

            if (start,end) not in existingRegions:
                tuples.append((start,end,maxThresh))
                existingRegions.append((start,end))

    commands = []
    thresholdList = [0.3,0.5,0.7,0.8]
    for tup in tuples:
        start,end,maxThresh = tup
        if maxThresh==0.8:
            commands.append('sbatch -o /n/scratch2/rg252/ACMG59_NEW/outFiles/{}_{}-{}_out.txt config.sh {} {} {}'
                            .format(gene,start,end,gene,start,end))
        else:
            runThresh = [x for x in thresholdList if x<=maxThresh]
            for thresh in runThresh:
                commands.append('sbatch -o /n/scratch2/rg252/ACMG59_NEW/outFiles/{}_{}-{}_{}-0.5_out.txt config.sh {} {} 0.5 {} {}'
                                .format(gene,start,end,thresh,gene,thresh,start,end))

    commands.sort(key=lambda x:(int((((x.split()[2]).split('/')[-1]).split('_')[1]).split('-')[0]),
                                int((((x.split()[2]).split('/')[-1]).split('_')[1]).split('-')[1])))

    if len(commands)>0:
        for command in commands:
            print(command)
        if (raw_input('\nExecute? Y / N -> ')).lower()=='y':
            for command in commands:
                print('\n{}'.format(command))
                os.system(command)
                log(command)
    else:
        print('No more regions to extend.')

def main():
    gene = sys.argv[1]
    print()
    extend(gene)
    print()

if __name__=="__main__":
    main()
