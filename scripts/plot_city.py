from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from purpleair import purpleair
from purpleair import sensor
import random


# Get the purpleair data
p = purpleair.PurpleAir()
df = p.to_dataframe()
var_to_viz = 'temp_c'  # The dict item that we want to visualize
# Store the lat and lon coords to plot
lat = df['lat'].values
lon = df['lon'].values
colors = df[var_to_viz].values  # Variable on which to generate the color gradient

# Coorinates for Los Angeles, CA
m = Basemap(llcrnrlon=-118.5,
            llcrnrlat=33.15,
            urcrnrlon=-117.15,
            urcrnrlat=34.5,
            lat_0=34.,
            lon_0=-118.,
            projection='lcc',
            resolution = 'i',
            epsg=3498  # Lookup via https://epsg.io
            )

m.arcgisimage(service='ESRI_Imagery_World_2D', xpixels=2000)
m.drawcoastlines()

# convert lat and lon to map projection coordinates
lons, lats = m(lon, lat)
# plot points as red dots
m.scatter(lons, lats, marker='o', c=colors, cmap='plasma', zorder=5, s=3)
plt.colorbar().set_label(f'{var_to_viz}', rotation=270)
plt.savefig('maps/city_map.png', dpi=300)
