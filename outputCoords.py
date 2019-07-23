# Takes gene as input
# Obtains and returns list of region_threshold as strings from actual output results
import os

def outputCoords(gene):
    path = '/n/scratch2/rg252/ACMG59_NEW/%s' %gene
    fullList = os.listdir(path)
    filtered = [x for x in fullList if (os.path.isdir(os.path.join(path,x)) and x!='output' and not x.startswith('.'))]
    final = sorted(filtered,key=lambda x:((int((x.split('_')[0]).split('-')[-1]))-(int(x.split('-')[0])),int(x.split('-')[0]),int((x.split('_')[0]).split('-')[-1]),float((x.split('_')[-1]).split('-')[0])))
    return final