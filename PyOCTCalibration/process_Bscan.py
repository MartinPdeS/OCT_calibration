
'''_____Standard imports_____'''
import numpy as np
import json
import scipy.fftpack as fp


'''_____Project imports_____'''
from toolbox.parsing import parse_arguments
from toolbox.loadings import load_Bscan_spectra, load_calibration
from toolbox.plottings import Bscan_plots
from toolbox.fits import get_fit_curve
from toolbox.filters import butter_highpass_filter
from toolbox.spectra_processing import linearize_spectra, compensate_dispersion
from toolbox.maths import spectra2aline


arguments = parse_arguments()




Bscan_dir = "/Volumes/Untitled/Calibrations/Bscan/"
file = Bscan_dir + arguments.input_file

Bscan_spectra = load_Bscan_spectra(file)


calibration = load_calibration()


Pdispersion = np.array( calibration['dispersion'] )



Bscan = []
Spectra = []

for i, spectra in enumerate(Bscan_spectra):

    spectra = np.array(spectra) + np.array(calibration['dark_not']) - np.array(calibration['dark_ref']) - np.array(calibration['dark_sample'])
    #spectra = np.array(spectra) - np.array(calibration['dark_ref']) #- np.array(calibration['dark_ref']) - np.array(calibration['dark_sample'])
    #spectra = apodization(spectra)
    spectra = butter_highpass_filter(spectra, cutoff=180, fs=30000, order=5)
    #spectra = butter_lowpass_filter(spectra, cutoff=5000, fs=30000, order=6)
    spectra = linearize_spectra(spectra, calibration['klinear'])
    spectra = compensate_dispersion( np.array(spectra), arguments.dispersion * Pdispersion )
    Spectra.append(spectra)
    Aline = spectra2aline(spectra)
    Aline = Aline[0:len(Aline)//2]
    Bscan.append(Aline)

Bscan = np.array(Bscan)
F1 = fp.fft2((Bscan).astype(float))
F2 = fp.fftshift(F1)

F2[500:540,:] = 0
F2[511,:] = 0
(w, h) = Bscan.shape
half_w, half_h = int(w/2), int(h/2)

F2[0 :1024, half_h -1 : half_h + 1] = 0
#plt.figure(figsize=(10,10))
#plt.imshow( (20*np.log10( 0.1 + F2)).astype(int))
#plt.show()

Bscan = np.abs(fp.ifft2(fp.ifftshift(F2)).real)
print(np.max(Bscan), np.min(Bscan))


Bscan = np.array(Bscan)











Bscan_plots(Spectra, Bscan, arguments=arguments)
















#-
