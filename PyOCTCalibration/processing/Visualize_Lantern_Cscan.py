
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
from toolbox.plottings import Lantern_Cscan_vizualiser
import toolbox.directories as directories

data = np.load('citrus_LP11.npy')
print(np.shape(data))


arguments = Bscan_parse_arguments()

data_LP01 = data
data_LP11 = data

A = Lantern_Cscan_vizualiser( fig1=[0,1,2],
                              Cscan_LP01=data_LP01[:,:,1:200],
                              Cscan_LP11=data_LP11[:,:,1:200],
                              arguments=arguments)

A.Bscan_lanterne_plots()






#-
