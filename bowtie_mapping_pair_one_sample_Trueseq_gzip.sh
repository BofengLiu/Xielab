#!/bin/bash

files=$1
file=${files%_r1.fq.gz}

trim_galore --paired $files $file\_r2.fq.gz --dont_gzip


echo "" >> $file\mapping_log.txt
echo "$file\_mapping_info" >> $file\mapping_log.txt
bowtie2 -t -q -p 96 -N 1 -L 25 -X 2000 --no-mixed --no-discordant -x ./mm9 -1 $file\_r1_val_1.fq -2 $file\_r2_val_2.fq > $file\_pair.sam 2>> $file\mapping_log.txt
perl ./rm_cut.pl $file\_pair.sam > $file\_pair_cleaned.sam
bash ./rm_polyclonal.sh mm9 $file\_pair_cleaned rmdup
grep "^@" $file\_pair.sam > $file\_pmu.sam
nohup samtools view $file\_pair_cleaned.bam | awk '$3~/chr[0-9]|X|Y/' - | grep -v 'XS:i:' | grep -v random | grep -v chrM >> $file\_pmu.sam &

samtools view -@ 16 -b -S $file\_pair.sam > $file\_pair.bam
samtools view -@ 16 -b -S $file\_pmu.sam > $file\_pmu.bam

rm metrics.txt
rm -r ./tmp_dir
grep -v Time $file\mapping_log.txt | grep -v full-index | grep -v Overall | grep -v Warning > $file\mapping_log_tmp.txt
sed 's/\\_/_/g' $file\mapping_log_tmp.txt > $file\mapping_log.txt
rm $file\mapping_log_tmp.txt
rm $file\_cut1.fq
rm $file\_cut2.fq
rm $file\_pair_cleaned.bam
rm $file\_pair_cleaned.sam
rm $file\_r1_val_1.fq
rm $file\_r2_val_2.fq
rm $file\_pair_cleaned.withdup.bam
#rm $file\_pair.sam &
#rm $file\_pmu.sam & 
