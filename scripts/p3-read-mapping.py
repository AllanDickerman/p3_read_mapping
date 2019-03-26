#!/usr/bin/env python
import argparse
import sys
#import read_mapping_tools
import os.path
import re
import subprocess
import sra_tools

def fetch_sra_files(args):
    """ 
    call external library sra_tools to download and unpack fastq files
    Add resulting file(s) to -pe or -se section of args
    """
    sys.stderr.write("fetch_sra_files() args.sra="+" ".join(args.sra)+"\n")
    for sra in args.sra:
        runinfo = sra_tools.get_runinfo(sra)

        sys.stderr.write("downloading %s\n"%sra)
        sra_tools.ftp_download_single_run(sra)

        if not os.path.exists(sra+".sra"):
            raise Exception("Problem: file %s.sra does not exist after trying to download %s\n"%(sra, sra_file_url))

        if runinfo['LibraryLayout'].startswith("SINGLE"):
            sra_tools.fastqDumpExistingSraFile(sra+".sra", splitFiles=False)
            if not os.path.exists(sra+".fastq"):
                raise Exception("Problem: file %s.fastq does not exist after running fastq-dump on %s.sra\n"%(sra, sra))
            if not args.se:
                args.se = []
            args.se.append(sra+".fastq")
        elif runinfo['LibraryLayout'].startswith("PAIRED"):
            sra_tools.fastqDumpExistingSraFile(sra+".sra", splitFiles=True)
            if not (os.path.exists(sra+"_1.fastq") and os.path.exists(sra+"_2.fastq")):
                raise Exception("Problem: file %s_1.fastq and/or %s_2.fastq do not exist after running fastq-dump --split-files on %s.sra\n"%(sra, sra, sra))
            if not args.pe:
                args.pe = []
            args.pe.append(sra + "_1.fastq:" + sra +"_2.fastq")
    return

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='A script to map fastq reads to a set of genes of interest, e.g. MLST alleles.',
            usage='usage: %s --pe read1.fq:read2.fq --se reads.fq --sra SRRxxxx --kma_index name'%sys.argv[0])

    parser.add_argument('--pe', nargs='*', metavar="read1.fq:read2.fq", help='Paired-end fastq files (read1.fq:read2.fq). Allow multiple.')
    parser.add_argument('--se', nargs='*', metavar="reads.fq", help='Single-end fastq file. Allows multiple.')
    parser.add_argument('--sra', nargs='*', metavar="SRRxxx", help='SRA run accession (SRR12345). Allows multiple.')
    parser.add_argument('-o', '--output_directory', metavar="DIR", default=".", help='Output directory.')
    parser.add_argument('-b', '--output_file_base', metavar="PREFIX", help='Base name for output files.')

    parser.add_argument('--kma_index', required=True, help='Indexed sequences for kma.')
    parser.add_argument('--kma_options', nargs='*', metavar="OPT", default=["-and"])

    args = parser.parse_args()
    print args

    if not (args.se or args.pe or args.sra):
        raise Exception("No input file was specified.")

    if not args.output_file_base:
        filebase = None
        if args.se:
            filebase = args.se[0]
        elif args.pe:
            filebase = args.pe[0].split(':')[0]
        elif args.sra:
            filebase = args.sra[0]
        filebase = os.path.basename(filebase)
        m = re.match(r"\w+", filebase)
        if m:
            filebase = m.group(0)
        filebase += "_vs_"+os.path.basename(args.kma_index).replace(r"\..*", "")
        args.output_file_base = filebase

    if args.sra:
        fetch_sra_files(args)

    if not os.path.exists(args.output_directory):
        os.mkdir(args.output_directory)
    command = "kma -t_db "+args.kma_index
    command += " -o "+os.path.join(args.output_directory, args.output_file_base)
    if args.se:
        command += " -i "+" ".join(args.se)
    elif args.pe:
        command += " -ipe "
        for pair in args.pe:
            command += " ".join(pair.split(":"))
    if args.kma_options:
        command += " "+" ".join(args.kma_options)

    print command
    subprocess.call(command.split(" "))

