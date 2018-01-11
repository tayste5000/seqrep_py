css = '''<style>
body{
    font-family: monospace;
}
p{
    margin: 0;
    -pdf-keep-with-next: true;
}
</style>'''

seq_line_template = '''
<p><br>&nbsp;&nbsp;{a_start:0>4}&nbsp;&nbsp;{a}&nbsp;&nbsp;{a_end:0>4}<br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{match}<br>
&nbsp;&nbsp;{b_start:0>4}&nbsp;&nbsp;{b}&nbsp;&nbsp;{b_end:0>4}</p>'''

def format_seq_line(a, b, match, a_range, b_range):

    return seq_line_template.format(a=a,
        a_start=a_range[0],
        a_end=a_range[1],
        match=match,b=b,
        b_start=b_range[0],
        b_end=b_range[1])

html_template = '''
<html><head>{}</head><body>
<p>Sequence: {}</p><br>
<p>Template sequence: {}.</p><br>{}</body>'''

def format_html(seq_file, construct_file, alignment):

    return html_template.format(css, seq_file, construct_file, alignment)