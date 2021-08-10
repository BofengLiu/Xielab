genomeHeader=./$1/$1.fa.fai
input=$2
dup=$3

samtools view -@ 16 -bt $genomeHeader $input.sam | samtools sort - -@ 16 -o $input.withdup.bam  
# remove duplicate if indicated
if [ $dup == "rmdup" ];
then
echo "Removing duplicates ...."
java -Xmx8g -jar ./picard-tools-1.119/MarkDuplicates.jar INPUT=$input.withdup.bam OUTPUT=$input.bam METRICS_FILE=$input\_metrics.txt REMOVE_DUPLICATES=true ASSUME_SORTED=true TMP_DIR=$input\_tmp_dir
else
mv $input.withdup.bam $input.bam
fi

#rm $input.bam.bai
#rm $input.withdup.bam
rm $input\_metrics.txt
rm -r $input\_tmp_dir
#rm $input.sam
#
# index bam file
#samtools index $input.bam
