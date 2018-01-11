import argparse

# Generate an argparse object to run the command line process
parser = argparse.ArgumentParser(description='''Generate an excel
    spreadsheet that pairs sequencing results with the template
    sequence that they should be aligned to for assesment of successful
    cloning.''')


# Input of a directory name that contains all sequencing
# results is required
parser.add_argument('sequencing_dir', help='path to a directory containing nothing but sequence files.')

# The name of a file containing a
# template sequence can be supplied
parser.add_argument('template_seq', help='plaintext file containing the sequence that you want the results aligned to.')

# If you want to edit the spreadsheet before 
# generating the report
parser.add_argument('-e', '--edit', action='store_true', help='change specifications of the report before generating.')