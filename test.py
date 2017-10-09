from streamflow import *

# Retrieve station list
station_list = get_station_list()
for string in station_list:
    print(string)

# Search for Station ID
station = search_station('Bailey')

# Get streamflow data
data = get_streamflow(station, '2015/10/01', '2017/10/01')

# Plot as time series
fig, ax = plot_ts(data)
plt.show()

