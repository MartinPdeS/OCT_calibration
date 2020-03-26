
'''_____Standard imports_____'''
import numpy as np
import json



def load_data(dir, type=float):

    data = []

    data = np.load(dir)

    return data


def load_Bscan_spectra(file_dir, dimension=(1,1024,3147)):

    data = np.load(file_dir)
    data = np.reshape(data, dimension)

    return data


def load_calibration(dir=None):

    if dir is None:
        dir = "calibration/calibration_parameters.json"

    with open(dir) as json_file:
        calibration = json.load(json_file)

    return calibration
