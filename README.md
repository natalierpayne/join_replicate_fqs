# join_replicate_fqs
Concatenate fastq files containing reads from replicate samples.

When utilizing Stacks to process RADseq data, fastq files are produced for each sample, with forward and reverse reads stored in separate files (denoted as ‘.1.fq’ and ‘.2.fq’). In RADseq experiments, it is common for several replicate samples to be included within and between sequencing libraries to calculate genotyping error rates and optimize SNP-calling parameters. The reads from replicate samples can then be combined to achieve higher coverage for these samples.

The purpose of join_replicate_fqs.py is to identify files in the same directory belonging to replicate samples, based on file naming conventions specified by the user, and subsequently concatenate them. Separation between forward and reverse reads is maintained. It can accept gzipped fastq files such as those produced by the process_radtags program in Stacks. 

Users can optionally choose to save concatenated files to a specified output directory. It is also possible to identify replicate fastqs and copy them to a new directory without concatenating them, which could be useful for identifying only replicate samples to use for error rate calculation.
