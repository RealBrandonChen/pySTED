import numpy as np
from pysted import base, utils, raster, bleach_funcs
from matplotlib import pyplot as plt
import time
import tifffile


molecules_disposition = np.zeros((128, 128))
molecules_disposition[30:40, 30:40] = 10
# molecules_disposition = np.zeros((3, 3))
# molecules_disposition[1, 1] = 10

print("test")
print("Setting up the microscope ...")
# Microscope stuff
egfp = {"lambda_": 535e-9,
        "qy": 0.6,
        "sigma_abs": {488: 1.15e-20,
                      575: 6e-21},
        "sigma_ste": {560: 1.2e-20,
                      575: 6.0e-21,
                      580: 5.0e-21},
        "sigma_tri": 1e-21,
        "tau": 3e-09,
        "tau_vib": 1.0e-12,
        "tau_tri": 5e-6,
        "phy_react": {488: 1e-7,   # 1e-4
                      575: 1e-11},   # 1e-8
        "k_isc": 0.26e6}
pixelsize = 10e-9
bleach = True
p_ex = 1e-6
p_ex_array = np.ones(molecules_disposition.shape) * p_ex
p_sted = 30e-3
p_sted_array = np.ones(molecules_disposition.shape) * p_sted
pdt = 10e-6
pdt_array = np.ones(molecules_disposition.shape) * pdt
roi = 'max'
bleach_func = bleach_funcs.default_update_survival_probabilities

# Generating objects necessary for acquisition simulation
laser_ex = base.GaussianBeam(488e-9)
laser_sted = base.DonutBeam(575e-9, zero_residual=0)
detector = base.Detector(noise=True, background=0)
objective = base.Objective()
fluo = base.Fluorescence(**egfp)
datamap = base.Datamap(molecules_disposition, pixelsize)
microscope = base.Microscope(laser_ex, laser_sted, detector, objective, fluo, load_cache=True)
i_ex, _, _ = microscope.cache(datamap.pixelsize, save_cache=True)
datamap.set_roi(i_ex, roi)

print(f'starting acq with phy_react = {egfp["phy_react"]}')
time_start = time.time()
acquisition, bleached, intensity = microscope.get_signal_and_bleach(datamap, datamap.pixelsize, pdt, p_ex, p_sted,
                                                                    bleach=True, update=False,
                                                                    bleach_func=bleach_func, seed=42)
print(f"ran in {time.time() - time_start} s")
# print(utils.mse_calculator(datamap.whole_datamap[datamap.roi], bleached["base"][datamap.roi]))
# survival = utils.molecules_survival(datamap.whole_datamap[datamap.roi], bleached["base"][datamap.roi])
# print(survival)

tifffile.imwrite("./masked-acquisition.tif", acquisition.astype(np.uint16))

# fig, axes = plt.subplots(1, 3)
#
# axes[0].imshow(datamap.whole_datamap[datamap.roi])
# axes[0].set_title(f"Datamap roi")
#
# axes[1].imshow(bleached["base"][datamap.roi])
# axes[1].set_title(f"Bleached datamap")
#
# axes[2].imshow(acquisition)
# axes[2].set_title(f"Acquired signal (photons)")
#
# plt.show()
