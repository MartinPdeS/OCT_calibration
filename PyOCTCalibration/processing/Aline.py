
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)


'''_____Project imports_____'''
from toolbox.Bscan_processing import process_Aline
from toolbox.parsing import Aline_parse_arguments
from toolbox.loadings import load_data, load_calibration

dir = "data/mirror-.txt"

arguments = Aline_parse_arguments()

spectra = load_data(dir)

calibration = load_calibration(dir =  arguments.calibration_file)

Aline = process_Aline(spectra, calibration, shift=0, arguments=arguments)

dB_plot(Aline)
