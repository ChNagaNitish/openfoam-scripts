import os
import glob
import dask.dataframe as dd

relative_path = 'results/data'
output_dir = f'.{os.path.sep}{relative_path}'

fileNames = []

parquet_files = glob.glob(os.path.join(relative_path, '*.parquet'))
fileNames = [os.path.basename(f).replace('.parquet', '') for f in parquet_files]
fileNames = [name for name in fileNames if not name.endswith('Mean')]


for base_name in fileNames:
    output_mean_path_parquet = os.path.join(output_dir, f'{base_name}Mean.parquet')
    file_path = os.path.join(relative_path,f'{base_name}.parquet')
    ddf = dd.read_parquet(file_path, engine='pyarrow')
    grouped_mean = ddf.groupby(['GridIndex']).mean()
    mean_pandas_df = grouped_mean.compute()
    mean_pandas_df.to_parquet(output_mean_path_parquet, index=False)
    print('|----------------------------------------------------------------|')
    print('|  '+base_name+'Mean in Parquet format  |')
    print('|----------------------------------------------------------------|')