
'''_____Standard imports_____'''
import numpy as np
import json

def load_data(dir):

    data = []
    file = open(dir,'r')
    for line in file:
        data.append(float(line))
    return data


def load_Bscan_spectra(file_dir, block_start=276, block_end = 632084, shape1=617, shape2=1024):

    data = np.fromfile(file_dir, dtype = np.uint16)

    block_end = block_start + 1024*1024

    block_data = data[block_start: block_end]
    Bscan_spectra = block_data.reshape([1024,1024])
    return Bscan_spectra


def load_calibration(dir=None):

    if dir is None:
        dir = "calibration/calibration_parameters.json"

    with open(dir) as json_file:
        calibration = json.load(json_file)

    return calibration
