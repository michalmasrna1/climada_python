# %%
# from climada.hazard import Centroids
# import matplotlib.pyplot as plt
#
#
# min_lat, max_lat, min_lon, max_lon = 47.9, 49.6, 16.9, 22.4
# cent = Centroids()
# cent.set_raster_from_pnt_bounds((min_lon, min_lat, max_lon, max_lat), res=0.4)
# cent.check()
# cent.plot(figsize=(3, 4))
# plt.show()

# %%

import matplotlib.pyplot as plt

from climada.hazard import StormEurope
from climada.util.constants import WS_DEMO_NC

storm_instance = StormEurope()
# storm_instance.read_footprints(WS_DEMO_NC)
plt.rcParams['figure.figsize'] = [10, 10]

WISC_files = '/home/michal/climada/data/C3S_WISC_FOOTPRINT_NETCDF_0100/fp_era[!er5]*_0.nc'
storm_instance.read_footprints(WISC_files)
storm_instance.write_hdf5('/home/michal/climada/helfni/data/wisc.hdf5')

# %%

# storm_prob = storm_instance.generate_prob_storms(reg_id=None, ssi_args={'method': 'wind_gust',
#                                                                        'threshold': 25,
#                                                                        })

slovakia = storm_instance.select(reg_id=421)
slovakia.plot_intensity(event=0)

plt.show()
