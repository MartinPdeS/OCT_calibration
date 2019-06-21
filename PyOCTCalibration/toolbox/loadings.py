
'''_____Standard imports_____'''
import numpy as np
import json

def load_data(dir):

    data = []
    file = open(dir,'r')
    for line in file:
        data.append(float(line))
    return data


def load_Bscan_spectra(file_dir, block_start=276, dimension=(1,1049,1024)):

    data = np.fromfile(file_dir, dtype = np.uint16)

    header_size = 276
    foot_size = 4096
    buffer_size = 19

    data = data[header_size:]
    data = data[:-foot_size]

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()

    begin = 0
    end = 1024*1049

    tmp = []

    for iter in range(dimension[0]-1):
        begin = end + 20
        end = begin + 1024*1049
        tmp.append( np.reshape( data[begin:end],[1049,1024] ) )


    return tmp


def load_calibration(dir=None):

    if dir is None:
        dir = "calibration/calibration_parameters.json"

    with open(dir) as json_file:
        calibration = json.load(json_file)

    return calibration
