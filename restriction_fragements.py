import re
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.Restriction import *
from collections import Counter
import collections
import sys


file = sys.argv[1]
org = sys.argv[2]

enzimas_1 = [TaqI, AvaII, AvrII, BanI]
enz_2 = BstNI

with open(file) as handle:
    for record in SeqIO.parse(handle, "fasta"):

        seq = record.seq
        genome_size = len(record.seq)
        seq_string = str(seq)


        for enz_1 in enzimas_1:

            sites_1 = enz_1.search(seq)
            sites_1.append(genome_size)

            site_5 = 0
            c = 0

            for site_3 in sites_1:
                fragment = seq_string[site_5:site_3]
                fragment = Seq(fragment)
                sites = enz_2.search(fragment)
                if len(sites) > 0:
                    c += 1
                    site = sites[0]
                    end = site+site_5
                    print('>', org, ';', str(enz_1), '+', str(enz_2),
                    '; start=', site_5, 'end=', end, 'size=', site+1)
                    print(seq_string[site_5:end])

                site_5 = site_3 - 1

            print('\n\n\n')
