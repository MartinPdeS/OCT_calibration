
'''_____Standard imports_____'''
import os
import sys
import numpy as np
import json
import scipy.fftpack as fp
import matplotlib.pyplot as plt


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)


'''_____Project imports_____'''
from toolbox.parsing import Bscan_parse_arguments
from toolbox.loadings import load_Bscan_spectra, load_calibration
from toolbox.plottings import Bscan_plots
import toolbox.directories as directories
from toolbox.spectra_processing import process_Bscan, denoise_Bscan



arguments = Bscan_parse_arguments()

Bscan_spectra = load_Bscan_spectra(arguments.input_file)

if ".raw" in arguments.input_file:

    calibration = load_calibration(dir =  arguments.calibration_file)

    Bscan = process_Bscan(Bscan_spectra, calibration, shift=0, arguments=arguments)

    Bscan = denoise_Bscan(Bscan)

else:
    Bscan = Bscan_spectra

Bscan_plots(Bscan, arguments=arguments)





#-
