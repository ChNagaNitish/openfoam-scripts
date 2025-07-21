import pandas as pd

import numpy as np
import argparse
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import matplotlib.animation as animation
import pyarrow as pa
import pyarrow.parquet as pq

def plotVelAtHLines(path,fps):
    inputVelData = np.load(path)
    mm_per_px = 0.02175955
    fps_capture = 130000
    factor = mm_per_px*1e-3*fps_capture
    fac = 8
    y = 44
    u = inputVelData[:,y,:,0]*factor
    x_mm = np.arange(u.shape[1])*mm_per_px*8
    nFrames = u.shape[0]
    fig, ax = plt.subplots()
    line, = ax.plot(x_mm,u[0,:])
    ax.axhline(0,color='black',linewidth=0.5)
    ax.set_xlabel('x [mm]')
    ax.set_ylabel('u [m/s]')
    ax.set_ylim([-15,25])
    title = ax.set_title(f'Frame 1/{nFrames}')
    def updateFrame(frame):
        line.set_ydata(u[frame,:])
        title.set_text(f'Frame {frame+1}/{nFrames}')
        return line, title
    ani = animation.FuncAnimation(fig=fig, func=updateFrame, frames=nFrames-1, blit=True, interval=1000/fps,repeat=False)
    writer = animation.FFMpegWriter(fps=fps)
    ani.save(path[:-4]+'_hline.avi', writer=writer, dpi=150)

def rotate(x, y, angle, cx, cy):
    angle_rad = np.radians(angle)
    x_rotated = cx + (x - cx) * np.cos(angle_rad) - (y - cy) * np.sin(angle_rad)
    y_rotated = cy + (x - cx) * np.sin(angle_rad) + (y - cy) * np.cos(angle_rad)
    return x_rotated, y_rotated

def is_inside_concave(x, y):
    return 0.4877811560945907*x - y > 0.0055113921338018936 and y < 0.011

def alphaVar(path):
    table = pq.read_table(path)
    df = table.to_pandas()
    timeStamps = np.sort(df['Time'].unique())
    df = df.set_index(['Time','index'])
    table = pq.read_table('data/points.parquet')
    dfp = table.to_pandas()
    x = dfp['Points:0'].values
    y = dfp['Points:1'].values
    # Apply rotation to the points
    angle_degrees = 8 # Replace with your desired rotation angle
    cx, cy = 0.03385, 0.011  # Replace with your desired center of rotation
    x_rotated, y_rotated = rotate(x, y, angle_degrees, cx, cy)
    triang = tri.Triangulation(x_rotated, y_rotated)
    x_centroids = x_rotated[triang.triangles].mean(axis=1)
    y_centroids = y_rotated[triang.triangles].mean(axis=1)
    mask = np.array([is_inside_concave(x, y) for x, y in zip(x_centroids, y_centroids)])
    triang.set_mask(mask)
    #
    var = df['alpha.water'].groupby(['index']).var()
    maxVar = var.idxmax()
    print(maxVar)
    plt.tricontourf(triang,var)
    plt.plot(x_rotated[maxVar],y_rotated[maxVar],'ro')
    plt.show()



def contourVideo(path,geom):
    df = pq.read_table(path,columns=['Time','index','alpha.water'])
    df = df.to_pandas()
    timeStamps = np.sort(df['Time'].unique())
    df = df.set_index(['Time','index'])
    # Load points
    dfp = pq.read_table('data/points.parquet')
    dfp = dfp.to_pandas()
    x = dfp['Points:0'].values
    y = dfp['Points:1'].values
    # Apply rotation to the points
    angle_degrees = 8 # Replace with your desired rotation angle
    cx, cy = 0.03385, 0.011  # Replace with your desired center of rotation
    x_rotated, y_rotated = rotate(x, y, angle_degrees, cx, cy)
    triang = tri.Triangulation(x_rotated, y_rotated)
    x_centroids = x_rotated[triang.triangles].mean(axis=1)
    y_centroids = y_rotated[triang.triangles].mean(axis=1)
    mask = np.array([is_inside_concave(x, y) for x, y in zip(x_centroids, y_centroids)])
    triang.set_mask(mask)
    # Plot
    fps = 20
    fig, ax = plt.subplots()
    cont = ax.tricontourf(triang, df.loc[timeStamps[0]]['alpha.water'].values, cmap='viridis')
    plt.colorbar(cont,fraction=0.046/5,pad=0.01)
    def updateFrame(step):
        time = timeStamps[step]
        z = df.loc[time]['alpha.water'].values
        ax.clear()
        ax.set_xlim([0.03385,0.1])
        ax.set_ylim([0.011,0.02])
        ax.set_aspect('equal')
        cont = ax.tricontourf(triang, z, cmap='viridis')
        title = ax.set_title(f'Time {time}')
        return cont, title
        '''if geom=='3d':
            unique_z = np.sort(df['Points:2'].unique())
            nz = len(unique_z)
            midPlane = nz//2
            print(midPlane)
            df = df[np.abs(df['Points:2']==unique_z[midPlane])]'''
    ani = animation.FuncAnimation(fig=fig, func=updateFrame, frames=len(timeStamps), blit=True, interval=1000/fps,repeat=False)
    writer = animation.FFMpegWriter(fps=fps)
    ani.save('alphaWater.avi', writer=writer, dpi=150)
        #plt.show()


# Read file
path='data/alpha_k_nut_omega.parquet'
contourVideo(path,'2d')
#alphaVar(path)

'''df = pd.read_parquet(path)
x = df['Points:0'].values
y = df['Points:1'].values
z = df['U:0'].values

# 1. Define the rotation function
def rotate(x, y, angle, cx, cy):
    angle_rad = np.radians(angle)
    x_rotated = cx + (x - cx) * np.cos(angle_rad) - (y - cy) * np.sin(angle_rad)
    y_rotated = cy + (x - cx) * np.sin(angle_rad) + (y - cy) * np.cos(angle_rad)
    return x_rotated, y_rotated

# 2. Apply rotation to the points
angle_degrees = 8  # Replace with your desired rotation angle
cx, cy = 0.03385, 0.011  # Replace with your desired center of rotation

x_rotated, y_rotated = rotate(x, y, angle_degrees, cx, cy)

def is_inside_concave(x, y):
    return 0.4877811560945907*x - y > 0.0055113921338018936 and y < 0.011
    #return 11*x - 33.85*y > 0 and 11*x + 78.27*y < 1.23332
# Create a triangulation
triang = tri.Triangulation(x_rotated, y_rotated)

# Calculate the centroids of each triangle
x_centroids = x_rotated[triang.triangles].mean(axis=1)
y_centroids = y_rotated[triang.triangles].mean(axis=1)

# Create a mask based on the concave shape condition
mask = np.array([is_inside_concave(x, y) for x, y in zip(x_centroids, y_centroids)])

# Apply the mask to the triangulation
triang.set_mask(mask)

# Create the filled contour plot
plt.figure()
ax = plt.gca()
cont = ax.tricontourf(triang, z, cmap='viridis')
plt.xlim([0.03385,0.08])
plt.ylim([0.011,0.02])
ax.set_aspect('equal')
plt.colorbar(cont,fraction=0.046/5,pad=0.01)
plt.show()
'''