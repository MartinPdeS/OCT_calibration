
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter
from scipy import signal
import struct
import binascii
import copy
import json
from scipy.interpolate import interp1d


'''_____Project imports_____'''
from PySpectra import Spectra
from toolbox.parsing import parse_arguments
from toolbox.spectra_processing import process_Bscan
from toolbox.fits import get_fit_curve
from toolbox.maths import apodization
from toolbox.loadings import load_Bscan_spectra
from toolbox.plottings import Bscan_plots


with open("calibration/calibration_parameters.json") as json_file:
    calibration = json.load(json_file)

args = parse_arguments()



file = "/Volumes/USBEBE/data/" + args.input_file + '.raw'

Bscan_spectra = load_Bscan_spectra(file)



Bscan, Spectra = process_Bscan(Bscan_spectra, sign_dispersion=args.dispersion)


Bscan_plots(Spectra, Bscan)


if args.save_plots:
    fig1 = plt.figure(figsize=(16,10))
    ax3 = fig.add_subplot(111)
    plt.imshow( np.log(Bscan.T), cmap='gray')
    plt.gca().invert_yaxis()
    plt.savefig(args.input_file, bbox='tight')













#-
