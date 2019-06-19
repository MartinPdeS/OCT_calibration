
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter
from scipy import signal
import copy
import json
from scipy.interpolate import interp1d


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)


'''_____Project imports_____'''
from PySpectra import Spectra
from toolbox.Bscan_processing import process_Aline

dir = "data/mirror-.txt"


spectra = load_data(dir)

with open("calibration_parameters.json") as json_file:
    calibration = json.load(json_file)


spectra = np.array(spectra) - np.array(calibration['dark_not']) - np.array(calibration['dark_ref']) + np.array(calibration['dark_sample'])

plt.plot(spectra)
print("click the image to exit")
plt.waitforbuttonpress()
plt.close()

spectra = apodization(spectra)

plt.plot(spectra)
print("click the image to exit")
plt.waitforbuttonpress()
plt.close()

spectra = butter_highpass_filter(spectra,
                                 cutoff=0.8,
                                 fs=30,
                                 order=4)


spectra = linearize_spectra(spectra, np.array(calibration['klinear']) )


plt.plot(spectra)
print("click the image to exit")
plt.waitforbuttonpress()
plt.close()


spectra = compensate_dispersion(spectra, np.array(calibration['dispersion']) )

plt.plot(spectra)
print("click the image to exit")
plt.waitforbuttonpress()
plt.close()


aline = spectra2aline(spectra)

dB_plot(aline)
