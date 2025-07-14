import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import sys

src = os.getcwd()
dirName = os.path.basename(src)

threeDimensional = bool(sys.argv[1])

fileNames =['points','velocity','pressure','alpha_k_nut_omega','velocityGradients']
columns = [['Time'],['Points:0','Points:1','Points:2'], ['U:0','U:1','U:2'],['p','pGrad:0','pGrad:1','pGrad:2'],['alpha.water','k','nut','omega'],['uGrad:0','uGrad:1','uGrad:2','uGrad:3','uGrad:4','uGrad:5','uGrad:6','uGrad:7','uGrad:8']]
if not threeDimensional:
    columns[2] = columns[2][:-1]
    columns[3] = columns[3][:-1]
    columns[-1] = ['uGrad:0','uGrad:1','uGrad:3','uGrad:4']
usecols = sum(columns,[])
if not threeDimensional:
    columns[1] = columns[1][:-1]

path = os.path.join(src, 'results', 'data')
csvFiles = [file for file in os.listdir(path) if file.endswith('.csv')]
num_of_timesteps = len(csvFiles)

first_csv_path = os.path.join(path, csvFiles[-1])
df_check = pd.read_csv(first_csv_path, nrows=1)
columns_in_first_file = df_check.columns.tolist()
if 'k' not in columns_in_first_file:
    # For SA model
    fileNames[3] = 'alpha_nut'

parquet_writers = []
parquet_schemas = []

for i in range(num_of_timesteps):
    csv_file_path = os.path.join(path,csvFiles[i])
    df = pd.read_csv(csv_file_path, usecols=usecols)
    if not threeDimensional:
        df = df[df['Points:2']==0]
        df.drop(['Points:2'],axis=1,inplace=True)
    df = df.astype(float)
    df.reset_index(inplace=True)
    if i==0:
        pointTable = pa.Table.from_pandas(df[sum([['index'],columns[1]],[])], preserve_index=False)
        writer = pq.ParquetWriter(os.path.join(path, f'{fileNames[0]}.parquet'), pointTable.schema)
        writer.write_table(pointTable)
        writer.close()
    velTable = pa.Table.from_pandas(df[sum([columns[0],['index'],columns[2]],[])], preserve_index=False)
    preTable = pa.Table.from_pandas(df[sum([columns[0],['index'],columns[3]],[])], preserve_index=False)
    alpTable = pa.Table.from_pandas(df[sum([columns[0],['index'],columns[4]],[])], preserve_index=False)
    velGradTable = pa.Table.from_pandas(df[sum([columns[0],['index'],columns[5]],[])], preserve_index=False)
    if not parquet_writers:
        parquet_schemas.append(velTable.schema)
        parquet_schemas.append(preTable.schema)
        parquet_schemas.append(alpTable.schema)
        parquet_schemas.append(velGradTable.schema)
        parquet_writers.append(pq.ParquetWriter(os.path.join(path, f'{fileNames[1]}.parquet'), parquet_schemas[0]))
        parquet_writers.append(pq.ParquetWriter(os.path.join(path, f'{fileNames[2]}.parquet'), parquet_schemas[1]))
        parquet_writers.append(pq.ParquetWriter(os.path.join(path, f'{fileNames[3]}.parquet'), parquet_schemas[2]))
        parquet_writers.append(pq.ParquetWriter(os.path.join(path, f'{fileNames[4]}.parquet'), parquet_schemas[3]))
    parquet_writers[0].write_table(velTable)
    parquet_writers[1].write_table(preTable)
    parquet_writers[2].write_table(alpTable)
    parquet_writers[3].write_table(velGradTable)
parquet_writers[0].close()
parquet_writers[1].close()
parquet_writers[2].close()
parquet_writers[3].close()

print('|----------------------------------------------------------------|')
print('|  Saved in Parquet format  |')
print('|----------------------------------------------------------------|')

    
'''
for j,base_name in enumerate(fileNames):
    usecols = columns[j]
    writer = None
    schema = None
    for i in range(num_of_timesteps):
        current_timestamp = timeStamps[i]
        csv_file_path = os.path.join(path, f'data_{i}.csv')
        df = pd.read_csv(csv_file_path, usecols=usecols, index_col=False)
        df.reset_index(inplace=True)
        df.rename(columns={'index': 'GridIndex'}, inplace=True)
        df['Time'] = current_timestamp
        cols_to_select = ['Time', 'GridIndex'] + [col for col in usecols if col in df.columns]
        df = df[cols_to_select]
        df = df.astype(float)
        df['GridIndex'] = df['GridIndex'].astype(int)
        table = pa.Table.from_pandas(df, preserve_index=False)
        if writer==None:
            parquet_file_path = os.path.join(path, f'{base_name}.parquet')
            schema = table.schema
            writer = pq.ParquetWriter(parquet_file_path, schema)
        writer.write_table(table)
    writer.close()
    print('|----------------------------------------------------------------|')
    print('|  '+fileNames[j]+' saved in Parquet format  |')
    print('|----------------------------------------------------------------|')'''
