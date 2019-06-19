
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

dir_LP01 = ".temporary/Cscan_LP01.csv"
dir_LP11 = ".temporary/Cscan_LP11.csv"


DataFrame_LP01 = pd.read_pickle(dir_LP01)
DataFrame_LP11 = pd.read_pickle(dir_LP11)

data_LP01 = DataFrame_LP01.to_numpy().reshape(20,1049,508)
data_LP11 = DataFrame_LP11.to_numpy().reshape(20,1049,508)


I_01 = data_LP01
I_11 = data_LP11

I_norm = I_01 + I_11

bra  = I_11 / I_norm

Brad_ratio = I_01 / I_11



A = Bscan_vizualiser(fig1=[0,1,2], Bscan_LP01=Brad_ratio, Bscan_LP11=data_LP11, arguments=arguments)

A.Bscan_lanterne_plots()






#-
