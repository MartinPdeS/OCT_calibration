
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
from toolbox.parsing import Bscan_parse_arguments
from toolbox.loadings import load_Bscan_spectra, load_calibration
from toolbox.spectra_processing import process_Bscan, clean_Bscan, process_Cscan
import toolbox.directories as directories



arguments = Bscan_parse_arguments()

LP = 'LP11'

Cscan_file = "/Users/macbooklodi/Desktop/Cscan_" + LP + ".raw"

calibration_file = "/Volumes/Untitled/Calibrations/lanterne/" + LP + "/calibration_parameters.json"

temp_dir = directories.csv + LP + ".csv"


raw_data = np.fromfile(Cscan_file, dtype = np.uint16)


dim = (512,1049,1024)


start_block = 276
end_block = start_block + dim[0]*dim[1]*dim[2]


data = raw_data[start_block:end_block]

Cscan_spectra = data.reshape(dim, order='C')

Cscan_spectra = np.array(Cscan_spectra)

calibration = load_calibration(dir = calibration_file)

output_Cscan = []

C_scan = process_Cscan(Cscan_spectra)

print('%%%%%%%%%%%__ saving into pickle file__%%%%%%%%%%% \n shape of file : {0}'.format(np.shape(Bscan.tolist() ) ) )

df = DataFrame(np.array(output_Cscan).reshape(length,1049*508))

df.to_pickle(temp_dir)








#-
