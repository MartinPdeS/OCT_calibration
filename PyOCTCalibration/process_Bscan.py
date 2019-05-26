
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


with open("calibration/calibration_parameters.json") as json_file:
    calibration = json.load(json_file)

args = parse_arguments()



file = "/Volumes/USBEBE/data/" + args.input_file + '.raw'

Bscan_spectra = load_Bscan_spectra(file)



Bscan, Spectra = process_Bscan(Bscan_spectra, sign_dispersion=args.dispersion)
Bscan = np.array(Bscan)


fig = plt.figure(figsize=(16,10))

ax0 = fig.add_subplot(221)
ax0.grid()
ax0.set_ylabel('Magnitude [dB]')
ax0.set_xlabel('Wavenumber k [U.A]')
ax0.set_title("Spectra")
ax0.plot(Spectra[200])


ax1 = fig.add_subplot(222)
ax1.grid()
ax1.set_ylabel('Magnitude [dB]')
ax1.set_xlabel('Wavenumber k [U.A]')
ax1.set_title("Aline")
ref = np.min(Bscan[200])
ax1.plot( 10*np.log(Bscan[200]/ref) )
ax1.invert_xaxis()


ax2 = fig.add_subplot(223)


data = np.log(Bscan.T)
#data = image_high_pass(data=data, axis=1)
print(np.min(data), np.max(data))
ax2.imshow( data, cmap='gray', vmin=10, vmax= np.max(data) )
ax2.set_title("Processed Bscan")
ax2.invert_yaxis()


plt.show()


if args.save_plots:
    fig1 = plt.figure(figsize=(16,10))
    ax3 = fig.add_subplot(111)
    plt.imshow( np.log(Bscan.T), cmap='gray')
    plt.gca().invert_yaxis()
    plt.savefig(args.input_file, bbox='tight')













#-
