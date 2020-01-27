
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
from toolbox.parsing import Cscan_parse_arguments
from toolbox.loadings import load_calibration
from toolbox.spectra_processing import process_Cscan
import toolbox.directories as directories
from toolbox.spectra_processing import *


arguments = Cscan_parse_arguments()

raw_data = np.fromfile(arguments.input_file, dtype = np.uint16)

print(np.shape(raw_data))

start_block = 276
end_block = 4096
tampon_block = 20
Spectrum_block = 1024
Bscan_block = 512 + 25
Cscan_block = 512

dim = (Cscan_block, Bscan_block, Spectrum_block)







data = raw_data[start_block:-end_block]

tampon = []
for i in range(1, Cscan_block):
    tampon_start = Spectrum_block * Bscan_block* i + tampon_block * (i-1)
    tampon_end = tampon_start + tampon_block
    tampon = tampon + list(range(tampon_start, tampon_end))

data = np.delete(data,tampon)


Cscan_spectra = data.reshape(dim, order='C')

print('############00')
print(np.shape(Cscan_spectra))


Cscan_spectra = np.array(Cscan_spectra)

calibration = load_calibration(dir = arguments.calibration_file)

C_scan = process_Cscan(Cscan_spectra, calibration, arguments)

sys.stdout.write('%%%%%%%%%%%__ saving into csv file__%%%%%%%%%%% \n shape of file : {0}'.format(np.shape(C_scan ) ) )


np.save('array', [C_scan])









#-
