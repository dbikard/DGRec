# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/API/02_utils.ipynb.

# %% auto 0
__all__ = ['align2mut', 'mut_rix', 'get_mutations', 'mut_to_str', 'str_to_mut', 'genstr_to_seq', 'get_prot_mut',
           'parse_genotypes', 'downsample_fastq_gz', 'get_basename_without_extension']

# %% ../nbs/API/02_utils.ipynb 2
import gzip
import itertools
import os
import csv
from . import pairwise2
from .pairwise2 import format_alignment
from Bio.Align import PairwiseAligner
from Bio.Seq import Seq

# %% ../nbs/API/02_utils.ipynb 3
def align2mut(align):
    """Converts a sequence alignment result from Bio.pairwise2.Align.globalms into a list of mutations.
    Positions are those of the alignment."""
    res=[]
    for i in range(align.end):
        if align.seqA[i]!=align.seqB[i]:
            mut=(align.seqA[i],i,align.seqB[i])
            res.append(mut)
    return res

# %% ../nbs/API/02_utils.ipynb 5
def mut_rix(mutations):
    """Reindexes the positions of the mutations to go from 
    their position in the sequence alignment to their position in the original sequence."""
    ph=0
    res_rix=[]
    for mut in mutations:
        rix=mut[1]+ph
        res_rix.append((mut[0],rix,mut[2]))
        if mut[0]=='-':
            ph-=1
            
    return res_rix

# %% ../nbs/API/02_utils.ipynb 7
def get_mutations(seqA,seqB):
    """Aligns two sequences and returns a genotype string.
    The string is a comma separated list of mutations.
    """
    align=pairwise2.align.globalms(seqA,seqB, 2, -1, -1, -.5, one_alignment_only=True)[0]
    mutations=align2mut(align) 
    mutations=mut_rix(mutations)
    return mutations

# %% ../nbs/API/02_utils.ipynb 13
def mut_to_str(mutations: list):
    """Converts list of mutations to a comma separated string"""
    mut_str_list=[''.join(map(str,mut)) for mut in mutations]
    mut_str=','.join(mut_str_list)
    return mut_str

# %% ../nbs/API/02_utils.ipynb 15
def str_to_mut(gen: str):
    """Converts genotype string to a list of mutations"""
    
    mutations=[]
    if gen=="":
        return mutations
    else:
        g=gen.split(',')
        for mut in g:
            mut_from=mut[0]
            ix=int(mut[1:-1])
            mut_to=mut[-1]
            mutations.append([mut_from,ix,mut_to])

        return mutations

# %% ../nbs/API/02_utils.ipynb 17
def genstr_to_seq(genstr,refseq):
    j=0
    seq=''
    for mut in str_to_mut(genstr):
        tb, i, qb = mut
        seq+=refseq[j:i]
        if tb=="-":
            seq+=qb
            j=i
        elif qb=="-":
            j=i+1
            pass
        else:
            seq+=qb
            j=i+1

    seq+=refseq[j:]

    return seq

# %% ../nbs/API/02_utils.ipynb 20
def get_prot_mut(genstr,refseq):
    mut_seq=genstr_to_seq(genstr,refseq)
    mut_prot=Seq(mut_seq).translate()
    ref_prot=Seq(refseq).translate()
    return mut_to_str(get_mutations(ref_prot,mut_prot))


# %% ../nbs/API/02_utils.ipynb 23
def parse_genotypes(genotypes_file):
    gen_list=[]
    with open(genotypes_file,"r") as handle: 
        reader = csv.reader(handle, delimiter='\t')
        for row in reader:
            gen_list.append((row[0],int(row[1])))
    return gen_list

# %% ../nbs/API/02_utils.ipynb 26
def downsample_fastq_gz(input_file, output_file, num_reads=10000):
    """Downsamples a compressed FASTQ file to the specified number of reads.

    Args:
        input_file (str): Path to the input FASTQ.gz file.
        output_file (str): Path to the output FASTQ.gz file.
        num_reads (int, optional): Number of reads to keep. Defaults to 10000.
    """

    with gzip.open(input_file, 'rb') as infile, gzip.open(output_file, 'wb') as outfile:
        lines = itertools.islice(infile, num_reads * 4)  # Read 4 lines (1 read) at a time
        for line in lines:
            outfile.write(line)

# %% ../nbs/API/02_utils.ipynb 28
def get_basename_without_extension(file_path):
    """
    Extracts the basename of a file without the extension.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The basename of the file without the extension.
    """

    basename = os.path.basename(file_path)
    if '.' in basename:
        # Split at the last dot to remove the extension
        return basename.rsplit('.', 1)[0]
    else:
        # No extension, return the whole filename
        return basename
