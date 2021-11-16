#!/usr/bin/env python

"""
Script to generate passwords.txt data file from Richelieu top passwords dataset file
"""

import argparse
import codecs
import logging
import os
import sys

# Default parameters
default_encoding = 'utf8'

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
    help='Input Richelieu top passwords file path',
)

in_opts = parser.add_argument_group('Input options')

in_opts.add_argument(
    '-e', '--encoding',
    type=str,
    dest='encoding',
    help='Input file encoding (default: %s)' % default_encoding,
    default=default_encoding
)


out_opts = parser.add_argument_group('Output options')

out_opts.add_argument(
    '-o', '--output',
    type=str,
    dest='output',
    help='Output directory (Default: same as input Richelieu file)',
)

out_opts.add_argument(
    '-L', '--limit',
    type=int,
    dest='limit',
    help='Limit number of password to export in output file. Top ranked passwords will be keep. (Default: no limit)',
)

options = parser.parse_args()

if not options.input:
    parser.error('You must specify input Richelieu top passwords file path as first positional parameter.')

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

passwords = []

with open(options.input, encoding=options.encoding) as fd:
    if options.progress:
        import progressbar
        line_count = sum(1 for line in fd.readlines())
        fd.seek(0)
        c = 0
        class PasswordsCount(progressbar.Widget):  # pylint: disable=too-few-public-methods
            """ Progress bar widget to show how many passwords are already loaded """
            def update(self, *args):  # pylint: disable=unused-argument
                global passwords
                return '(%d passwords)' % len(passwords)

        pbar = progressbar.ProgressBar(
            widgets=[
                "Load top passwords from input file %s: " % options.input,
                progressbar.Percentage(),
                ' ',
                progressbar.Bar(),
                ' ',
                progressbar.SimpleProgress(),
                ' ',
                PasswordsCount(),
                ' ',
                progressbar.ETA()
            ],
            maxval=line_count
        ).start()
    else:
        log.info("Load top passwords from input file %s ... ", options.input)
    for row in fd.readlines():
        password = row.strip()
        if password:
            passwords.append(password)
        if options.progress:
            c += 1
            pbar.update(c)

    if options.progress:
        pbar.finish()

output_path = os.path.join(options.output, 'passwords.txt')
log.info('Export passwords in %s...', output_path)
with codecs.open(output_path, 'w', 'utf8') as fd:
    count = 0
    total = len(passwords)
    for idx, password in enumerate(passwords if not options.limit else passwords[:options.limit]):
        rank = total - idx
        fd.write(u"%s    %d\n" % (password, rank))
