# -

'''_____Standard imports_____'''
import numpy as np
import cupy as cp
import os, sys
import time

import pandas


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)

'''_____Arguments parsing/loading_____'''
from src.toolbox.parsing import Cscan_parse_arguments
arguments = Cscan_parse_arguments()
from src.toolbox._arguments import Arguments
from src.toolbox.loadings import make_dataframe
from src.toolbox.gpu.algorithm import resampling_2Dmapping


'''_____Project imports_____'''
from src.toolbox.loadings import load_calibration

if Arguments.compiled:
    if Arguments.gpu:
        from src.toolbox.cython.main_processing_gpu import process_2D
    else:
        from src.toolbox.cython.main_processing_cpu import process_2D
else:

    if Arguments.gpu:
        from src.toolbox.gpu.processing import process_2D
    else:
        from src.toolbox.cpu.processing import process_2D


def main():

    calibration = load_calibration(dir = Arguments.calibration_file)

    Bscan_list = [os.path.join(Arguments.input_directory, s) for s in os.listdir(Arguments.input_directory)]

    if Arguments.gpu:
        resampling = resampling_2Dmapping(calibration['klinear'])
        dispersion = cp.asarray(calibration['dispersion'])

    sys.stdout.write('Processing ... \n')

    dataframe = make_dataframe(Arguments.dimension[0],
                               Arguments.dimension[1],
                               Arguments.dimension[2]//2)

    for n_i, Bscan_dir in enumerate(Bscan_list):

        if n_i % 10 == 0:
            sys.stdout.write('Loading data: {0} [{1}/{2}] \n'.format(Bscan_dir, n_i, len(Bscan_list) ) )

        if Arguments.gpu:
            dataframe.loc[n_i] =  process_2D(cp.load(Bscan_dir).astype(cp.float32),
                                             resampling,
                                             dispersion)

        else:
            dataframe.loc[0] = process_2D(np.load(Bscan_dir), calibration)

    if Arguments.gpu:
        cp.cuda.Device().synchronize()

    return dataframe




if __name__ == "__main__":

    T0 = time.time()

    dataframe = main()

    T1 = time.time()

    sys.stdout.write('Processing finished in [ {0:7.5f} seconde] \n'.format(T1-T0))

    if Arguments.silent:

        import napari

        napari.gui_qt()

        with napari.gui_qt():

            viewer = napari.view_image(dataframe.values.reshape(100,100,512))

#-
