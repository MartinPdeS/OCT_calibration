
'''_____Standard imports_____'''
import numpy as np
import os
import tables
import sys


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)

'''_____Project imports_____'''
from src.toolbox.parsing import Cscan_parse_arguments
arguments = Cscan_parse_arguments()
from src.toolbox.loadings import load_calibration
from src.toolbox.main_processing_gpu import *
from src.toolbox._arguments import Arguments


if Arguments.gpu:
    from src.toolbox.cython_main_processing_gpu import process_Bscan
else:
    from src.toolbox.cython_main_processing_cpu import process_Bscan

calibration = load_calibration(dir = Arguments.calibration_file)

Bscan_list = os.listdir(Arguments.input_directory)

Bscan_list = [os.path.join(Arguments.input_directory, s) for s in Bscan_list]

outfile = Arguments.output_file

f = tables.open_file(outfile, mode='w')

atom = tables.Float64Atom()

array_c = f.create_earray(f.root, 'data', atom, (0, Arguments.dimension[1], Arguments.dimension[2]/2))

for n_i, Bscan_spectra in enumerate(Bscan_list):

    sys.stdout.write('Bscan processing ... [{0}/{1}] \n'.format(n_i, len(Bscan_list) ) )

    raw_Bscan_spectra = np.load(Bscan_spectra)

    Bscan = [process_Bscan(raw_Bscan_spectra, calibration)]

    array_c.append(Bscan)

    del Bscan

sys.stdout.write(' saving into {0} file \n'.format(Arguments.output_file ) )

f.close()









#-
