#!/usr/bin/env python
"""This is a program to convert the process .txt files into a standard wig file
for use in other analysis programs such as IGB"""
"""Save excel file into tab delimted txt file with the following format:
Chromosome Start Signal"""
 
__version__ = "0.1"
__description__ = ""

import sys
import os
from optparse import OptionParser

hg18_chr_len={"chr1":247249719,"chr1_random":1663265,"chr10":135374737,"chr10_random":113275,"chr11":134452384,"chr11_random":215294,"chr12":132349534,"chr13":114142980,"chr13_random":186858,"chr14":106368585,"chr15":100338915,"chr15_random":784346,"chr16":88827254,"chr16_random":105485,"chr17":78774742,"chr17_random":2617613,"chr18":76117153,"chr18_random":4262,"chr19":63811651,"chr19_random":301858,"chr2":242951149,"chr2_random":185571,"chr20":62435964,"chr21":46944323,"chr21_random":1679693,"chr22":49691432,"chr22_random":257318,"chr22_h2_hap1":63661,"chr3":199501827,"chr3_random":749256,"chr4":191273063,"chr4_random":842648,"chr5":180857866,"chr5_random":143687,"chr5_h2_hap1":1794870,"chr6":170899992,"chr6_random":1875562,"chr6_cox_hap1":4731698,"chr6_qbl_hap2":4565931,"chr7":158821424,"chr7_random":549659,"chr8":146274826,"chr8_random":943810,"chr9":140273252,"chr9_random":1146434,"chrM":16571,"chrX":154913754,"chrX_random":1719168,"chrY":57772954}

mm9_chr_len={"chr1":197195432,"chr2":181748087,"chrX":166650296,"chr3":159599783,"chr4":155630120,"chr5":152537259,"chr7":152524553,"chr6":149517037,"chr8":131738871,"chr10":129993255,"chr14":125194864,"chr9":124076172,"chr11":121843856,"chr12":121257530,"chr13":120284312,"chr15":103494974,"chr16":98319150,"chr17":95272651,"chr18":90772031,"chr19":61342430,"chrY_random":58682461,"chrY":15902555,"chrUn_random":5900358,"chrX_random":1785075,"chr1_random":1231697,"chr8_random":849593,"chr17_random":628739,"chr9_random":449403,"chr13_random":400311,"chr7_random":362490,"chr5_random":357350,"chr4_random":160594,"chr3_random":41899,"chrM":16299,"chr16_random":3994}

hg19_chr_len={"chr1":249250621,"chr2":243199373,"chrX":155270560,"chr3":198022430,"chr4":191154276,"chr5":180915260,"chr7":159138663,"chr6":171115067,"chr8":146364022,"chr10":135534747,"chr14":107349540,"chr9":141213431,"chr11":135006516,"chr12":133851895,"chr13":115169878,"chr15":102531392,"chr16":90354753,"chr17":81195210,"chr18":78077248,"chr19":59128983,"chrY":59373566,"chr20":63025520,"chr21":48129895,"chr22":51304566}


#hg19_chr_len={"chr1":249250621,"chr2":243199373,"chr3":198022430,"chr4":191154276,"chr5":180915260,"chr6":171115067,"chr7":159138663,"chrX":155270560,"chr8":146364022,"chr9":141213431,"chr10":135534747,"chr11":135006516,"chr12":133851895,"chr13":115169878,"chr14":107349540,"chr15":102531392,"chr16":90354753,"chr17":81195210,"chr18":78077248,"chr20":63025520,"chrY":59373566,"chr19":59128983,"chr22":51304566,"chr21":48129895,"chr6_ssto_hap7":4928567,"chr6_mcf_hap5":4833398,"chr6_cox_hap2":4795371,"chr6_mann_hap4":4683263,"chr6_apd_hap1":4622290,"chr6_qbl_hap6":4611984,"chr6_dbb_hap3":4610396,"chr17_ctg5_hap1":1680828,"chr4_ctg9_hap1":590426,"chr1_gl000192_random":547496,"chrUn_gl000225":211173,"chr4_gl000194_random":191469,"chr4_gl000193_random":189789,"chr9_gl000200_random":187035,"chrUn_gl000222":186861,"chrUn_gl000212":186858,"chr7_gl000195_random":182896,"chrUn_gl000223":180455,"chrUn_gl000224":179693,"chrUn_gl000219":179198,"chr17_gl000205_random":174588,"chrUn_gl000215":172545,"chrUn_gl000216":172294,"chrUn_gl000217":172149,"chr9_gl000199_random":169874,"chrUn_gl000211":166566,"chrUn_gl000213":164239,"chrUn_gl000220":161802,"chrUn_gl000218":161147,"chr19_gl000209_random":159169,"chrUn_gl000221":155397,"chrUn_gl000214":137718,"chrUn_gl000228":129120,"chrUn_gl000227":128374,"chr1_gl000191_random":106433,"chr19_gl000208_random":92689,"chr9_gl000198_random":90085,"chr17_gl000204_random":81310,"chrUn_gl000233":45941,"chrUn_gl000237":45867,"chrUn_gl000230":43691,"chrUn_gl000242":43523,"chrUn_gl000243":43341,"chrUn_gl000241":42152,"chrUn_gl000236":41934,"chrUn_gl000240":41933,"chr17_gl000206_random":41001,"chrUn_gl000232":40652,"chrUn_gl000234":40531,"chr11_gl000202_random":40103,"chrUn_gl000238":39939,"chrUn_gl000244":39929,"chrUn_gl000248":39786,"chr8_gl000196_random":38914,"chrUn_gl000249":38502,"chrUn_gl000246":38154,"chr17_gl000203_random":37498,"chr8_gl000197_random":37175,"chrUn_gl000245":36651,"chrUn_gl000247":36422,"chr9_gl000201_random":36148,"chrUn_gl000235":34474,"chrUn_gl000239":33824,"chr21_gl000210_random":27682,"chrUn_gl000231":27386,"chrUn_gl000229":19913,"chrM":16571,"chrUn_gl000226":15008,"chr18_gl000207_random":4262}

yh_chr_len={"chr1":247249719,"chr1_random":1663265,"chr10":135374737,"chr10_random":113275,"chr11":134452384,"chr11_random":215294,"chr12":132349534,"chr13":114142980,"chr13_random":186858,"chr14":106368585,"chr15":100338915,"chr15_random":784346,"chr16":88827254,"chr16_random":105485,"chr17":78774742,"chr17_random":2617613,"chr18":76117153,"chr18_random":4262,"chr19":63811651,"chr19_random":301858,"chr2":242951149,"chr2_random":185571,"chr20":62435964,"chr21":46944323,"chr21_random":1679693,"chr22":49691432,"chr22_random":257318,"chr22_h2_hap1":63661,"chr3":199501827,"chr3_random":749256,"chr4":191273063,"chr4_random":842648,"chr5":180857866,"chr5_random":143687,"chr5_h2_hap1":1794870,"chr6":170899992,"chr6_random":1875562,"chr6_cox_hap1":4731698,"chr6_qbl_hap2":4565931,"chr7":158821424,"chr7_random":549659,"chr8":146274826,"chr8_random":943810,"chr9":140273252,"chr9_random":1146434,"chrM":16571,"chrX":154913754,"chrX_random":1719168,"chrY":57772954}

dm6_chr_len={"chr3R":32079331,"chr3L":28110227,"chr2R":25286936,"chrX":23542271,"chr2L":23513712,"chrY":3667352}

dm3_chr_len={"chr2L":23011544,"chr2LHet":368872,"chr2R":21146708,"chr2RHet":3288761,"chr3L":24543557,"chr3LHet":2555491,"chr3R":27905053,"chr3RHet":2517507,"chr4":1351857,"chrU":10049037,"chrUextra":29004656,"chrX":22422827,"chrXHet":204112,"chrYHet":347038,"chrM":19517}


def main():

    usage = "usage: %prog species File"
    parser = OptionParser(usage, description=__description__,
            version=__version__)
    parser.add_option("-v", "--verbose",
                    action="store_true", dest="verbose")

    (opts, args) = parser.parse_args()
    
    if len(args) < 2:
        print(usage)
        sys.exit()

    infileName = args[1]
    outfileName = args[1] + '.cleaned'
    tmpName = args[1] + '.tmp'
    species = args[0] 
    if species == "mm9": chr_len = mm9_chr_len
    elif species == "hg18": chr_len = hg18_chr_len
    elif species == "hg19": chr_len = hg19_chr_len
    elif species == "yh": chr_len = yh_chr_len
    elif species == "dm6": chr_len = dm6_chr_len
    elif species == "dm3": chr_len = dm3_chr_len
    else: print("genome length is required!")
    infile = open(infileName, 'r')
    #print "Header is skipped ..."
    #infile.next() # skip the head line
    outfile = open(outfileName, 'w')
    #outfile.write("track type=bedGraph\n")
    for line in infile:
        line = line.strip()
        field = line.split('\t')
        chr = field[0]
        start = int(field[1])  
        end = int(field[2])
	#print chr_len[chr]
	if start <= 0 or end <= 0: continue
	if start >= chr_len[chr] or end >= chr_len[chr]: continue
        outfile.write("%s\t%s\t%s" %(chr,str(start), str(end)))
	if len(field) >= 3: 
		for item in field[3:]:
			outfile.write("\t%s" %item)
	outfile.write("\n")

    os.popen("mv %s %s" %(infileName,tmpName))
    os.popen("mv %s %s" %(outfileName,infileName))
 
if __name__ == "__main__":
    main()
