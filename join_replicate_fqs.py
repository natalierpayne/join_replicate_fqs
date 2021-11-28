#!/usr/bin/env python3
"""
Author : nataliermercer <nataliermercer@localhost>
Date   : 2021-11-17
Purpose: Join fastqs of replicate samples
"""

import argparse
import os
import sys
import re

# pylint:disable=too-many-locals,consider-using-with,unspecified-encoding,too-many-branches,too-many-statements


# --------------------------------------------------
def get_args():
    """Get command-line arguments"""

    parser = argparse.ArgumentParser(
        description='Join fastqs of replicate samples',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('pattern',
                        metavar='PATTERN',
                        type=str,
                        nargs='+',
                        help='Pattern(s) denoting replicates in filenames')

    parser.add_argument('-f',
                        '--files',
                        help='Input gzipped fastq file(s)',
                        metavar='FILE',
                        type=str,
                        nargs='+',
                        required=True,
                        default=None)

    parser.add_argument('-o',
                        '--outdir',
                        help='Directory to output concatenated files',
                        metavar='str',
                        type=str,
                        default='')

    parser.add_argument('-d',
                        '--dir',
                        help='Directory to output extracted files',
                        metavar='str',
                        type=str,
                        default='')

    parser.add_argument('-c',
                        '--concatenate',
                        help='Concatenate replicate files',
                        action='store_true')

    parser.add_argument('-e',
                        '--extract',
                        help='Extract replicate files',
                        action='store_true')

    parser.add_argument('-s',
                        '--silent',
                        help='Silence warnings',
                        action='store_true')

    args = parser.parse_args()

    for fh in args.files:
        if not os.path.isfile(fh):
            parser.error(f'{fh} does not exist.' +
                         ' Please provide valid filename.')

    if not args.concatenate:
        if not args.extract:
            parser.error('What would you like me to do?' +
                         ' Please use one or both of --concatenate' +
                         ' or --extract')

    if args.outdir:
        if not args.concatenate:
            parser.error('Please use --concatenate' +
                         ' to use the --outdir option')

    if args.dir:
        if not args.extract:
            parser.error('Please use --extract to use the --dir option')

    if args.extract:
        if not args.dir:
            parser.error('Please specify where to copy' +
                         ' the extracted files with --dir')

    return args


# --------------------------------------------------
def main():
    """Make a jazz noise here"""

    args = get_args()

    if args.outdir:
        if not os.path.isdir(args.outdir):
            os.mkdir(args.outdir)
        elif not args.silent:
            cont = input(f'Warning: The directory "{args.outdir}"' +
                         ' already exists!' +
                         ' Are you sure you want to continue (y/n)?')
            if cont == 'n':
                sys.exit('Okay, see you next time!')

    if args.dir:
        if not os.path.isdir(args.dir):
            os.mkdir(args.dir)
        elif not args.silent:
            cont = input(f'Warning: The directory "{args.dir}"' +
                         ' already exists!' +
                         ' Are you sure you want to continue (y/n)?')
            if cont == 'n':
                sys.exit('Okay, see you next time!')

    if args.concatenate and not args.silent:
        if not args.outdir:
            cont = input('Warning: Are you sure you want to write' +
                         ' output to the current directory (y/n)?')
            if cont == 'n':
                sys.exit('Okay, see you next time!')

    reps = []

    for fh in args.files:
        for pattern in args.pattern:
            if re.search(pattern, fh):
                reps.append(fh)

    if reps == []:
        sys.exit(f'No replicates were found! Check {args.pattern} is correct.')

    rep_sample_names = []

    for fh in reps:
        for pattern in args.pattern:
            if pattern in fh:
                rep_sample_names.append(re.sub(pattern, '', fh))

    # print(rep_sample_names)
    # print(reps)

    for name in set(rep_sample_names):
        basename = os.path.basename(name)
        root, _ext = os.path.splitext(basename)
        filename, direction = os.path.splitext(root)
        for rep in reps:
            if filename and direction in rep:
                # print(name, rep) # inspect pairing
                fh1 = open(name).read()
                fh2 = open(rep).read()
                # gz going to need special handling here, right???
                if args.concatenate:
                    if args.outdir:
                        outfile = ''.join(args.outdir + '/' + basename)
                    else:
                        outfile = basename
                    if not os.path.isfile(outfile):
                        with open(outfile, 'wt', encoding='utf8') as fh:
                            fh.write(fh1 + '\n')
                    with open(outfile, 'at', encoding='utf8') as fh:
                        fh.write(fh2 + '\n')

                if args.extract:
                    original_file = ''.join(args.dir + '/' + basename)
                    rep_file = ''.join(args.dir + '/' +
                                       os.path.basename(rep))
                    with open(original_file, 'wt', encoding='utf8') as fh:
                        fh.write(fh1 + '\n')
                    with open(rep_file, 'wt', encoding='utf8') as fh:
                        fh.write(fh2 + '\n')

# gz
# FH.name to save mem?
# Typing info?


# --------------------------------------------------
if __name__ == '__main__':
    main()
