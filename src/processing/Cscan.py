# -

'''_____Standard imports_____'''
import numpy as np
import os
import tables
import sys


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)

'''_____Arguments parsing/loading_____'''
from src.toolbox.parsing import Cscan_parse_arguments
arguments = Cscan_parse_arguments()
from src.toolbox._arguments import Arguments



'''_____Project imports_____'''
from src.toolbox.loadings import load_calibration

if Arguments.compiled:
    if Arguments.gpu:
        from src.toolbox.cython.main_processing_gpu import process_Bscan
    else:
        from src.toolbox.cython.main_processing_cpu import process_Bscan
else:

    if Arguments.gpu:
        from src.toolbox.main_processing_gpu import process_Bscan
    else:
        from src.toolbox.main_processing_cpu import process_Bscan

calibration = load_calibration(dir = Arguments.calibration_file)

Bscan_list = [os.path.join(Arguments.input_directory, s) for s in os.listdir(Arguments.input_directory)]

length = len(Bscan_list)

Cscan = np.empty( Arguments.dimension )

for n_i, Bscan_dir in enumerate(Bscan_list):

    sys.stdout.write('Loading data: {0} [{1}/{2}] \n'.format(Bscan_dir, n_i, length ) )

    Cscan[n_i,:,:] = np.load(Bscan_dir)

sys.stdout.write('Processing ... \n')

temp = process_Bscan(Cscan, calibration)

sys.stdout.write('Saving into {0} file \n'.format(Arguments.output_file ) )
"""
f = tables.open_file(Arguments.output_file, mode='w')

atom = tables.Float64Atom()

array_c = f.create_earray(f.root, 'data', atom, (0, Arguments.dimension[1], Arguments.dimension[2]/2))

array_c.append(temp)

f.close()
"""

if not Arguments.silent:

    import napari

    napari.gui_qt()

    with napari.gui_qt():

        viewer = napari.view_image(temp)

#-
