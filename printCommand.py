from __future__ import print_function
import sys
import os

def printCommand(gene):
    finalPaths = os.listdir('/net/data/acmg59/final/{}'.format(gene)) # ['1-100_0.3-0.5','1-100_0.5-0.5',...]
        
    for path in finalPaths:
        start = int((path.split('_')[0]).split('-')[0])
        end = int((path.split('_')[0]).split('-')[-1])
        bit = float((path.split('_')[-1]).split('-')[0])
        
        print('sbatch -o /n/scratch2/rg252/ACMG59_NEW/outFiles/{}_out.txt config.sh {} 0.5 {} {}'.format(gene,bit,start,end))

def main():
    gene = sys.argv[1]
    print()
    printCommand(gene)
    print()
    
if __name__=="__main__":
    main()
