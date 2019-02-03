from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
from purpleair import purpleair
from purpleair import sensor


# Get the purpleair data
p = purpleair.PurpleAir()
df = p.to_dataframe()
# Store the lat and lon coords to plot
lat = df['lat'].values
lon = df['lon'].values

margin = 1  # buffer to add to the range
lat_min = min(lat) - margin
lat_max = max(lat) + margin
lon_min = min(lon) - margin
lon_max = max(lon) + margin

m = Basemap(llcrnrlon=lon_min,
            llcrnrlat=lat_min,
            urcrnrlon=lon_max,
            urcrnrlat=lat_max,
            lat_0=(lat_max - lat_min)/2,
            lon_0=(lon_max-lon_min)/2,
            projection='merc',
            resolution = 'h',
            area_thresh=10000.,
            )

m.drawcoastlines()
m.drawcountries()
m.drawstates()

# Colors
water = '#46bcec'
land = '#ffffff'
m.drawmapboundary(fill_color=water)
m.fillcontinents(color = land, lake_color=water)

# convert lat and lon to map projection coordinates
lons, lats = m(lon, lat)
# plot points as red dots
m.scatter(lons, lats, marker='o', color='r', zorder=5, alpha=0.25, s=2)
plt.savefig('sensor_map.png')
