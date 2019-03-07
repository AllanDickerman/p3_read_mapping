# p3_read_mapping
Use kma to ap fastq reads to specified set of genes, for MLST etc.

Requirements:
	kma is on path
	kma index is available and specified as --kma_index option (file name excluding ".index.b" suffix)
	one single-end or paired-end fastq read library is specified as --se or --pe option
	output directory is specified as --output_directory option, will be created if needed

Output directory holds these files:
	prefix.res: results telling which allele for each locus is matched best
	prefix.aln: the alignment of the read assembly against best-hit alleles
	prefix.fsa: sequence of read assembly for each locus

