# For regions that don't overlap
# ex) 1-100, 101-200, ...

from __future__ import print_function
from collections import OrderedDict
import sys
from outputCoords import outputCoords
import os

def extend(gene):
    existingPaths = outputCoords(gene) # ['1-100_0.3-0.5','1-100_0.5-0.5',...]
    
    existingRegions = [] # [(1,100),(101,200),(201,300),...]
    
    ruleSatisfied = OrderedDict() # {(1,100):0.3,(201,300):0.5,...}
    
    for path in existingPaths:
        start = int((path.split('_')[0]).split('-')[0])
        end = int((path.split('_')[0]).split('-')[-1])
        bit = float((path.split('_')[-1]).split('-')[0])
        
        region = (start,end)
        
        if region not in existingRegions:
            existingRegions.append(region)
            
        geneLen = max([x[1] for x in existingRegions])
        
        try:
            csv = '/n/scratch2/rg252/ACMG59_NEW/%s/%s/align/%s_alignment_statistics.csv' %(gene,path,path)
            with open(csv) as f:
                stats = ((f.readlines())[1]).split(',')
            path,mincov,nseqs,seqlen,ncov,nlc,perc,fuc,luc,lencov,nlcov,neff = stats
            
            if float(neff) >= 4.5*int(seqlen): # Leaves only the maximum threshold
                ruleSatisfied[region] = bit # Replaces threshold value if already there
                
        except IOError:
            print('ERROR')
            return
    
    commands = []

    thresholdList = [0.3,0.5,0.7,0.8]
    for key1 in ruleSatisfied: # Only regions(keys) that satisfy the 5x rule
        start1,end1 = key1
        filteredDict = {x:y for x,y in ruleSatisfied.items() if x[0]==end1+1}
        
        if len(filteredDict)==0:
            start = start1-50
            end = end1+50
            maxThresh = ruleSatisfied[key1]

            runThresh = [x for x in thresholdList if x<=maxThresh]
            
            if ((start,end) not in existingRegions) and start>=1 and end<=geneLen:
                if len(runThresh)>=4:
                    commands.append('sbatch -o /n/scratch2/rg252/ACMG59_NEW/outFiles/{}_{}-{}_out.txt config.sh {} {} {}'
                        .format(gene,start,end,gene,start,end))   
                else:
                    for thresh in runThresh:
                        commands.append('sbatch -o /n/scratch2/rg252/ACMG59_NEW/outFiles/{}_{}-{}_{}-0.5_out.txt config.sh {} {} 0.5 {} {}'
                            .format(gene,start,end,thresh,gene,thresh,start,end))

        else:
            for key2 in filteredDict:
                start2,end2 = key2
                start = start1
                end = end2
                maxThresh = max(ruleSatisfied[key1],ruleSatisfied[key2])
                    
                runThresh = [x for x in thresholdList if x<=maxThresh]
                
                if ((start,end) not in existingRegions) and start>=1 and end<=geneLen:
                    if len(runThresh)>=4:
                        commands.append('sbatch -o /n/scratch2/rg252/ACMG59_NEW/outFiles/{}_{}-{}_out.txt config.sh {} {} {}'
                            .format(gene,start,end,gene,start,end))   
                    else:
                        for thresh in runThresh:
                            commands.append('sbatch -o /n/scratch2/rg252/ACMG59_NEW/outFiles/{}_{}-{}_{}-0.5_out.txt config.sh {} {} 0.5 {} {}'
                                .format(gene,start,end,thresh,gene,thresh,start,end))
                        
    for command in commands:
        if commands.count(command)>=2:
            commands.remove(command)
    
    commands.sort(key=lambda x:(int((((x.split()[2]).split('/')[-1]).split('_')[1]).split('-')[0]),
                                            int((((x.split()[2]).split('/')[-1]).split('_')[1]).split('-')[1])))
                        
    if len(commands)>0:                         
        for command in commands:
            print(command)
        if (raw_input('\nExecute? Y / N -> ')).lower()=='y':
            for command in commands:
                print('\n{}'.format(command))
                os.system(command)
    else:
        print('No more regions to extend.')

def main():
    gene = sys.argv[1]
    print()
    extend(gene)
    print()

if __name__=="__main__":
    main()
