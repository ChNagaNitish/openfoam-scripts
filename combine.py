import os
import sys
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import glob

procs = int(sys.argv[1])
relative_path = 'results/data'
output_dir = f'.{os.path.sep}{relative_path}'
os.makedirs(output_dir, exist_ok=True)
#timeStamps = [float(name) for name in os.listdir(f'.{os.path.sep}') if name.startswith('0.') | name.startswith('1.') | name.startswith('2.')]
#timeStamps.sort()
#num_of_timesteps = len(timeStamps)
#print(num_of_timesteps)

fileNames = []
proc1_data_path = os.path.join('proc_1', relative_path)
parquet_files_in_proc1 = glob.glob(os.path.join(proc1_data_path, '*.parquet'))
fileNames = [os.path.basename(f).replace('.parquet', '') for f in parquet_files_in_proc1]
fileNames = [name for name in fileNames if not name.endswith('Mean')]

for base_name in fileNames:
    final_writer = None
    final_schema = None
    for i in range(1,procs+1):
        proc_dir_name = f'proc_{i}'
        current_proc_data_path = os.path.join(proc_dir_name, relative_path)
        individual_parquet_path = os.path.join(current_proc_data_path, f'{base_name}.parquet')
        table = pq.ParquetFile(individual_parquet_path)
        if i==1:
            final_parquet_path = os.path.join(output_dir, f'{base_name}.parquet')
            final_schema = table.schema_arrow
            final_writer = pq.ParquetWriter(final_parquet_path, final_schema)
        for batch in table.iter_batches():
            final_writer.write_batch(batch)
    final_writer.close()
    print('|----------------------------------------------------------------|')
    print('|  '+base_name+' combined in Parquet format  |')
    print('|----------------------------------------------------------------|')