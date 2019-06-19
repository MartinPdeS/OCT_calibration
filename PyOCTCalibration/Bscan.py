
'''_____Standard imports_____'''
import numpy as np
import json
import scipy.fftpack as fp
import matplotlib.pyplot as plt
#from skimage import restoration


'''_____Project imports_____'''
from toolbox.parsing import Bscan_parse_arguments
from toolbox.loadings import load_Bscan_spectra, load_calibration
from toolbox.plottings import Bscan_plots
from toolbox.fits import get_fit_curve
from toolbox.filters import butter_highpass_filter
from toolbox.spectra_processing import linearize_spectra, compensate_dispersion
from toolbox.maths import spectra2aline


arguments = Bscan_parse_arguments()


Bscan_file = arguments.input_file
calibration_file = arguments.calibration_file

Bscan_spectra = load_Bscan_spectra(Bscan_file)

calibration = load_calibration(dir = calibration_file)

Pdispersion = np.array( calibration['dispersion'] )

#psf_kernel = np.array([calibration["psf_kernel"]])


Bscan = []
Spectra = []
Aline_intensity = []

for i, spectra in enumerate(Bscan_spectra):

    spectra = np.array(spectra) + np.array(calibration['dark_not']) - np.array(calibration['dark_ref']) - np.array(calibration['dark_sample'])
    #spectra = np.array(spectra) - np.array(calibration['dark_ref']) #- np.array(calibration['dark_ref']) - np.array(calibration['dark_sample'])
    #spectra = apodization(spectra)
    Aline_intensity.append( np.sum(spectra) )
    spectra = butter_highpass_filter(spectra, cutoff=180, fs=30000, order=5)
    spectra = linearize_spectra(spectra, calibration['klinear'])
    spectra = compensate_dispersion( np.array(spectra), arguments.dispersion * Pdispersion )
    Spectra.append(spectra)
    Aline = spectra2aline(spectra)
    Aline = Aline[0:len(Aline)//2]
    #Aline = restoration.richardson_lucy(np.array([Aline]), psf_kernel, iterations=30)
    Bscan.append(Aline)

plt.plot(Aline_intensity)
print("click the image to exit")
plt.waitforbuttonpress()
plt.close()

Bscan = np.array(Bscan)

F1 = fp.fft2((Bscan).astype(float))

F2 = fp.fftshift(F1)

F2[500:540,:], F2[511,:] = 0, 0

(w, h) = Bscan.shape

half_w, half_h = int(w/2), int(h/2)

F2[0 :1024, half_h -1 : half_h + 1] = 0

Bscan = np.abs(fp.ifft2(fp.ifftshift(F2)).real)

Bscan_plots(Spectra, Bscan, arguments=arguments)





#-
