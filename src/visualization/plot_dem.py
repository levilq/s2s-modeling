# src/visualization/plot_dem.py

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# Set backend to ensure proper rendering in PyCharm
matplotlib.use('TkAgg')  # 'TkAgg' works well for interactive 3D plots

def visualize_dem(dem_data, meta):
    """
    Visualize the DEM as a 3D surface plot.
    :param dem_data: DEM array
    :param meta: DEM metadata (for spatial extent)
    """
    # Create coordinate grid based on DEM dimensions
    nrows, ncols = dem_data.shape
    x = np.linspace(meta['transform'][2], 
                    meta['transform'][2] + meta['width'] * meta['transform'][0], 
                    ncols)
    y = np.linspace(meta['transform'][5], 
                    meta['transform'][5] + meta['height'] * meta['transform'][4], 
                    nrows)
    X, Y = np.meshgrid(x, y)

    # Create 3D plot
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(111, projection='3d')

    # Plot surface
    ax.plot_surface(X, Y, dem_data, cmap='terrain', edgecolor='none')

    # Labels and title
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.set_zlabel("Elevation (m)")
    ax.set_title("3D Digital Elevation Model (DEM)")

    # Show the plot interactively
    plt.show(block=True)  # Ensures the plot remains open
