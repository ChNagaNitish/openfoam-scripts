import pandas as pd
import numpy as np
from scipy.interpolate import LinearNDInterpolator

from math import cos, sin

df = pd.read_parquet('results/data/All/velocityMean.parquet')#,usecol=['Points:0','Points:1','U:0','U:1','alpha.water'])

#Rotate data set by 8deg to match experimental data and visualize diverging section as horizontal
theta = np.deg2rad(8)
rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])

throat = np.array([[33.85*1e-3, 11*1e-3]]).transpose()
df[['Points:0','Points:1']] = np.dot(rot,df[['Points:0','Points:1']].values.transpose()-throat).transpose()
df[['U:0','U:1']] = np.dot(rot,df[['U:0','U:1']].values.transpose()).transpose()
#df[['pGrad:0','pGrad:1']] = np.dot(rot,df[['pGrad:0','pGrad:1']].values.transpose()).transpose()
#df[['turbulenceProperties:R:0','turbulenceProperties:R:3','turbulenceProperties:R:3','turbulenceProperties:R:1']] = rot.transpose().dot(df[['turbulenceProperties:R:0','turbulenceProperties:R:3','turbulenceProperties:R:3','turbulenceProperties:R:1']].values.reshape(-1,2,2)).dot(rot).transpose(0,2,1).transpose().reshape(-1,4)


def distance_to_line_vectorized(points, start_point, end_point):
    """Calculates the distance between an array of points and a line."""
    v1 = np.array(end_point) - np.array(start_point)
    v2 = points - np.array(start_point) 
    distances = np.linalg.norm(np.cross(v1, v2)) / np.linalg.norm(v1)
    return distances



# Getting start and end points for the line
points = [0.0015,0.003,0.005,0.01,0.015,0.02]
variable = []
i=0
for j in points:
    i=i+1
    start_point = (j, 0)  # Replace with your actual start point coordinates
    end_point = (j, 10e-3)  # Replace with your actual end point coordinates

    # Calculate bounding box dimensions based on the line and your threshold
    threshold = i*2*1e-3
    min_x = min(start_point[0], end_point[0]) - threshold
    max_x = max(start_point[0], end_point[0]) + threshold
    min_y = min(start_point[1], end_point[1]) - threshold
    max_y = max(start_point[1], end_point[1]) + threshold
    #min_z = min(start_point[2], end_point[2]) - threshold
    #max_z = max(start_point[2], end_point[2]) + threshold
    # Filter points within the bounding box
    line_data = df[
        (df['Points:0'] >= min_x) & (df['Points:0'] <= max_x) &
        (df['Points:1'] >= min_y) & (df['Points:1'] <= max_y)
    ]
    num_points = 1000
    x_line = np.linspace(start_point[0], end_point[0], num_points)
    y_line = np.linspace(start_point[1], end_point[1], num_points)
    f = LinearNDInterpolator((line_data['Points:0'].values,line_data['Points:1'].values),line_data['U:0'].values) 
    along_line = f(x_line, y_line)
    variable.append(along_line)
np.savetxt('results/data/velxLines.dat',variable)