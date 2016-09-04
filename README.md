In some cases, sequencing centers will put the barcode sequences in the fastq labels before handing it off. It is important to know the exact length of the barcode:

This script is demultiplexing fastq.gz file based on the header barcode using multi processors. 


In some cases, sequence barcodes are not provided in a separate file, or a dual barcoding strategy may have been applied during sequencing. From the headers, the script will generate a list of barcodes that will be used to demultiplex the file. 

#Dependencies 
	Biopython: [sudo] pip install biopython


```
**Example of headers:**
    Dual indexed
        @M01132:152:000000000-AUA7D:1:1102:16025:1335 1:N:0:ACGCAAC+CCGATTG
        GGTGATATTGTTTGTTATCGTTTAATATTGCGCTATATTTTAAAAAAGCTATATTTATTCCCGTATATACTCGGCGATTGCTAAATTCACAATTATATTTTTTGTTTATCATTCAATTCAGATAAAAAACAACGATAAATTGATTCTAAAAAAGAAATGAGGTTATAAAGACATTAAGAAAACAGGCAATAAAATATAGCGATCGAAACACGTTAACAAAATGAGTCTCATTATCAGAGTAGGACAACAGG
        +
        AAAA>FFFFDBFGFFGGGGGFGEHBBGGHDG?GGAFHFFFGFGDFHEEHHHHFHHHHHHHHHGGEHHHHFFHGFGE>EHGBGHHHHHHGGHHHGHHHHHHGHGGGHCEGHHHHHGHHHHHHEHGFHHHCGEHECFHGGHGHHHHHHHFHDGB@?FG<FGEHHHFHHGHFHGHHHHHHHHHHHHHHEEHHHHGHHHGGHHGGGEECGGFGGGGFGGGGGGEFGFGGFFFGFGGGGGGFBFFFFF/BBFFFFF

    Single indexing
        @MISEQ03:64:000000000-A2H3D:1:1101:14358:1530 1:N:0:TCCACAGGAGT
        TNCAGAGGGTGCAAGCGTTAATCGGAATTACTGGGCGTAAAGCGCGCGTAGGTGGTTTGTTAAGTTGGATGTGAAATCCCCGGGCTCAACCTGGGAACTGCATTCAAAACTGACAAGCTAGAGTATGGTAGAGGGTGGTGGAATTTCCTGTGTAGCGGTGAAATGCGTAGATATAGGAAGGAACACCAGTGGCGAAGGCGACCACCTGGACTGAAACTGACACTGAGGGGCGAAAGCGGGGGGGGCAAACG
        +
        ?#5<????DDDDDDDDEEEEFFHHHHHHHHHHHHHHDCCHHFGDEHEH>CCE5AEEHHHHHHHHHHHHHHHHHFFFFHHHHHHEEADEEEEEEEEEEEEEEEEEEEEEEE?BEEEEEEEEEEEAEEEE0?A:?EE)8;)0ACEEECECCECAACEE?>)8CCC?CCA8?88ACC*A*::A??:0?C?.?0:?8884>'.''..'0?8C?C**0:0::?ECEE?############################
       
```


```
usage: Demultiplex_by_headers2.0.py [-h] -i IFILE [-t THREAD] [-m MIN_READS]
                                    -l LENGTH [-L LIST]

optional arguments:
  -h, --help            show this help message and exit
  -i IFILE, --ifile IFILE
                        Input file
  -t THREAD, --thread THREAD
                        Input Number of threads
  -m MIN_READS, --min_reads MIN_READS
                        Minimum reads per barcode [OPTIONAL]
  -l LENGTH, --length LENGTH
                        Length of the barcode
  -L LIST, --list LIST  List of barcodes[OPTIONAL]
```

List of barcodes:
	The file containing the list of indexes should be identical to the header in the fastq file. 




```
**Example:**
    Dual indexed
        @M01132:152:000000000-AUA7D:1:1102:16025:1335 1:N:0:ACGCAAC+CCGATTG
        GGTGATATTGTTTGTTATCGTTTAATATTGCGCTATATTTTAAAAAAGCTATATTTATTCCCGTATATACTCGGCGATTGCTAAATTCACAATTATATTTTTTGTTTATCATTCAATTCAGATAAAAAACAACGATAAATTGATTCTAAAAAAGAAATGAGGTTATAAAGACATTAAGAAAACAGGCAATAAAATATAGCGATCGAAACACGTTAACAAAATGAGTCTCATTATCAGAGTAGGACAACAGG
        +
        AAAA>FFFFDBFGFFGGGGGFGEHBBGGHDG?GGAFHFFFGFGDFHEEHHHHFHHHHHHHHHGGEHHHHFFHGFGE>EHGBGHHHHHHGGHHHGHHHHHHGHGGGHCEGHHHHHGHHHHHHEHGFHHHCGEHECFHGGHGHHHHHHHFHDGB@?FG<FGEHHHFHHGHFHGHHHHHHHHHHHHHHEEHHHHGHHHGGHHGGGEECGGFGGGGFGGGGGGEFGFGGFFFGFGGGGGGFBFFFFF/BBFFFFF

    List barcode:
        ACGCAAC+CCGATTG
    
    Command line:
        If you have a list of barcodes:
            python Demultiplex_by_headers.py -i file.fastq.gz -t 8 -l 15 -L index.list
        
        If you do not have a list of barcodes
            python Demultiplex_by_headers.py -i file.fastq.gz -t 8 -l 15 -m 1000
```