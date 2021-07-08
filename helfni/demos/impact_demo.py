
# Exposure from the module Litpop
# Note that the file gpw_v4_population_count_rev11_2015_30_sec.tif must be downloaded (do not forget to unzip) if
# you want to execute this cell on your computer.

import numpy as np
from climada.entity import LitPop
import matplotlib.pyplot as plt
from os import path
from climada.hazard import TCTracks, TropCyclone, Centroids
from climada.entity import ImpactFuncSet, IFTropCyclone
from climada.engine import Impact

PLOTTING = True

# Cuba with resolution 10km and financial_mode = income group.
filename_exp = "data/litpop_cuba.hdf5"
if path.exists(filename_exp):
    exposure = LitPop()
    exposure.read_hdf5(filename_exp)
else:
    exposure = LitPop()
    exposure.set_country(countries=['CUB'], res_km=10, fin_mode='income_group', reference_year=2020)
    exposure.write_hdf5(filename_exp)
exposure.check()

if PLOTTING:
    exposure.plot_raster()
    plt.show()

# Load histrocial tropical cyclone tracks from ibtracs over the North Atlantic basin between 2010-2012
ibtracks_na = TCTracks()
ibtracks_na.read_ibtracs_netcdf(provider='usa', basin='NA', year_range=(2010, 2012), correct_pres=True)
print('num tracks hist:', ibtracks_na.size)
print('num tracks hist+syn:', ibtracks_na.size)
ibtracks_na.equal_timestep(0.5)  # Interpolation to make the track smooth c.f.

if PLOTTING:
    ax = ibtracks_na.plot()
    ax.get_legend()._loc = 2
    plt.show()

# Define the centroids from the exposures position
centrs = Centroids()
lat = exposure.gdf['latitude'].values
lon = exposure.gdf['longitude'].values
centrs.set_lat_lon(lat, lon)
centrs.check()

# Using the tracks, compute the windspeed at the location of the centroids
tc = TropCyclone()
tc.set_from_tracks(ibtracks_na, centrs)
tc.check()

# impact function TC
impf_tc = IFTropCyclone()
impf_tc.set_emanuel_usa()

# add the impact function to an Impact function set
impf_set = ImpactFuncSet()
impf_set.append(impf_tc)
impf_set.check()

# Get the hazard type and hazard id
[haz_type] = impf_set.get_hazard_types()
[haz_id] = impf_set.get_ids()[haz_type]
print(f"hazard type: {haz_type}, hazard id: {haz_id}")

# Exposures: rename column and assign id
exposure.gdf.rename(columns={"if_": "if_" + haz_type}, inplace=True)
exposure.gdf['if_' + haz_type] = haz_id
exposure.check()
print(exposure.gdf.head())

imp = Impact()
imp.calc(exposure, impf_set, tc, save_mat=False)

print(f"Aggregated average annual impact: {round(imp.aai_agg,0)} $")

if PLOTTING:
    imp.plot_hexbin_eai_exposure(buffer=1)
    plt.show()





