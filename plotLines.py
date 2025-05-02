import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from math import cos, sin
theta = np.deg2rad(8)
rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])

pts = [0.0015,0.003,0.005,0.01,0.015,0.02]
df1 = np.loadtxt('results/data/velxLines.dat')

fig, axs = plt.subplots(1,len(pts),sharey=True,figsize=(10,5))
for i in range(len(pts)):
    axs[i].set_xlabel('x = '+str(pts[i])+' mm')#, labelpad=17)
    axs[i].plot(df1[i,:],np.arange(0,10,0.01))
    #axs[i].xaxis.get_offset_text().set_position((1,0))
plt.savefig('results/velxLines.png')