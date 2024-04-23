# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/API/02_plotting.ipynb.

# %% auto 0
__all__ = ['plot_mutations', 'plot_mutations_percentage']

# %% ../nbs/API/02_plotting.ipynb 4
from fastcore.basics import *
import matplotlib.pyplot as plt
import seaborn as sns
import os
import csv
import numpy as np
from Bio import SeqIO
from typing import Union
from .utils import str_to_mut

# %% ../nbs/API/02_plotting.ipynb 9
def plot_mutations(gen_list: list, #list of genotypes. Each genotype is a tuple: (string representation of the genotype, number of molecules)
                   ref_seq: str, #reference sequence
                   sample_name: str = None,  #sample name
                   plot_range: Union[tuple,list] = None,  #limits the plot to the specified range
                   TR_range: Union[tuple,list] = None, #when specified creates a shaded box highlighting the position of the TR
                   ):
    
    if not plot_range:
        plot_range=[0,len(ref_seq)]

    L=plot_range[1]-plot_range[0]
    ref_seq=ref_seq[plot_range[0]:plot_range[1]]

    symbols=["A","T","G","C","del","ins","N"]
    mut_arrays=dict([(s,np.zeros(L)) for s in symbols])
    for gen, n in gen_list[1:]: #assumes the genotypes with the most molecules is the WT sequence and skips it
        g=gen.split(',')
        for mut in g:
            if mut:
                mut_from=mut[0]
                ix=int(mut[1:-1])
                k=mut[-1]
                if k=="-":
                    k="del"
                elif mut[0]=="-":
                    k="ins"
                mut_arrays[k][ix]+=n  


    for k in mut_arrays:
        mut_arrays[k]=mut_arrays[k][plot_range[0]:plot_range[1]]



    labels=np.array(range(L))

    fig, ax = plt.subplots(1,1,figsize=(20, 5))

    y=sum(mut_arrays.values())
    colors=["orange","red","green","blue","grey","black"]
    for i,s in enumerate(symbols[:-1]):
        sns.barplot(x=labels,y=y,color=colors[i],ax=ax,label=s)
        y-=mut_arrays[s]

    ax.set_xticks(range(len(ref_seq)))
    ax.set_xticklabels(list(ref_seq))
    ax.set_ylabel("number of molecules")
    ax.set_title(sample_name)
    if TR_range:
        ax.axvspan(max(plot_range[0],TR_range[0]),min(TR_range[1],plot_range[1]),alpha=0.1)
    ax.legend()
    #fig.savefig(base_path+"Plots/png/{}-{}_UMI_corrected_genotypes.png".format(sample.Sample_ID,sample.Sample_Name), dpi=300)
    #fig.savefig(base_path+"Plots/eps/{}-{}_UMI_corrected_genotypes.eps".format(sample.Sample_ID,sample.Sample_Name), format='eps')
    #plt.close()
    return ax
    

# %% ../nbs/API/02_plotting.ipynb 10
def plot_mutations_percentage(gen_list: list, #list of genotypes. Each genotype is a tuple: (string representation of the genotype, number of molecules)
                   ref_seq: str, #reference sequence
                   sample_name: str = None,  #sample name
                   plot_range: Union[tuple,list] = None,  #limits the plot to the specified range
                   TR_range: Union[tuple,list] = None, #when specified creates a shaded box highlighting the position of the TR
                   ):
    

    if not plot_range:
        plot_range=[0,len(ref_seq)]

    L=plot_range[1]-plot_range[0]
    ref_seq=ref_seq[plot_range[0]:plot_range[1]]

    count_geno=0
    count_muta=0
    for gen, n in gen_list:
        count_geno+=n


    symbols=["A","T","G","C","del","ins","N"]
    mut_arrays=dict([(s,np.zeros(L)) for s in symbols])
    for gen, n in gen_list[1:]: #assumes the genotypes with the most molecules is the WT sequence and skips it
        g=gen.split(',')
        count_muta+=n
        for mut in g:
            if mut:
                mut_from=mut[0]
                ix=int(mut[1:-1])
                k=mut[-1]
                if k=="-":
                    k="del"
                elif mut[0]=="-":
                    k="ins"
                mut_arrays[k][ix]+=n  


    for k in mut_arrays:
        mut_arrays[k]=(mut_arrays[k][plot_range[0]:plot_range[1]])/count_geno



    labels=np.array(range(L))

    fig, ax = plt.subplots(1,1,figsize=(20, 5))

    y=sum(mut_arrays.values())
    colors=["orange","red","green","blue","grey","black"]
    for i,s in enumerate(symbols[:-1]):
        sns.barplot(x=labels,y=y,color=colors[i],ax=ax,label=s)
        y-=mut_arrays[s]

    ax.set_xticks(range(len(ref_seq)))
    ax.set_xticklabels(list(ref_seq))
    ax.set_ylabel("Percentage of mutated bases")
    ax.set_title(sample_name)
    if TR_range:
        ax.axvspan(max(plot_range[0],TR_range[0]),min(TR_range[1],plot_range[1]),alpha=0.1)
    
    textstr = f'Total % of mutagenized molecules = {np.round(100*count_muta/count_geno,2)} %'
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

    # place a text box in upper left in axes coords
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,verticalalignment='top', bbox=props)

    ax.legend()
    #fig.savefig(base_path+"Plots/png/{}-{}_UMI_corrected_genotypes.png".format(sample.Sample_ID,sample.Sample_Name), dpi=300)
    #fig.savefig(base_path+"Plots/eps/{}-{}_UMI_corrected_genotypes.eps".format(sample.Sample_ID,sample.Sample_Name), format='eps')
    #plt.close()
    return ax
    
