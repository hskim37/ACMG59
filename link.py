from __future__ import print_function
from outputCoords_tako import outputCoords
import sys
import os

def link(gene):
    allPaths = outputCoords(gene) # ['1-100_0.3-0.5','1-100_0.5-0.5',...]
    ruleSatisfied = []
    pre = '/net/data/acmg59'
    
    for path in allPaths:
        csv = '{}/{}/{}/align/{}_alignment_statistics.csv'.format(pre,gene,path,path)
        with open(csv) as f:
            stats = ((f.readlines())[1]).split(',')
        source,mincov,nseqs,seqlen,ncov,nlc,perc,fuc,luc,lencov,nlcov,neff = stats
        
        seqlen = int(seqlen)
        
        if seqlen>100 and float(neff) >= 4.5*seqlen: # Leaves only the maximum threshold
            ruleSatisfied.append((path,seqlen))
            
    ruleSatisfied.sort(key=lambda x:x[1],reverse=True)
    
    for path,seqlen in ruleSatisfied:
        print('{} | {}'.format(seqlen,path))
    
    minlen = int(raw_input('\nDesired minimum length -> '))
    
    
    commands = ['ln -s {}/{}/{} {}/final/{}/'.format(pre,gene,path,pre,gene) for path,seqlen in ruleSatisfied if seqlen>=minlen]
    
    dirList = os.listdir('{}/final'.format(pre))
    if gene not in dirList:
        print('\nMaking directory...\n')
        os.system('mkdir {}/final/{}'.format(pre,gene))
    
    for command in commands:
        print('{}'.format(command))
        os.system(command)

def main():
    gene = sys.argv[1]
    print()
    link(gene)
    print()

if __name__=="__main__":
    main()
