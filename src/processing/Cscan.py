
'''_____Standard imports_____'''
import numpy as np
import os
import tables
import sys
import scipy


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)

'''_____Project imports_____'''
from src.toolbox.parsing import Cscan_parse_arguments
from src.toolbox.loadings import load_calibration
from src.toolbox.spectra_processing import  _process_Bscan
import src.toolbox.directories as directories
from src.toolbox.spectra_processing import *


arguments = Cscan_parse_arguments()

calibration = load_calibration(dir = arguments.calibration_file)

Bscan_list = os.listdir(arguments.input_directory)

Bscan_list = [os.path.join(arguments.input_directory, s) for s in Bscan_list]

Cscan = []

outfile = arguments.output_file

ROW_SIZE = 100

NUM_COLUMNS = 100

f = tables.open_file(outfile, mode='w')

atom = tables.Float64Atom()

array_c = f.create_earray(f.root, 'data', atom, (0, arguments.dimension[1], arguments.dimension[2]/2))

for n_i, Bscan_spectra in enumerate(Bscan_list):

    sys.stdout.write('Bscan processing ... [{0}/{1}] \n'.format(n_i, len(Bscan_list) ) )

    raw_Bscan_spectra = np.load(Bscan_spectra)

    if arguments.gpu:
        Bscan = [_process_Bscan(raw_Bscan_spectra, calibration, shift=0, arguments=arguments)]
    else:
        Bscan = [process_Bscan(raw_Bscan_spectra, calibration, shift=0, arguments=arguments)]

    #Bscan = denoise_Bscan(Bscan)

    array_c.append(Bscan)

    del Bscan


#Cscan = scipy.signal.detrend(Cscan, axis=0, type='constant')

#Cscan = scipy.signal.detrend(Cscan, axis=1, type='constant')

sys.stdout.write(' saving into {0} file \n shape of file : {1}'.format(arguments.output_file, str( np.shape( Cscan ) ) ) )

f.close()









#-
