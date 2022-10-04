import pandas as pd
import os
import re

cols = ['query acc.ver', 'subject acc.ver', '% identity', 'alignment length', 'mismatches',
 'gap opens', 'q. start', 'q. end', 's. start', 's. end', 'evalue', 'bit score']

os.chdir('fragments_hits')

cols_map = {i: cols[i] for i in range(len(cols))}

for filename in os.listdir(os.getcwd()):

    with open(filename, 'r') as f:
        lineas = f.readlines()
        print('Query info', lineas[2])
        query_size = re.search('size= \d+', lineas[2]).group()
        query_size = int(re.search('\d+', query_size).group())

        seq = re.search('seq=\S+', lineas[0]).group()
        print(seq)


    df = pd.read_csv(filename, comment='#', sep='\t', header = None)
    df.rename(columns = cols_map, inplace = True)
    df = df[df['alignment length'] > query_size*0.5]
    print('Cantidad de matchs =', df.shape[0])
    df2 = df.sort_values('evalue', ascending=False).drop_duplicates(['subject acc.ver'])
    print('Genomas Matcheados =', df2.shape[0])
    print('Query size = ', query_size)
    print(df2['mismatches'].value_counts())

    csv_name = '../frags_dfs/'+ filename + '.csv'

    print('creando data frame ' + filename + '.csv', '\n\n')
    df2.to_csv(csv_name)
