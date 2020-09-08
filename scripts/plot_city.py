"""
Install requirements with `pip install -r requirements/common.txt`
"""

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from purpleair.network import SensorList

# Get the purpleair data
p = SensorList()
df = p.to_dataframe('all')
var_to_viz = 'temp_c'  # The dict item that we want to visualize
# Store the lat and lon coords to plot
lat = df['lat'].values
lon = df['lon'].values
# Variable on which to generate the color gradient
colors = df[var_to_viz].values

# Coorinates for Los Angeles, CA
m = Basemap(llcrnrlon=-118.5,
            llcrnrlat=33.15,
            urcrnrlon=-117.15,
            urcrnrlat=34.5,
            lat_0=34.,
            lon_0=-118.,
            projection='lcc',
            resolution='i',
            epsg=3498  # Lookup via https://epsg.io
            )

# This line does not work: https://github.com/matplotlib/basemap/issues/499
# m.arcgisimage(xpixels=2000, verbose=True)
m.shadedrelief(scale=1)
m.drawcoastlines()

# convert lat and lon to map projection coordinates
lons, lats = m(lon, lat)
# plot points as red dots
m.scatter(lons, lats, marker='o', c=colors, cmap='plasma', zorder=5, s=3)
plt.colorbar().set_label(f'{var_to_viz}\n\n\n\n', rotation=90)
plt.savefig('maps/city_map.png', dpi=300)
