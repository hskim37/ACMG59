from __future__ import print_function
from outputCoords import outputCoords
import sys
import os
from log import log

def stats(ID,gene):
    paths = outputCoords(gene) # list of strings
    
    smallAreas = []
    
    for path in paths[:4]:
        if int((path.split('_')[0]).split('-')[1])-int((path.split('_')[0]).split('-')[0])<99:
            paths.remove(path)
            smallAreas.append(path)

    geneLen = max([int((x.split('_')[0]).split('-')[1]) for x in paths])
    index = (geneLen//100)*4
    paths[index:index] = smallAreas
    
    errorList = []
    
    for path in paths:
        
        region = path.split('_')[0]
        thresh = (path.split('_')[1]).split('-')[0]
        
        csv = '/n/scratch2/rg252/ACMG59_NEW/{}/{}/align/{}_alignment_statistics.csv'.format(gene,path,path)
        
        try:
            with open(csv) as f:
                stats = ((f.readlines())[1]).split(',')
            path,mincov,nseqs,seqlen,ncov,nlc,perc,fuc,luc,lencov,nlcov,neff = stats
            newlist = [nseqs,seqlen,perc,fuc,luc,neff]
            joinedstr = ','.join(newlist)
            
            print('HUMAN,{},{},{},{},{}'.format(ID,gene,region,thresh,joinedstr),end='')
            
        except IOError:
            print('HUMAN,{},{},{},{}'.format(ID,gene,region,thresh))
            start,end = region.split('-')
            errorList.append((start,end,thresh))        
            
    commandList = []
    
    if len(errorList)>0:

        for error in errorList:
            start,end,thresh = error
            commandList.append('sbatch -o /n/scratch2/rg252/ACMG59_NEW/outFiles/{}_{}-{}_{}-0.5_out.txt config.sh {} {} 0.5 {} {}'
                .format(gene,start,end,thresh,gene,thresh,start,end))
            print('\n{}_{}-{}_{}-0.5'.format(gene,start,end,thresh),end='')
            
        if (raw_input('\n\nExecute? Y / N -> ')).lower()=='y':
            for command in commandList:
                 print('\n{}'.format(command))
                 os.system(command)
                 log(command)

def main():
    ID = sys.argv[1]
    gene = sys.argv[2]
    print()
    stats(ID,gene)
    print()
    
if __name__=="__main__":
    main()
