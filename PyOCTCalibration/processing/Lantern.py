
'''_____Standard imports_____'''
import numpy as np
import pandas as pd
import os
import sys

'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)


'''_____Project imports_____'''
from toolbox.parsing import Bscan_parse_arguments
from toolbox.loadings import load_Bscan_spectra, load_calibration
from toolbox.plottings import Lantern_vizualiser
from toolbox.spectra_processing import process_Bscan, denoise_Bscan
import toolbox.directories as directories



arguments = Bscan_parse_arguments()

dir_LP01 = directories.raw + "LP01_shift.raw"
dir_LP11 = directories.raw + "LP11_shift.raw"

Bscan_spectra_LP01 = load_Bscan_spectra(dir_LP01)
Bscan_spectra_LP11 = load_Bscan_spectra(dir_LP11)

calibration_LP01 = load_calibration(dir =   directories.calib + "calibration_parameters_LP01.json")
calibration_LP11 = load_calibration(dir =   directories.calib + "calibration_parameters_LP11.json")


Bscan_LP01 = process_Bscan(Bscan_spectra_LP01, calibration_LP01, shift=0, arguments=arguments)
Bscan_LP11 = process_Bscan(Bscan_spectra_LP11, calibration_LP01, shift=0.03536, arguments=arguments)



Bscan_LP01 = denoise_Bscan(Bscan_LP01)
Bscan_LP11 = denoise_Bscan(Bscan_LP11)

I_01 = Bscan_LP01
I_11 = Bscan_LP11

I_norm = I_01 + I_11

bra  = I_11 / I_norm

Brad_ratio = I_01 / I_11

A = Lantern_vizualiser(fig1=[0,1,2], Bscan_LP01=[Brad_ratio], Bscan_LP11=[Bscan_LP11], arguments=arguments)

A.Bscan_lanterne_plots()






#-
