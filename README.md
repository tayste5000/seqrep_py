# seqrep_py
Generate .pdf reports sequence alignments from a directory of query sequences.

Required dependencies:

Python 3.5
openpyxl
numpy
scikitbio
xhtml2pdf

How to install:

This project is not on pip yet, so the only way to install is to copy this repository
onto your computer, and then run 'python setup.py install' in the root directory of the repo

How to use:

Once you have installed seqrep you can use it from the command line. Seqrep is supposed to 
be used on a directory that contains nothing but sequencing results in plaintext format. Additionaly,
you should specify a template sequence (also a plaintext file) to align all of the sequencing results to.
Seqrep is called  in the following way: 'seqrep sequencing_dir template_seq'. You can add the -e flag
if you would like to make manual changes to how the files are aligned, such as whether they are in the
forward or reverse direction (seqrep looks for the string 'rev' in each sequencing result name in an 
attempt to do this automatically) or if you would like to use alternate template sequences. Doing
this will create an excel file detailing the alignment in the same directory where you are running the command.
After you make changes to the excel file you can then rerun seqrep, it will detect the excel file and start from this 
file to generate the output.
