"""
Install requirements with `pip install -r requirements/common.txt`
"""

import datetime

import cartopy.crs as ccrs
import matplotlib.pyplot as plt

from purpleair.network import SensorList


VAR_TO_VIZ = 'temp_c'  # The dict item that we want to visualize

# Get PurpleAir data
p = SensorList()
df = p.to_dataframe('all')

# Store the lat and lon coords to plot
lat = df['lat'].values
lon = df['lon'].values

# Variable from which to generate the color gradient
colors = df[VAR_TO_VIZ].values

# Create the figure and the axes
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Display some map info
ax.set_global()  # Show whole globe
ax.stock_img()  # Use default background image
ax.coastlines()  # Draw coastlines with higher contrast

# Add scatter points for each coordinate pair
scatter = ax.scatter(lon, lat, marker='o', c=colors, cmap='plasma', zorder=5, s=3)

# Add scale
sm = plt.cm.ScalarMappable(cmap='plasma') 
cb = plt.colorbar(scatter).set_label(f'{VAR_TO_VIZ}', rotation=90)

# Draw title and save
ax.set_aspect('auto', adjustable=None)
plt.title(
    f'Global {VAR_TO_VIZ} at {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}')
plt.savefig('maps/sensor_map.png', dpi=300, bbox_inches='tight')
