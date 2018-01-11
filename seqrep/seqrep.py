from .cmdparser import parser
from .functions import prep_excel, gen_reports
import os, sys
from openpyxl import load_workbook
import subprocess

__version__ = "0.0.1"

def main():
    # Get command line arguments
    args = parser.parse_args()

    # Make sure that a proper directory has been provided
    if not os.path.isdir(args.sequencing_dir):
        sys.exit('{} is not a directory'.format(args.sequencing_dir))

    # Read the file names from this directory
    files = os.listdir(args.sequencing_dir)

    # Fail if there is already a reports directory
    if 'reports' in files:
        sys.exit('''{} already contains /reports directory.
            Please remove the directory to run this script'''.format(args.sequencing_dir))

    # Name of spreadsheet to generate
    excel_name = 'report.xlsx'

    # If the spreadsheet is already there skip to gen_reports
    if excel_name in files:
        
        wb = load_workbook(os.path.join(args.sequencing_dir,'report.xlsx'))

        gen_reports(args.sequencing_dir, wb, line_length=60)

    # If the -edit argument was specified, only generate the spreadsheet and then open it
    elif args.edit:

        _ = prep_excel(args.sequencing_dir, files, args.template_seq, excel_name)

        subprocess.run(['open', os.path.join('.', args.sequencing_dir, excel_name)])

    # Run all functions
    else:

        wb = prep_excel(args.sequencing_dir, files, args.template_seq, excel_name)

        gen_reports(args.sequencing_dir, wb, line_length=60)