import pandas as pd
import sys
procs = int(sys.argv[1])
path = '/results/data/All/'
fileNames = ['velocity','pressure','alpha_nut','velocityGradients']
#fileNames = ['velocity','pressure','alpha_k_nut_omega','turbulentStress','velocityGradients']
for j in range(len(fileNames)):
    data = pd.read_parquet('./proc_1'+path+fileNames[j]+'.parquet')
    for i in range(2,procs+1):
	    filePath = './proc_'+str(i)+path+fileNames[j]+'.parquet'
	    data = pd.concat([data,pd.read_parquet(filePath)])
    data.to_parquet('.'+path+fileNames[j]+'.parquet')
    dataMean = data.groupby(level=1).mean()
    dataMean.to_parquet('.'+path+fileNames[j]+'Mean.parquet')
