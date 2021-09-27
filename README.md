## INTRODUCTION ##
BioIntersect (Beta version) is a program developed to help geneticists with little to no experience in programming to run their own genetics coordinates intersections.
Especially helpful for Windows-based computer users, since Windows is not compatible with Bedtools, a well-known intersection software.


## INPUT FILES FORMAT ##
The program takes two inputs (have to be in the same folder as the .py file):
- Input 1: genomic coordinates of interest. No file header.
	"chr_name"	"coord_start"	"coord_end"
	chr01		123				12345
	chr02		4567			67858
	chr02		5678			34536
- Input 2: genomic coordinates of interest - with description (optional). No file header.
	"chr_name"	"coord_start"	"coord_end"		"description"
	chr01		123				1234			geneA
	chr02		4567			67858			geneB
	chr03		5678			34536			geneC_mutated

IMPORTANT!
- Input file names will be requested when program starts.
- Two sets of input examples are provided.


## OUTPUTS ##	
The output files consist of:
- A Venn diagram displaying the number of intersections between input1 and input2 (venn.png)
- A barplot displaying the number of intersected coordinates per chromosome (barplot.png)
- A .bed file displaying the intersection coordinates (output.csv)
	"chr_name"	"intersect_start"	"intersect_end"	"intersect_length"	"description"
	chr01		123					1234			1112				geneA
	chr02		4567				67858			63292				geneB

Three windows will be automatically displayed after the program finishes runnning.
Click "Load intersection table!" if you wish to see the intersection table.
It is possible to edit the table and write the modifications back to the original file (using "Write modifications" button).


## BEFORE FIRST USE ##
1. Install Python 3 (version 3.7 or higher) or Anaconda 3
	2. If installing stand-alone Python 3: Double-click "installing_dependencies.exe" to install dependencies.


## RUNNING THE PROGRAM ##
1. Open Windows cmd or Anaconda prompt
2. Type "cd <path to folder where your program files are>"
3. Type "python biointersect.py"
