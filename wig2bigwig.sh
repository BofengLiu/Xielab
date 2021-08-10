#!/bin/bash
cleanwig=./clean_chr_boundary.py

input=${2%.wig} 
$cleanwig $1 $input.wig
bedGraphToBigWig $input.wig ./$1/$1_chromInfo.txt $input.bw
