import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
src = os.getcwd()
dirName = os.path.basename(src)
path = os.path.join(src, 'results', 'data')
timeStamps = [float(name) for name in os.listdir(src) if name.startswith('0.') | name.startswith('1.') | name.startswith('2.')]
timeStamps.sort()
num_of_timesteps = len(timeStamps)
first_csv_path = os.path.join(path, 'data_1.csv')
df_check = pd.read_csv(first_csv_path, nrows=1)
columns_in_first_file = df_check.columns.tolist()
if 'k' in columns_in_first_file:
    # For k-omega SST-SAS model use below two lines
    files = [['Points:0','Points:1','Points:2','U:0','U:1','U:2'],['Points:0','Points:1','Points:2','p','pGrad:0','pGrad:1','pGrad:2'],['Points:0','Points:1','Points:2','alpha.water','k','nut','omega'],['Points:0','Points:1','Points:2','turbulenceProperties:R:0', 'turbulenceProperties:R:1','turbulenceProperties:R:2','turbulenceProperties:R:3','turbulenceProperties:R:4','turbulenceProperties:R:5'],['Points:0','Points:1','Points:2','uGrad:0','uGrad:1','uGrad:2','uGrad:3','uGrad:4','uGrad:5','uGrad:6','uGrad:7','uGrad:8']]
    fileNames =['velocity','pressure','alpha_k_nut_omega','turbulentStress','velocityGradients']
else:
    # For SA model use below two lines
    files = [['Points:0','Points:1','Points:2','U:0','U:1','U:2'],['Points:0','Points:1','Points:2','p','pGrad:0','pGrad:1','pGrad:2'],['Points:0','Points:1','Points:2','alpha.water','nut'],['Points:0','Points:1','Points:2','uGrad:0','uGrad:1','uGrad:2','uGrad:3','uGrad:4','uGrad:5','uGrad:6','uGrad:7','uGrad:8']]
    fileNames = ['velocity','pressure','alpha_nut','velocityGradients']

parquet_writers = {}
parquet_schemas = {}

for j,base_name in enumerate(fileNames):
    usecols = files[j]
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
    print('|----------------------------------------------------------------|')
