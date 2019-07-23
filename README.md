# ACMG 59
I wrote these Python files to facilitate the usage of the EVcouplings-EVfold software in my project on the ACMG 59 genes (list of clinically actionable disease genes maintained by the American College of Medical Genetics and Genomics).
I am currently working on this project for my MIT(Massachusetts Institute of Technology) UROP(Undergraduate Research Opportunities Program) as a research intern at Harvard Medical School.

# extend.py
Draws extendable regions from existing EVcouplings-EVfold alignment data and directly executes commands for extending those regions.
Extends regions by
1. joining consecutive regions that satisfy the rule and
2. stretching 50 amino acids both to the left and to the right if an isolated region satisfies the rule.

# stats.py
Extracts all existing EVcouplings-EVfold alignment data for input gene,
arranges and prints data in comma-separated form so that it can be copied and pasted to spreadsheet right away.

# outputCoords.py
Helper function for extend.py and stats.py.
Obtains all existing file paths for specified gene.
