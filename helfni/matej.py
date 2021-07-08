import pandas as pd
from climada.util.constants import ENT_TEMPLATE_XLS
from climada.entity import Exposures
from climada.entity.exposures.litpop import LitPop
import contextily as ctx
import matplotlib.pyplot as plt
from os import path
from climada.hazard import Hazard
from climada.util import HAZ_TEMPLATE_XLS

# file_name = ENT_TEMPLATE_XLS
# exp_templ_xlsx = pd.read_excel(file_name)
# exp_templ = Exposures(exp_templ_xlsx)
# exp_templ.set_geometry_points()
# exp_templ.check()

filename_exp = "data/litpop_germany.hdf5"
if path.exists(filename_exp):
    exposure = LitPop()
    exposure.read_hdf5(filename_exp)
else:
    exposure = LitPop()
    exposure.set_country('Germany', reference_year=2020)
    exposure.write_hdf5(filename_exp)

exposure.plot_basemap(buffer=30000, cmap='brg')
plt.show()
# haz = Hazard('TC')
# haz.read_excel(HAZ_TEMPLATE_XLS)
# haz.check()
#
# haz.plot_intensity(event='event002')
# plt.show()


