""" Tests for join_replicate_fqs.py """

import os
import re
from subprocess import getstatusoutput
from shutil import rmtree

PRG = './join_replicate_fqs.py'


# --------------------------------------------------
def test_exists():
    """ Program exists """

    assert os.path.isfile(PRG)


# --------------------------------------------------
def test_usage():
    """ Program prints usage statement with help flag """

    for flag in ['-h', '--help']:
        rv, out = getstatusoutput(f'{PRG} {flag}')
        assert rv == 0
        assert out.lower().startswith('usage')


# --------------------------------------------------
def test_dies_bad_file():
    """ Program fails with nonexistent file """

    rv, out = getstatusoutput(f'{PRG} oo -f foo')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search("foo does not exist. Please provide valid filename.", out)


# -------------------------------------------------
def test_dies_no_task():
    """ Program fails without -c or -e"""

    suffix = '_WR'
    rv, out = getstatusoutput(f'{PRG} {suffix} -f inputs/*.fq')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search('join_replicate_fqs.py: error:', out)


# -------------------------------------------------
def test_dies_o_without_c():
    """ Program fails when -o used without -c"""

    suffix = '_WR'
    rv, out = getstatusoutput(f'{PRG} {suffix} -f inputs/*.fq -o')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search('join_replicate_fqs.py: error:', out)


# -------------------------------------------------
def test_dies_d_without_e():
    """ Program fails when -d used without -e"""

    suffix = '_WR'
    rv, out = getstatusoutput(f'{PRG} {suffix} -f inputs/*.fq -d')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search('join_replicate_fqs.py: error:', out)


# -------------------------------------------------
def test_dies_e_without_d():
    """ Program fails when -e used without -d"""

    suffix = '_WR'
    rv, out = getstatusoutput(f'{PRG} {suffix} -f inputs/*.fq -e')
    assert rv != 0
    assert out.lower().startswith('usage:')
    assert re.search('join_replicate_fqs.py: error:', out)


# --------------------------------------------------
def test_dies_bad_pattern():
    """ Program fails to find replicates with bad pattern """

    rv, out = getstatusoutput(f'{PRG} foo -f inputs/*.fq -ed exdir')
    assert rv != 0
    assert out == ("No replicates were found! Check ['foo'] is correct.")
    if os.path.isdir('exdir'):
        rmtree('exdir')


# -------------------------------------------------
def test_fqs_concat():
    """ Program concatenates replicate fq files """

    suffix = '_WR'
    rv, out = getstatusoutput(f'{PRG} {suffix} -f inputs/*.fq -c -o outdir')
    assert rv == 0
    assert out == ''
    assert os.path.isdir('outdir')
    assert os.path.isfile('outdir/ind_1.1.fq')
    assert os.path.isfile('outdir/ind_1.2.fq')
    with open('outdir/ind_1.1.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_SEQ_1',
                                               'AAAA',
                                               '+',
                                               '::::',
                                               '@IND_1_SEQ_2',
                                               'TTTT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_1',
                                               'AATT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_2',
                                               'TTAA',
                                               '+',
                                               '::::'])

    with open('outdir/ind_1.2.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_SEQ_1_REV',
                                               'AAAA',
                                               '+',
                                               '::::',
                                               '@IND_1_SEQ_2_REV',
                                               'TTTT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_1_REV',
                                               'AATT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_2_REV',
                                               'TTAA',
                                               '+',
                                               '::::'])
    if os.path.isdir('outdir'):
        rmtree('outdir')


# -------------------------------------------------
def test_fqs_extract():
    """ Program extracts replicate fq files """

    suffix = '_WR'
    rv, out = getstatusoutput(f'{PRG} {suffix} -f inputs/*.fq -e -d outdir')
    assert rv == 0
    assert out == ''
    assert os.path.isdir('outdir')
    assert os.path.isfile('outdir/ind_1.1.fq')
    assert os.path.isfile('outdir/ind_1_WR.1.fq')
    assert os.path.isfile('outdir/ind_1.2.fq')
    assert os.path.isfile('outdir/ind_1_WR.2.fq')
    with open('outdir/ind_1.1.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_SEQ_1',
                                               'AAAA',
                                               '+',
                                               '::::',
                                               '@IND_1_SEQ_2',
                                               'TTTT',
                                               '+',
                                               '::::'])

    with open('outdir/ind_1_WR.1.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_WR_SEQ_1',
                                               'AATT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_2',
                                               'TTAA',
                                               '+',
                                               '::::'])

    with open('outdir/ind_1.2.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_SEQ_1_REV',
                                               'AAAA',
                                               '+',
                                               '::::',
                                               '@IND_1_SEQ_2_REV',
                                               'TTTT',
                                               '+',
                                               '::::'])

    with open('outdir/ind_1_WR.2.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_WR_SEQ_1_REV',
                                               'AATT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_2_REV',
                                               'TTAA',
                                               '+',
                                               '::::'])
    if os.path.isdir('outdir'):
        rmtree('outdir')


# # -------------------------------------------------
def test_fqs_concat_extract():
    """ Program concatenates and extracts replicate files """

    rv, out = getstatusoutput(f'{PRG} _WR -f inputs/*.fq -co catdir -ed exdir')
    assert rv == 0
    assert out == ''
    assert os.path.isdir('catdir')
    assert os.path.isfile('catdir/ind_1.1.fq')
    assert os.path.isfile('catdir/ind_1.2.fq')
    with open('catdir/ind_1.1.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_SEQ_1',
                                               'AAAA',
                                               '+',
                                               '::::',
                                               '@IND_1_SEQ_2',
                                               'TTTT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_1',
                                               'AATT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_2',
                                               'TTAA',
                                               '+',
                                               '::::'])

    with open('catdir/ind_1.2.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_SEQ_1_REV',
                                               'AAAA',
                                               '+',
                                               '::::',
                                               '@IND_1_SEQ_2_REV',
                                               'TTTT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_1_REV',
                                               'AATT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_2_REV',
                                               'TTAA',
                                               '+',
                                               '::::'])
    if os.path.isdir('catdir'):
        rmtree('catdir')

    assert os.path.isdir('exdir')
    assert os.path.isfile('exdir/ind_1.1.fq')
    assert os.path.isfile('exdir/ind_1_WR.1.fq')
    assert os.path.isfile('exdir/ind_1.2.fq')
    assert os.path.isfile('exdir/ind_1_WR.2.fq')
    with open('exdir/ind_1.1.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_SEQ_1',
                                               'AAAA',
                                               '+',
                                               '::::',
                                               '@IND_1_SEQ_2',
                                               'TTTT',
                                               '+',
                                               '::::'])

    with open('exdir/ind_1_WR.1.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_WR_SEQ_1',
                                               'AATT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_2',
                                               'TTAA',
                                               '+',
                                               '::::'])

    with open('exdir/ind_1.2.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_SEQ_1_REV',
                                               'AAAA',
                                               '+',
                                               '::::',
                                               '@IND_1_SEQ_2_REV',
                                               'TTTT',
                                               '+',
                                               '::::'])

    with open('exdir/ind_1_WR.2.fq', encoding='utf-8') as fh:
        assert fh.read().strip() == '\n'.join(['@IND_1_WR_SEQ_1_REV',
                                               'AATT',
                                               '+',
                                               '::::',
                                               '@IND_1_WR_SEQ_2_REV',
                                               'TTAA',
                                               '+',
                                               '::::'])
    if os.path.isdir('exdir'):
        rmtree('exdir')
