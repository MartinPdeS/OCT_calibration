
'''_____Standard imports_____'''
import numpy as np
import json
import matplotlib.pyplot as plt
import pandas as pd
import sys


'''_____Project imports_____'''
from toolbox.parsing import Bscan_parse_arguments
from toolbox.loadings import load_Bscan_spectra, load_calibration
from toolbox.plottings import Bscan_vizualiser
from toolbox.fits import get_fit_curve
from toolbox.filters import butter_highpass_filter
from toolbox.spectra_processing import linearize_spectra, compensate_dispersion
from toolbox.maths import spectra2aline
from toolbox.Bscan_processing import process_Bscan, clean_Bscan




arguments = Bscan_parse_arguments()

Bscan_LP01_dir = "/Volumes/Untitled/Calibrations/Bscan/cible_2.raw"
Bscan_LP11_dir = "/Volumes/Untitled/Calibrations/Bscan/cible_3.raw"

Bscan_spectra_LP01 = load_Bscan_spectra(Bscan_LP01_dir)
Bscan_spectra_LP11 = load_Bscan_spectra(Bscan_LP11_dir)


Calibration_LP01_dir = "/Volumes/Untitled/Calibrations/lantern/LP11/calibration_parameters.json"
Calibration_LP11_dir = "/Volumes/Untitled/Calibrations/lantern/LP11/calibration_parameters.json"

calibration_LP01 = load_calibration(dir = Calibration_LP01_dir)
calibration_LP11 = load_calibration(dir = Calibration_LP11_dir)


Bscan_LP01 = process_Bscan(Bscan_spectra_LP01, calibration_LP01, arguments)
Bscan_LP11 = process_Bscan(Bscan_spectra_LP11, calibration_LP01, arguments)

I_01 = clean_Bscan(Bscan_LP01)
I_11 = clean_Bscan(Bscan_LP11)


I_norm = np.mean(I_01 + I_11)

I_11_norm = I_11 / I_norm
I_01_norm = I_01 / I_norm

Brad_ratio = I_01 / I_11_norm


#print(np.min(Brad_ratio), np.max(Brad_ratio))
#plt.imshow(Brad_ratio)
#plt.show()


#print('############', np.shape(Brad_ratio), np.shape(I_01))

A = Bscan_vizualiser(fig1=[0,1,2], Bscan_LP01=[I_01_norm], Bscan_LP11=[I_11_norm], arguments=arguments)

A.Bscan_lanterne_plots()






#-
