import re
from setuptools import setup
 
 
version = re.search(
    '^__version__\s*=\s*"(.*)"',
    open('seqrep/seqrep.py').read(),
    re.M
    ).group(1)

setup(
    name = "seqrep_py",
    packages = ["seqrep"],
    entry_points = {
        "console_scripts": ['seqrep = seqrep.seqrep:main']
        },
    version = version,
    description = "Generate multiple .pdf reports of sequencing data.",
    long_description = "TODO",
    author = "Taylor Stevens",
    author_email = "tayste5000@gmail.com"
    )