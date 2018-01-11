from openpyxl import Workbook
import os, sys
import numpy as np
import skbio.alignment, skbio.sequence
from xhtml2pdf import pisa
from .formatting import format_html, format_seq_line

pisa.showLogging()

def prep_excel(sequencing_dir, files, template_seq_name, excel_name='report.xlsx'):
    '''
    Extract the sequence from each sequencing file and generate a
    spreadsheet that matches each sequence with a template sequence and 
    indicates whether it is a forward or reverse sequence.

    Parameters
    ----------

    template_seq: str
        The default template sequence to align all query sequences to

    template_seq_name: str
        The name of the file which contains the template sequence

    sequencing_dir: str
        The path to the directory which contains all of the sequencing files

    excel_name: str
        The name of the spreadsheet file to generate
    '''

    # Make a spreadsheet and add the desired columns
    wb = Workbook()
    ws = wb.active
    ws.append(['Filename', 'Rev?', 'Construct', 'Sequence', 'Template Sequence'])

    print("Reading files in {}...\r".format(sequencing_dir))

    # Parse the template sequence
    if template_seq_name:
        with open(template_seq_name) as template_seq_file:
            template_seq = template_seq_file.read()
            template_seq = template_seq.lower() # Make lower case
            template_seq = template_seq.strip() # Remove \n

    else:
        template_seq = ''

    # Add a row for each sequence
    for file in files:
        filename = os.path.join(sequencing_dir,file)

        try:
            # Extract the actual sequence and add to spreadsheet
            with open(filename) as seq_file:
                seq = ''.join([x.strip() for x in seq_file.readlines()])
                seq = seq.lower() # Make lower case
                seq = seq.strip() # Remove \n

            isrev = 'rev' in file
            ws.append([file, isrev, template_seq_name or '', seq, template_seq ])
        except:
            # TODO: generate a custom error instance for this that deletes extra stuff
            sys.exit('''Error occured with {}. Make sure there are only sequencing files in the directory.'''.format(filename))

    print("Generating {}...\r".format(os.path.join(sequencing_dir, excel_name)))

    # Save the file
    wb.save(os.path.join(sequencing_dir, excel_name))

    return wb

def get_match_str(a,b):
    bool_val = np.array(list(a)) == np.array(list(b))
    list_val = np.where(bool_val,'|','-')
    list_val = list(list_val)
    string_val = ''.join(list_val)
    return string_val

def gen_aligned_seqs(a, overhangs=50):
    '''
    Generate formatted strings from the alignment object generated
    by skbio.sequence.DNA

    parameters
    ----------

    a : ??? (skbio.sequence.DNA output)
        The alignment object producted by skbio.sequence.DNA

    overhangs : int
        The number of bases from unaligned regions of the sequence flanking
        the alignment to include in the output
    '''

    # The overhang length could be limited by the positioning of the aligned
    # regions within the query and target sequences
    start_overhang = min(a.query_begin, a.target_begin, overhangs)

    end_overhang = min(len(a.query_sequence) - 1 - a.query_end,
        len(a.target_sequence) - 1 - a.target_end_optimal,
        overhangs)

    # Get the overhanging strings
    query_overhangs = [
        a.query_sequence[a.query_begin-start_overhang:a.query_begin],
        a.query_sequence[a.query_end+1:a.query_end+end_overhang]
    ]

    target_overhangs = [
        a.target_sequence[a.target_begin-start_overhang:a.target_begin],
        a.target_sequence[a.target_end_optimal+1:a.target_end_optimal+end_overhang]
    ]

    # Add the overhangs to the aligned sequences
    query_sequence_ex = a.aligned_query_sequence.join(query_overhangs)
    target_sequence_ex = a.aligned_target_sequence.join(target_overhangs)

    # Generate the match string
    match_str = get_match_str(query_sequence_ex, target_sequence_ex)

    return query_sequence_ex, target_sequence_ex, match_str

def gen_reports(sequencing_dir, wb, line_length=60):
    '''
    Take an excel spreadsheet containing alignment inputs, generate the alignments, 
    and produce a .pdf file for each alignment

    parameters
    ----------

    sequencing_dir : str
        The path to the directory which contains all of the sequencing files
    wb : ??? (openpyxl workbook object)
        openpyxl object of the spreadsheet which contains the alignment input data
    line_length : int
        The number of characters per each line in the formatted alignment
    '''

    # Make the reports directory
    report_dirname = os.path.join(sequencing_dir, 'reports')

    print('Generating {}.'.format(report_dirname))
    os.mkdir(report_dirname)

    # Get rows and column labels from the spreadsheet
    ws = wb.get_active_sheet()

    rows = list(ws.rows)
    header = list(map(lambda x: x.value, rows.pop(0)))

    # Make a custom substition matrix to allow alignments of sequences with 'N' nucleotides
    mtrx = skbio.alignment.make_identity_substitution_matrix(1, -2, alphabet='ACGTN')

    # Iterate through the rows
    for row in rows:

        # Make row into a dict with column name as the index
        row_vals = map(lambda x: x.value, row)
        row_dict = dict(zip(header,row_vals))

        # Convert to reverse complement if reverse sequence
        if row_dict['Rev?']:
            sequence = skbio.sequence.DNA(row_dict['Sequence'].strip(),lowercase=True).reverse_complement()
            row_dict['Sequence'] = str(sequence)

        # Generate alignment
        print("Aligning {} to {}\r".format(row_dict['Filename'], row_dict['Construct']))
        a = skbio.alignment.StripedSmithWaterman(row_dict['Sequence'].lower())(row_dict['Template Sequence'].lower())

        # Get the sequence position where the alignment starts
        query_begin = a.query_begin
        target_begin = a.target_begin

        # format alignment
        query_sequence, target_sequence, match_str = gen_aligned_seqs(a)

        # Initialize formatted alignment string
        seq = ''

        # Split the alignment up into fragments according to line_length and format
        for i in range(len(query_sequence) // line_length + 1):
            a = query_sequence[0+i*line_length:line_length+i*line_length]
            b = target_sequence[0+i*line_length:line_length+i*line_length]
            match = match_str[0+i*line_length:line_length+i*line_length]

            # Determine the actually sequence length covered by the line
            a_length = len(a) - a.count('-')
            b_length = len(b) - b.count('-')

            # Format
            seq += format_seq_line(a, b, match,
                (query_begin, query_begin+a_length-1),
                (target_begin, target_begin+b_length-1))

            # Increment length
            query_begin += a_length
            target_begin += b_length

        # Prepare into html file
        html = format_html(row_dict['Filename'], row_dict['Construct'], seq)

        # Generate .pdf file
        basename = row_dict['Filename'].split('.')[0]
        report_filename = os.path.join(report_dirname, '{}.pdf'.format(basename))

        with open(report_filename, "w+b") as reportFile:
            # convert HTML to PDF
            pisaStatus = pisa.CreatePDF(
                html,
                dest=reportFile)