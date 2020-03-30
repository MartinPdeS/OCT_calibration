'''_____Standard imports_____'''
import os
import sys
import numpy as np


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)


'''_____Project imports_____'''
from src.toolbox.parsing import Bscan_parse_arguments
arguments = Bscan_parse_arguments()
from src.toolbox.cython_loadings import load_Bscan_spectra, load_calibration
from src.toolbox.cython_plottings import Bscan_plots
from src.toolbox._arguments import Arguments
from src.toolbox.cython_filters import denoise_Bscan

if Arguments.gpu:
    from src.toolbox.cython_main_processing_gpu import process_Bscan
else:
    from src.toolbox.cython_main_processing_cpu import process_Bscan


dimension = (1,3147,1024)

Bscan_spectra = load_Bscan_spectra(Arguments.input_file, dimension = dimension)

calibration = load_calibration(dir =  Arguments.calibration_file)

Bscan = []

for iteration in range(dimension[0]):

    print( "########## iteration [{0}/{1}]".format( iteration + 1, dimension[0] ) )

    tmp = process_Bscan(Bscan_spectra[iteration], calibration)

    Bscan.append( denoise_Bscan(tmp) )


Bscan_output = np.mean(Bscan, axis=0)


if Arguments.silent is False:
    Bscan_plots(Bscan_output)



#-
