
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
import os, sys


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)


'''_____Project imports_____'''
from src.toolbox.spectra_processing import process_Aline
from src.toolbox.parsing import Aline_parse_arguments
from src.toolbox.loadings import load_data, load_calibration
from src.toolbox.maths import spectra2aline
from src.toolbox.plottings import dB_plot

arguments = Aline_parse_arguments()

spectra = load_data(arguments.input_file)

calibration = load_calibration(dir =  arguments.calibration_file)

Aline = process_Aline(spectra, calibration, shift=0, arguments=arguments)

dB_plot(data1=Aline,
        data2=spectra2aline(spectra)[0:len(spectra)//2])
