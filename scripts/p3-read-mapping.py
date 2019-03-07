#!/usr/bin/env python
import argparse
import sys
#import read_mapping_tools
import os.path
import re
import subprocess

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A script to map fastq reads to a set of genes of interest, e.g. MLST alleles.',
            usage='usage: p3-read-mapping.py --pe read1.fq:read2.fq --se reads.fq --sequence_set seq.fasta --kma_index name')

    parser.add_argument('--pe', required=False, help='Paired-end fastq files (read1.fq:read2.fq)')
    parser.add_argument('--se', required=False, help='Single-end fastq file')
    parser.add_argument('--output_directory', required=True, help='Output directory')
    parser.add_argument('--sequence_set_fasta', required=False, help='alternate allele sequences (fasta)')
    parser.add_argument('--sequence_kma_index', required=False, help='indexed allele sequences for kma')
    parser.add_argument('--kma_options', default="-and")

    args = parser.parse_args()
    print args
    if not args.output_directory:
        sys.exit("Output directory must be specified")

    filebase = "x"
    if args.se:
        m = re.match(r"\w+", os.path.basename(args.se))
        if m:
            filebase = m.group(0)
    elif args.pe:
        file1 = args.pe.split(':')[0]
        m = re.match(r"\w+", os.path.basename(file1))
        if m:
            filebase = m.group(0)
    filebase += "_vs_"+os.path.basename(args.sequence_kma_index).replace(r"\..*", "")
    if not os.path.exists(args.output_directory):
        os.mkdir(args.output_directory)
    command = "kma -t_db "+args.sequence_kma_index
    command += " -o "+os.path.join(args.output_directory, filebase)
    if args.se:
        command += " -i "+args.se
    elif args.pe:
        command += " -ipe "+" ".join(args.pe.split(":"))
    command += " "+args.kma_options

    print command
    subprocess.call(command.split(" "))

