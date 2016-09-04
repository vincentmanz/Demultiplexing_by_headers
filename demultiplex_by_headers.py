#!/usr/bin/python
from Bio import SeqIO
import collections
import time
import os
import multiprocessing
import gzip
import argparse
from datetime import datetime
import sys


startTime = datetime.now()

#make a new directory for the analyses, day/time
now = ((time.strftime("%Y_%m_%d")) + "_" + (time.strftime("%H.%M.%S")))
print(now + '\n')
os.mkdir(now)

indexes_list = []

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--ifile", type=str, help="Input file", required=True)
	parser.add_argument("-t", "--thread", type=int, help="Input Number of threads", default=[2])
	parser.add_argument("-m", "--min_reads", type=int, help="Minimum reads per barcode [OPTIONAL]", default=[1])
	parser.add_argument("-l", "--length", type=int, help="Length of the barcode", default=[15], required=True)
	parser.add_argument("-L", "--list", type=str, help="List of barcodes[OPTIONAL]")

	args = parser.parse_args()
	filegz = args.ifile
	nproc = args.thread
	min_reads_per_barcodes = args.min_reads
	length = args.length

print('Input file is: ' + filegz)
print('Number of threads is: ' + str(nproc))
print('Minimum reads per barcode is: ' + str(min_reads_per_barcodes))
print('The length of the barcode is: ' + str(length))
if args.list:
	list_barcode = open(args.list, 'r')
	indexes_list = list_barcode.read().splitlines()
	print('The list of barcode is on the file: ' + args.list)

#file to open
filename = gzip.open(filegz, 'rt')


def demultiplex(barcode):
	'''write the new file with associated barcode'''
	filename = gzip.open(filegz, 'rt')
	for seq_record in (SeqIO.parse(filename, "fastq")):
		header = seq_record.description
		if header[-length:] == str(barcode):
			new_file = barcode + '_' + '.fastq.gz'
			with gzip.open('./' + now + '/' + new_file, 'a') as file:
				SeqIO.write(seq_record, file, "fastq")


def parse_file(barcodes_set, iteration):

	'''This function start the different processes'''
	if __name__ == '__main__':
		procs = []
		n = 0
		for i in range(iteration):
			n = 1 + n
			p = multiprocessing.Process(target=demultiplex, args=(barcodes_set[-n],))
			p.start()
			procs.append(p)
		for p in procs:
			p.join()

#print freq_barcodes denovo
if not indexes_list:
	list_header = []
	for seq_record in SeqIO.parse(filename, "fastq"):
		list_header.append(seq_record.description[-length:])
		freq_barcodes = collections.Counter(list_header)
	number_barcodes = len(freq_barcodes)
	print('\n\nBarcodes list and abondance:')
	for key, value in sorted(freq_barcodes.iteritems(), key=lambda (k,v): (v,k)):
		if value > min_reads_per_barcodes:
			print "%s: %s" % (key, value)
	sorted_freq_barcodes = sorted(freq_barcodes.iteritems(), key=lambda (k,v): (v,k))
else:
	number_barcodes = len(indexes_list)
	sorted_freq_barcodes = indexes_list
	print '\nNumber of barcodes provided from the file:', number_barcodes

#loop x by X according to the number of proc.
start = number_barcodes - nproc
end = number_barcodes
if start < 0:
	start = 0

for bar in (range(int(number_barcodes / nproc + 1))):
	if start < 0:
		start = 0
	iteration = end - start
	if not indexes_list:
		barcodes = dict(sorted_freq_barcodes[start:end])
		barcodes_set = barcodes.keys()
	else:
		barcodes_set = sorted_freq_barcodes[start:end]
	parse_file(barcodes_set, iteration)
	start = start - nproc
	end = end - nproc
print(datetime.now() - startTime)

print('Done!')
