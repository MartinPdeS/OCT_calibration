
'''_____Standard imports_____'''
import numpy as np
import json
import os
import matplotlib.pyplot as plt
import sys
from pandas import DataFrame


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)

'''_____Project imports_____'''
from src.toolbox.parsing import Cscan_parse_arguments
from src.toolbox.loadings import load_calibration
from src.toolbox.spectra_processing import process_Cscan
import src.toolbox.directories as directories
from src.toolbox.spectra_processing import *


arguments = Cscan_parse_arguments()

dimension = (1,1049,1024)

calibration = load_calibration(dir = arguments.calibration_file)

Bscan_list = os.listdir(arguments.input_directory)

Bscan_list = [os.path.join(arguments.input_directory, s) for s in Bscan_list]

Cscan = []

for n_i, Bscan in enumerate(Bscan_list):

    sys.stdout.write('Bscan processing ... [{0}/{1}] \n'.format(n_i, len(Bscan_list) ) )

    raw_Bscan = np.load(Bscan)

    raw_Bscan = np.reshape(raw_Bscan, dimension)

    Bscan = process_Bscan(raw_Bscan[0], calibration, shift=0, arguments=arguments)

    #Bscan = denoise_Bscan(Bscan)

    Cscan.append(Bscan)

sys.stdout.write(' saving into {0} file \n shape of file : {1}'.format(arguments.output_file, str( np.shape( Cscan ) ) ) )

np.save(arguments.output_file, Cscan)









#-
