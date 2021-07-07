# %%
from climada.hazard import Centroids
import matplotlib.pyplot as plt

min_lat, max_lat, min_lon, max_lon = 47.9, 49.6, 16.9, 22.4
cent = Centroids()
cent.set_raster_from_pnt_bounds((min_lon, min_lat, max_lon, max_lat), res=0.1)
cent.check()
cent.plot()
plt.show()
