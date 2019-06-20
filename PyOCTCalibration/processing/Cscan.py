
'''_____Standard imports_____'''
import numpy as np
import json
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



arguments = Cscan_parse_arguments()

raw_data = np.fromfile(arguments.input_file, dtype = np.uint16)

dim = (512,1049,1024)

start_block = 276
end_block = start_block + dim[0]*dim[1]*dim[2]

data = raw_data[start_block:end_block]

Cscan_spectra = data.reshape(dim, order='C')

Cscan_spectra = np.array(Cscan_spectra)

calibration = load_calibration(dir = arguments.calibration_file)

C_scan = process_Cscan(Cscan_spectra)

sys.stdout.write('%%%%%%%%%%%__ saving into csv file__%%%%%%%%%%% \n shape of file : {0}'.format(np.shape(Bscan.tolist() ) ) )

df = DataFrame(np.array(output_Cscan).reshape(length,1049*508))

df.to_pickle(arguments.output_file)








#-
