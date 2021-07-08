import pandas as pd
from climada.util.constants import ENT_TEMPLATE_XLS
from climada.entity import Exposures
from climada.entity.exposures.litpop import LitPop
import contextily as ctx
import matplotlib.pyplot as plt
from os import path

# file_name = ENT_TEMPLATE_XLS
# exp_templ_xlsx = pd.read_excel(file_name)
# exp_templ = Exposures(exp_templ_xlsx)
# exp_templ.set_geometry_points()
# exp_templ.check()

filename_exp = "data/litpop_slovakia.hdf5"
if path.exists(filename_exp):
    exposure = LitPop()
    exposure.read_hdf5(filename_exp)
else:
    exposure = LitPop()
    exposure.set_country('Slovakia', reference_year=2020)
    exposure.write_hdf5(filename_exp)

# select the background image from the available ctx.sources
ax = exposure.plot_basemap(buffer=30000, cmap='brg', zoom=11)  # using open street map

plt.show()

