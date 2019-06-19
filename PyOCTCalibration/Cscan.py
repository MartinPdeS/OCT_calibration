
'''_____Standard imports_____'''
import numpy as np
import json
import matplotlib.pyplot as plt
import sys
from pandas import DataFrame
#from skimage import restoration


'''_____Project imports_____'''
from toolbox.parsing import Bscan_parse_arguments
from toolbox.loadings import load_Bscan_spectra, load_calibration
from toolbox.fits import get_fit_curve
from toolbox.filters import butter_highpass_filter
from toolbox.spectra_processing import linearize_spectra, compensate_dispersion
from toolbox.maths import spectra2aline
from toolbox.Bscan_processing import process_Bscan, clean_Bscan




arguments = Bscan_parse_arguments()

LP = 'LP11'

Cscan_file = "/Users/macbooklodi/Desktop/Cscan_" + LP + ".raw"

calibration_file = "/Volumes/Untitled/Calibrations/lanterne/" + LP + "/calibration_parameters.json"

temp_dir = ".temporary/Cscan_" + LP + ".csv"


raw_data = np.fromfile(Cscan_file, dtype = np.uint16)


dim = (512,1049,1024)


start_block = 276
end_block = start_block + dim[0]*dim[1]*dim[2]


data = raw_data[start_block:end_block]

Cscan = data.reshape(dim, order='C')

Cscan = np.array(Cscan)

calibration = load_calibration(dir = calibration_file)

output_Cscan = []

length = 20

for iteration, Bscan_spectra in enumerate(Cscan[140: 140 + length,:,:]):

    print( '################## [{0}/{1}]'.format( iteration, length ) )

    Bscan = process_Bscan(Bscan_spectra, calibration, arguments)

    Bscan = clean_Bscan(Bscan)

    output_Cscan.append(Bscan)

print('%%%%%%%%%%%__ saving into pickle file__%%%%%%%%%%% \n shape of file : {0}'.format(np.shape(Bscan.tolist() ) ) )


df = DataFrame(np.array(output_Cscan).reshape(length,1049*508))



df.to_pickle(temp_dir)








#-
