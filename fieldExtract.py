#### import the simple module from the paraview and other required modules
from paraview.simple import *
import os
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()


src = os.getcwd()
dirName = os.path.basename(src)
dest = '/results/data'
read_file = src+'/'+dirName+'.foam'
save_path = src+dest
with open(dirName+'.foam', 'w') as fp:
    pass
try:
	os.makedirs(save_path, exist_ok = True)
	#print("Directory '%s' created successfully" % dest)
except OSError as error:
	print("Directory '%s' can not be created" % dest)
# create a new 'OpenFOAMReader'
foamfoam = OpenFOAMReader(FileName=read_file)
foamfoam.MeshRegions = ['internalMesh']
foamfoam.CellArrays = ['U', 'alpha.water', 'k', 'nut', 'omega', 'p']

gradient1 = Gradient(Input=foamfoam)
gradient1.ScalarArray = ['POINTS', 'p']
gradient1.ResultArrayName = 'pGrad'

gradient2 = Gradient(Input=gradient1)
gradient2.ScalarArray = ['POINTS', 'U']
gradient2.ResultArrayName = 'uGrad'

# save data
SaveData(save_path+'/data.csv', proxy=gradient2, ChooseArraysToWrite=1,PointDataArrays=['U', 'alpha.water', 'k', 'nut', 'omega', 'p', 'pGrad', 'uGrad'], WriteTimeSteps=1,WriteTimeStepsSeparately=1,Precision=6,AddTime=1)
print('|----------------------------------------|')
print('|  Extraction of All fields is complete  |')
print('|----------------------------------------|')
