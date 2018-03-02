import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import glob, os
from matplotlib.collections import PatchCollection
import matplotlib.patches as patches
from mpl_toolkits.mplot3d import Axes3D
import sys
def main():

    # for each file in folder
    # assign coordinate variables
    # take the average of the data to the right of the comma
    plot_type = sys.argv[1]
    fig = plt.figure()#subplots()

    # patches = []
    os.chdir("data")
    X, Y, Z, = np.array([]), np.array([]), np.array([])

    # Load data from CSV
    for file in glob.glob("*.txt"):
        filename = os.path.splitext(file)[0]
        signal = np.genfromtxt(file, delimiter=',',skip_header=0)
        X_dat = float(filename[0:2]) - 10# x coordinate
        Y_dat = float(filename[3:]) - 10# y coordinate
        Z_dat = abs(np.mean(signal[:,1])) # average signal strength
        X = np.append(X,X_dat)#[i])
        Y = np.append(Y,Y_dat)#[i])
        Z = np.append(Z,Z_dat)#[i])

    # Convert from pandas dataframes to numpy arrays
    # for i in range(len(X_dat)):


    # create x-y points to be used in heatmap
    xi = np.linspace(X.min(),X.max(),500)
    yi = np.linspace(Y.min(),Y.max(),500)
    xm, ym = np.meshgrid(xi,yi)
    # Z is a matrix of x-y values
    zi = griddata((X, Y), Z, (xi[None,:], yi[:,None]), method='cubic')

    # I control the range of my colorbar by removing data 
    # outside of my range of interest
    zmin = 0
    zmax = 2300
    zi[(zi<zmin) | (zi>zmax)] = None

    # Create the contour plot
    if plot_type == '2d':
        ax = fig.add_subplot(111, aspect = 'equal')
        CS = plt.contourf(xi, yi, zi, 15, cmap=plt.cm.rainbow,
                      vmax=zmax, vmin=zmin)
        ax.add_patch(patches.Circle((0,0),radius=4.125, fill=False, linewidth=10))
        ax.add_patch(patches.Circle((0,0),radius=2, fill=False, linewidth=3, color='b'))    
        plt.colorbar()  
        plt.gca().set_aspect('equal')
    if plot_type == '3d':
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(xm, ym, zi)#, cmap=plt.get_cmap('summer'))#, *args, **kwargs)

    # circle = Circle((0,0),radius=4.125, fill=False)#, linewidth=10)
    # Patch.set_fill(circle,False)
    # patches.append(circle)
    # Patch.set_facecolor(circle,'none')
    # p = PatchCollection(patches)

    # ax.add_collection(p)

    plt.show()

if __name__ == "__main__":
    main()