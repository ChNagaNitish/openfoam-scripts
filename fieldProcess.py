import os
import pandas as pd

src = os.getcwd()
dirName = os.path.basename(src)
path = src+'/results/data'
timeStamps = [float(name) for name in os.listdir(src) if name.startswith('0.') | name.startswith('1.') | name.startswith('2.')]
timeStamps.sort()
num_of_timesteps = len(timeStamps)

# For k-omega SST-SAS model use below two lines
#files = [['Points:0','Points:1','Points:2','U:0','U:1','U:2'],['Points:0','Points:1','Points:2','p','pGrad:0','pGrad:1','pGrad:2'],['Points:0','Points:1','Points:2','alpha.water','k','nut','omega'],['Points:0','Points:1','Points:2','alpha.water','turbulenceProperties:R:0', 'turbulenceProperties:R:1','turbulenceProperties:R:2','turbulenceProperties:R:3','turbulenceProperties:R:4','turbulenceProperties:R:5'],['Points:0','Points:1','Points:2','uGrad:0','uGrad:1','uGrad:2','uGrad:3','uGrad:4','uGrad:5','uGrad:6','uGrad:7','uGrad:8']]
#fileNames = ['velocity','pressure','alpha_k_nut_omega','turbulentStress','velocityGradients']

# For SA model use below two lines
files = [['Points:0','Points:1','Points:2','U:0','U:1','U:2'],['Points:0','Points:1','Points:2','p','pGrad:0','pGrad:1','pGrad:2'],['Points:0','Points:1','Points:2','alpha.water','nut'],['Points:0','Points:1','Points:2','uGrad:0','uGrad:1','uGrad:2','uGrad:3','uGrad:4','uGrad:5','uGrad:6','uGrad:7','uGrad:8']]
fileNames = ['velocity','pressure','alpha_nut','velocityGradients']

for j in range(len(fileNames)):
    frames = [pd.read_csv(path+'/data_'+str(i)+'.csv', usecols=files[j]) for i in range(num_of_timesteps)]
    allData = pd.concat(frames,keys=timeStamps)
    allData.to_parquet(path+'/'+fileNames[j]+'.parquet')
    print('|----------------------------------------------------------------|')
    print('|  '+fileNames[j]+' saved in Parquet format  |')
    print('|----------------------------------------------------------------|')
