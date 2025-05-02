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
foamfoam.CellArrays = ['U', 'alpha.water', 'k', 'nut', 'omega', 'p', 'p_rgh', 'rho', 'turbulenceProperties:R']

gradientOfUnstructuredDataSet1 = GradientOfUnstructuredDataSet(Input=foamfoam)
gradientOfUnstructuredDataSet1.ScalarArray = ['POINTS', 'p']
gradientOfUnstructuredDataSet1.ResultArrayName = 'pGrad'

gradientOfUnstructuredDataSet = GradientOfUnstructuredDataSet(Input=gradientOfUnstructuredDataSet1)
gradientOfUnstructuredDataSet.ScalarArray = ['POINTS', 'U']
gradientOfUnstructuredDataSet.ResultArrayName = 'uGrad'

# save data
SaveData(save_path+'/data.csv', proxy=gradientOfUnstructuredDataSet, ChooseArraysToWrite=1,PointDataArrays=['U', 'alpha.water', 'k', 'nut', 'omega', 'p', 'pGrad', 'turbulenceProperties:R','uGrad'], WriteTimeSteps=1)
print('|----------------------------------------|')
print('|  Extraction of All fields is complete  |')
print('|----------------------------------------|')