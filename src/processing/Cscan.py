# -

'''_____Standard imports_____'''
import numpy as np
import cupy as cp
import os
import tables
import sys
import time

'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)

'''_____Arguments parsing/loading_____'''
from src.toolbox.parsing import Cscan_parse_arguments
arguments = Cscan_parse_arguments()
from src.toolbox._arguments import Arguments
from src.toolbox.calibration_processing import resampling_2Dmapping



'''_____Project imports_____'''
from src.toolbox.loadings import load_calibration

if Arguments.compiled:
    if Arguments.gpu:
        from src.toolbox.cython.main_processing_gpu import process_2D
    else:
        from src.toolbox.cython.main_processing_cpu import process_2D
else:

    if Arguments.gpu:
        from src.toolbox.main_processing_gpu import process_2D
    else:
        from src.toolbox.main_processing_cpu import process_2D

calibration = load_calibration(dir = Arguments.calibration_file)

Bscan_list = [os.path.join(Arguments.input_directory, s) for s in os.listdir(Arguments.input_directory)]

if Arguments.gpu:
    Cscan = cp.ndarray( (Arguments.dimension[0], Arguments.dimension[1], Arguments.dimension[2]//2) )
    resampling = resampling_2Dmapping(calibration['klinear'])
else:
    Cscan = np.ndarray( (Arguments.dimension[0], Arguments.dimension[1], Arguments.dimension[2]//2) )



T0 = time.time()
sys.stdout.write('Processing ... \n')

for n_i, Bscan_dir in enumerate(Bscan_list):

    sys.stdout.write('Loading data: {0} [{1}/{2}] \n'.format(Bscan_dir, n_i, len(Bscan_list) ) )

    if Arguments.gpu:
        Cscan[n_i,:,:] = process_2D(cp.load(Bscan_dir), calibration, resampling)
    else:
        Cscan[n_i,:,:] = process_2D(np.load(Bscan_dir), calibration)



Cscan = cp.asnumpy(Cscan)

T1 = time.time()
sys.stdout.write('Processing finished in [ {0:7.5f} seconde] \n'.format(T1-T0))

if Arguments.save:

    sys.stdout.write('Saving into {0} file \n'.format(Arguments.output_file ) )

    f = tables.open_file(Arguments.output_file, mode='w')

    atom = tables.Float64Atom()

    array_c = f.create_earray(f.root, 'data', atom, (0, Arguments.dimension[1], Arguments.dimension[2]/2))

    array_c.append(temp)

    f.close()




if Arguments.silent:

    import napari

    napari.gui_qt()

    with napari.gui_qt():

        viewer = napari.view_image(Cscan)


#-
