import re
from Bio import SeqIO
from Bio.Seq import Seq
import sys
import subprocess
import pandas as pd

file = sys.argv[1]
min_size = int(sys.argv[2])
max_size = int(sys.argv[3])

c = 1
with open(file) as handle:
    for record in SeqIO.parse(handle, "fasta"):

        seq = record.seq
        if min_size < len(seq) < max_size:

            print('Fragmento = ', c)

            SeqIO.write(record, "query_fragment.fasta", "fasta")

            blast_cmd = ['blastn',
             '-query', 'query_fragment.fasta',
             '-db', 'rep_genomes/sars_db',
             '-word_size', '7',
             '-evalue',  '50',
             '-outfmt', '7',
             '-out', 'fragments_hits/' + 'frag_' + str(c)]

            result = subprocess.run(blast_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


            seq_cmd = ['sed',
            '-i', '1 i\#' + 'seq=' + str(seq),
            'fragments_hits/' + 'frag_' + str(c)
            ]

            sequence = subprocess.run(seq_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            c += 1
