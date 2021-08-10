#!/bin/bash
###############################################################################
# 
# Author: screamfever
# Created Time: Tue Aug 10 07:08:10 2021
# 
###############################################################################

echo "input read1 fastq file\n"
files=$1

bash bowtie_mapping_pair_one_sample_Trueseq_gzip.sh $files
wait
bash sam2bw_chip_total.sh mm9 ${files%_r1.fq.gz}_pmu.sam temp

