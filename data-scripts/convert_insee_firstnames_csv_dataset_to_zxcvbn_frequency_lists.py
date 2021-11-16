#!/usr/bin/env python

"""
Script to generate male_names.txt and female_names.txt data files
from INSEE CSV dataset file
"""

import argparse
import codecs
import csv
import logging
import os
import sys
from unidecode import unidecode

# Default parameters
default_delimiter = ';'
default_encoding = 'utf8'
default_unusual_firstname = '_PRENOMS_RARES'

### MAIN ####
parser = argparse.ArgumentParser(description=__doc__)

parser.add_argument(
    '-d', '--debug',
    action='store_true',
    help='Show debug messages'
)

parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    help='Show verbose messages'
)

parser.add_argument(
    '-w', '--warning',
    action='store_true',
    help='Show warning messages'
)

parser.add_argument(
    '-l', '--log-file',
    action="store",
    type=str,
    dest="logfile",
    help="Log file path"
)

parser.add_argument(
    '-C', '--console',
    action='store_true',
    help='Also log on console (even if log file is provided)'
)

parser.add_argument(
    '-p', '--progress',
    action="store_true",
    dest="progress",
    help="Show progress bar"
)

parser.add_argument(
    type=str,
    dest='input',
    help='CSV input file path',
)

csv_opts = parser.add_argument_group('CSV options')

csv_opts.add_argument(
    '-D', '--delimiter',
    type=str,
    dest='delimiter',
    help='CSV input file delimiter character (default: %s)' % default_delimiter,
    default=default_delimiter
)

csv_opts.add_argument(
    '-e', '--encoding',
    type=str,
    dest='encoding',
    help='CSV input file encoding (default: %s)' % default_encoding,
    default=default_encoding
)

csv_opts.add_argument(
    '--unusual-firstname',
    type=str,
    dest='unusual_firstname',
    help='CSV input file unusual firstname replacement string (default: "%s")' % default_unusual_firstname,
    default=default_unusual_firstname
)


out_opts = parser.add_argument_group('Output options')

out_opts.add_argument(
    '-o', '--output',
    type=str,
    dest='output',
    help='Output directory (Default: same as input CSV file)',
)

out_opts.add_argument(
    '-n', '--normalize',
    action='store_true',
    help='Add normalized firstname (if differ from raw firstname)'
)

out_opts.add_argument(
    '-L', '--limit',
    type=int,
    dest='limit',
    help='Limit number of firstname by gender to export in output files. Top ranked firstnames will be keep. (Default: no limit)',
)

options = parser.parse_args()

if not options.input:
    parser.error('You must specify input CSV file path as first positional parameter.')

if not options.output:
    options.output = os.path.dirname(options.input)

# Initialize log
log = logging.getLogger()
logformat = logging.Formatter("%(asctime)s - " + os.path.basename(sys.argv[0]) + " - %(levelname)s : %(message)s")

if options.debug:
    log.setLevel(logging.DEBUG)
elif options.verbose:
    log.setLevel(logging.INFO)
elif options.warning:
    log.setLevel(logging.WARNING)
else:
    log.setLevel(logging.FATAL)

if options.logfile:
    logfile = logging.FileHandler(options.logfile)
    logfile.setFormatter(logformat)
    log.addHandler(logfile)

if not options.logfile or options.console:
    logconsole = logging.StreamHandler()
    logconsole.setFormatter(logformat)
    log.addHandler(logconsole)

firstnames = {
    'male': {},
    'female': {},
}



#sexe;preusuel;annais;nombre
#2;ZYNA;2012;6
with open(options.input, encoding=options.encoding) as fd:
    if options.progress:
        import progressbar
        line_count = sum(1 for line in fd.readlines()) - 1
        fd.seek(0)
        c = 0
        class FirstnameCount(progressbar.Widget):  # pylint: disable=too-few-public-methods
            """ Progress bar widget to show how many firstnames are already loaded """
            def update(self, *args):  # pylint: disable=unused-argument
                global firstnames
                return '(%s)' % ', '.join(['%s: %i' % (gender, len(firstnames[gender])) for gender in firstnames])

        pbar = progressbar.ProgressBar(
            widgets=[
                "Load firstnames from input file %s: " % options.input,
                progressbar.Percentage(),
                ' ',
                progressbar.Bar(),
                ' ',
                progressbar.SimpleProgress(),
                ' ',
                FirstnameCount(),
                ' ',
                progressbar.ETA()
            ],
            maxval=line_count
        ).start()
    else:
        log.info("Load firstnames from input file %s ... ", options.input)
    csvfile = csv.DictReader(fd, delimiter=options.delimiter)
    for row in csvfile:
        if options.progress:
            c += 1
            pbar.update(c)

        firstname = row['preusuel']
        if firstname == options.unusual_firstname:
            continue

        firstname = firstname.lower()
        if row['sexe'] == '1':
            gender = 'male'
        elif row['sexe'] == '2':
            gender = 'female'
        else:
            log.warning('Column sexe value "%s" not recognized (complete line: %s)', row['sexe'], row)
            continue

        if firstname not in firstnames[gender]:
            firstnames[gender][firstname] = int(row['nombre'])
        else:
            firstnames[gender][firstname] += int(row['nombre'])

        if options.normalize:
            normalized_firstname = unidecode(firstname)
            if normalized_firstname != firstname:
                if normalized_firstname not in firstnames[gender]:
                    firstnames[gender][normalized_firstname] = int(row['nombre'])
                else:
                    firstnames[gender][normalized_firstname] += int(row['nombre'])

    if options.progress:
        pbar.finish()

for gender in firstnames:
    output_path = os.path.join(options.output, '%s_names.txt' % gender)
    log.info('Export %s firstnames in %s...', gender, output_path)
    with codecs.open(output_path, 'w', 'utf8') as fd:
        count = 0
        for firstname in sorted(firstnames[gender].keys(), key=lambda x: firstnames[gender][x], reverse=True):
            fd.write(firstname + "\n")
            count += 1
            if options.limit and count >= options.limit:
                log.info('Output limit of %i firtnames to export in output files expected for %s', options.limit, gender)
                break
