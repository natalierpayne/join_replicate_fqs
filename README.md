# Find and join replicate fastqs
Concatenate fastq files containing reads from replicate samples.

When utilizing Stacks to process RADseq data, fastq files are produced for each sample, with forward and reverse reads stored in separate files (denoted as ‘.1.fq’ and ‘.2.fq’). In RADseq experiments, it is common for several replicate samples to be included within and between sequencing libraries to calculate genotyping error rates and optimize SNP-calling parameters. The reads from replicate samples can then be combined to achieve higher coverage for these samples.

The purpose of join_replicate_fqs.py is to identify files in the same directory belonging to replicate samples, based on file naming conventions specified by the user, and subsequently concatenate them. Separation between forward and reverse reads is maintained. It can optionally accept gzipped fastq files such as those produced by the process_radtags program in Stacks. 

Users can optionally choose to save concatenated files to a specified output directory. It is also possible to identify replicate fastqs and copy them to a new directory without concatenating them, which could be useful for identifying only replicate samples to use for error rate calculation.

## Installation
To install the program, run the following:
```
git clone https://github.com/natalierpayne/join_replicate_fqs.git
```
The program relies on having Python 3 installed (written with Python 3.9.6), but no extra dependencies are required to run the program! Pylint and flake8 may be used when running the test suite, and THESE CAN BE INSTALLED WITH ______.

## Usage
```
usage: join_replicate_fqs.py [-h] -f FILE [FILE ...] [-o str] [-d str] [-c] [-e] [-s] PATTERN [PATTERN ...]

Join fastqs of replicate samples

positional arguments:
  PATTERN               Pattern(s) denoting replicates in filenames

optional arguments:
  -h, --help            show this help message and exit
  -f FILE [FILE ...], --files FILE [FILE ...]
                        Input fq or fq.gz file(s) (default: None)
  -o str, --outdir str  Directory to output concatenated files (default: )
  -d str, --dir str     Directory to output extracted files (default: )
  -c, --concatenate     Concatenate replicate files (default: False)
  -e, --extract         Extract replicate files (default: False)
  -s, --silent          Silence warnings (default: False)
  ```
  The program takes two required arguments: one or more patterns denoting replicate files (for example, _WR for within-library replicates and _BR for between-library replicates) and input filenames. The program will search among all provided input files for replicate files and the matching original files.
  
  The program is directed to concatenate replicate files and/or extract and copy them to a separate directory using the -c and -e options, respectively. For example, to concatenate replicates within the sample fastq files in the provided inputs directory:
  ```
  ./join_replicate_fqs.py _WR -f inputs/*.fq -co concat_dir
  ```
  where -o precedes the name of the directory where concatenated files will be saved.
  
  To extract replicates from the sample fastq files and copy them to a separate directory:
  ```
  ./join_replicate_fqs.py _WR -f inputs/*.fq -ed extract_dir
  ```
  where -d indicates the name of the directory the replicate files will be copied to.
  
  The previous two sample commands can also be run using the Makefile:
  ```
  make run_concat
  make run_extract
  ```
  It is also possible for the user to specify both concatenation and extraction:
  ```
  ./join_replicate_fqs.py _WR -f inputs/*.fq -co concat_dir -ed extract_dir
  ```
  To help prevent unwanted overwriting of files, the program also provides warnings when users specify output directories that already exist or do not specify a separate directory to store concatenated files. Users can choose to proceed anyway by typing 'y' when prompted. Users can choose to silence the warnings with the -s flag.
  ```
  $ ./join_replicate_fqs.py _WR -f inputs/*.fq -c
Warning: Are you sure you want to write output to the current directory (y/n)?
  ```
  Expected outputs when running concatenation or extraction with .fq or .fq.gz sample files from the inputs/ folder are available in the expected/ folder. In the output from --concatenate, sequences from the same samples and same direction are saved to the same file. Therefore, some sequence IDs will contain the user-specified pattern denoting replicates, while others will not. Note sequence IDs ending in "REV" represent reverse sequences, and these are kept separate from forward reads.
  ```
  $ head expected/concat/*
==> expected/concat/ind_1.1.fq <==
@IND_1_SEQ_1
AAAA
+
::::
@IND_1_SEQ_2
TTTT
+
::::
@IND_1_WR_SEQ_1
AATT

==> expected/concat/ind_1.2.fq <==
@IND_1_SEQ_1_REV
AAAA
+
::::
@IND_1_SEQ_2_REV
TTTT
+
::::
@IND_1_WR_SEQ_1_REV
AATT
  ```
  In the output of --extract, only replicate files (those containing the user-specified pattern or matching files belonging to the same samples) are copied. Note ind_2.1.fq and ind_2.2.fq were not extracted from the input files because they are not duplicated (there are no matching filenames containing _WR).
  ```
  $ head expected/extract/*
==> expected/extract/ind_1.1.fq <==
@IND_1_SEQ_1
AAAA
+
::::
@IND_1_SEQ_2
TTTT
+
::::
==> expected/extract/ind_1.2.fq <==
@IND_1_SEQ_1_REV
AAAA
+
::::
@IND_1_SEQ_2_REV
TTTT
+
::::
==> expected/extract/ind_1_WR.1.fq <==
@IND_1_WR_SEQ_1
AATT
+
::::
@IND_1_WR_SEQ_2
TTAA
+
::::
==> expected/extract/ind_1_WR.2.fq <==
@IND_1_WR_SEQ_1_REV
AATT
+
::::
@IND_1_WR_SEQ_2_REV
TTAA
+
::::
  ```
  
  When running the program with gzipped files, gzipped output files will be produced. When gunzipped, the content of these files will be identical to that of the outputs produced when running the program with non-gzipped files.
  ```
  ./join_replicate_fqs.py _WR -f inputs/*.gz -co concat_dir -ed extract_dir
  gunzip concat_dir/*
  gunzip extract_dir/*
  ```
  
  ## Testing
  A passing test suite should look like this:
  ```
  $ make test
  pytest -xv --pylint --flake8 test.py join_replicate_fqs.py
===================================================== test session starts =====================================================
platform linux -- Python 3.9.6, pytest-6.2.5, py-1.10.0, pluggy-1.0.0 -- /usr/local/bin/python3
cachedir: .pytest_cache
rootdir: /home/nataliermercer/be_project/join_replicate_fqs
plugins: flake8-1.0.7, mypy-0.8.1, pylint-0.18.0
collected 16 items                                                                                                            
--------------------------------------------------------------------------------
Linting files
..
--------------------------------------------------------------------------------

test.py::PYLINT PASSED                                                                                                  [  6%]
test.py::FLAKE8 PASSED                                                                                                  [ 12%]
test.py::test_exists PASSED                                                                                             [ 18%]
test.py::test_usage PASSED                                                                                              [ 25%]
test.py::test_dies_bad_file PASSED                                                                                      [ 31%]
test.py::test_dies_no_task PASSED                                                                                       [ 37%]
test.py::test_dies_o_without_c PASSED                                                                                   [ 43%]
test.py::test_dies_d_without_e PASSED                                                                                   [ 50%]
test.py::test_dies_e_without_d PASSED                                                                                   [ 56%]
test.py::test_dies_bad_pattern PASSED                                                                                   [ 62%]
test.py::test_fqs_concat PASSED                                                                                         [ 68%]
test.py::test_fqs_extract PASSED                                                                                        [ 75%]
test.py::test_fqs_concat_extract PASSED                                                                                 [ 81%]
test.py::test_gz_concat_extract PASSED                                                                                  [ 87%]
join_replicate_fqs.py::PYLINT PASSED                                                                                    [ 93%]
join_replicate_fqs.py::FLAKE8 PASSED                                                                                    [100%]

===================================================== 16 passed in 3.15s ======================================================
  ```
