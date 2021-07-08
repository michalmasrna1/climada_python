from matplotlib import colors
import matplotlib.pyplot as plt
from os import path

from climada.entity import LitPop, ImpactFuncSet
from climada.hazard import StormEurope
from climada.entity.impact_funcs.storm_europe import IFStormEurope
from climada.engine.impact import Impact


PLOTTING = True
filename_exp = "data/litpop_slovakia.hdf5"
filename_haz = "data/raw_wisc_slovakia.hdf5"
filename_imp = "data/imp_slovakia.hdf5"
WISC_files = '/home/michal/climada/data/C3S_WISC_FOOTPRINT_NETCDF_0100/fp_era[!er5]*_0.nc'

exposure = LitPop()
if path.exists(filename_exp):
    exposure.read_hdf5(filename_exp)
else:
    exposure.set_country('SVK', reference_year=2020)
    exposure.write_hdf5(filename_exp)
exposure.check()

if PLOTTING:
    # exposure.set_geometry_points() # no idea what this does
    # plot exposure with linear colormap:
    # exposure.plot_hexbin(pop_name=False) # not much info can be seen here
    # plot exposure with log-normal colormap:
    norm = colors.LogNorm(vmin=500, vmax=4.0e9)
    exposure.plot_hexbin(norm=norm, pop_name=False)


hazard = StormEurope()
if path.exists(filename_haz):
    hazard.read_hdf5(filename_haz)
else:
    hazard.read_footprints(WISC_files)
    # hazard = hazard.generate_prob_storms(reg_id=421) # does not work for slovakia yet
    hazard.write_hdf5(filename_haz)
# hazard.select(reg_id=421) # results in ValueError
hazard.check()

if PLOTTING:
    # some coordinates recalculation seem to be necessary
    hazard.plot_intensity(event=0)

impact_function = IFStormEurope()
impact_function.set_welker()

impf_set = ImpactFuncSet()
impf_set.append(impact_function)
impf_set.check()

[haz_type] = impf_set.get_hazard_types()
[haz_id] = impf_set.get_ids()[haz_type]

exposure.gdf.rename(columns={"if_": "if_" + haz_type}, inplace=True)
exposure.gdf['if_' + haz_type] = haz_id
exposure.check()

imp = Impact()
if path.exists(filename_imp):
    imp.read_excel(filename_imp)
else:
    imp.calc(exposure, impf_set, hazard, save_mat=False)
    imp.write_excel(filename_imp)

print(f"Aggregated average annual impact: {round(imp.aai_agg,0)} $")

if PLOTTING:
    norm = colors.LogNorm(vmin=1, vmax=2)  # TODO: study and implement more sensible colors
    imp.plot_hexbin_eai_exposure(buffer=1, norm=norm, pop_name=False)

if PLOTTING:
    plt.show()
