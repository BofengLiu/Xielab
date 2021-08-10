#!/bin/bash
EXPECTED_ARGS=3
if [ $# -ne $EXPECTED_ARGS ];
then
echo "Usage: '$0' genome samFile web_folder"
exit
fi

web_folder=$3
input=${2%.sam}
chr_len_bed=./$1/$1_chr_len_bed
genomeHeader=./$1/$1.fa.fai
get_count=./get_counts_gw.pl
wig2bigwig=./wig2bigwig.sh
cleanwig=./clean_chr_boundary.py
chr=./GO.bed2wig_$1_wei
chr_len=./$1/$1_chr_len.txt

echo $input

samtools view -bt $genomeHeader $input.sam | bamToBed -i - | cut -f1-3 | sort -k1,1 -k2,2n > $input.short
$get_count $input.short 100 $chr_len_bed > $input\_rpk.wig &
total_read=`wc -l $input.short`
factor=`echo $total_read | cut -f1 -d" "`

if [ $factor -gt 1000000 ];
then
mfactor=$((factor/1000000)) ### Here it is actually /1,000,000 * 10 = 100,000 to get 1kb per million
elif [ $factor -gt 100000 ];
then
mfactor=$((factor/100000))
else
mfactor=$((factor/10000))
fi
echo "$input\t$mfactor"


slopBed -i $input.short -g $chr_len -l 0 -r 250 -s > $input.long.bed
$chr $input.long.bed 1 $1
awk '{printf "%s\t%d\t%d\t%.2f\n",$1,$2,$3,(($4*10)/('$mfactor'*3))}' $input.long.bed.min1.wig | egrep -v "chrM" | grep -v "_" > $input.wig
$cleanwig $1 $input.wig
sort -k1,1 -k2,2n $input.wig > $input\_sort.wig
mv $input\_sort.wig $input.wig
$wig2bigwig $1 $input.wig
mv $input.wig $input\_300bp_rpkm.wig
awk '{printf "%s\t%d\t%.2f\n",$1,($2+$3)/2,$4}' $input\_300bp_rpkm.wig > $input\_300bp_rpkm.tsv &

#### for calculation #####

#$get_count $input.short 100 $chr_len_bed > $input\_rpk.wig
awk '{printf "%s\t%d\t%d\t%.2f\n",$1,$2,$3,($4*10)/'$mfactor'}' $input\_rpk.wig | egrep -v "chrM" | grep -v "_" > $input\_100bp_rpkm.wig
$cleanwig $1 $input\_100bp_rpkm.wig
echo "$input\_cal_wig_cleaned"

awk '{printf "%s\t%d\t%.2f\n",$1,($2+$3)/2,$4}' $input\_100bp_rpkm.wig > $input\_100bp_rpkm.tsv

rm $input.short
rm $input\_rpk.wig
rm $input.long.bed*
rm $input*.wig.tmp
