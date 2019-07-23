# EVcouplings-EVfold

extend.py
Draws extendable regions from existing EVcouplings-EVfold alignment data and directly executes commands for extending those regions.
Extends regions by
1) joining consecutive regions that satisfy the rule and
2) stretching 50 amino acids both to the left and to the right if an isolated region satisfies the rule.

stats.py
Extracts all existing EVcouplings-EVfold alignment data for input gene,
arranges and prints data in comma-separated form so that it can be copied and pasted to spreadsheet right away.
