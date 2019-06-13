
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





def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='valid')
    return y_smooth



arguments = Bscan_parse_arguments()


Bscan_file_LP01 = "/media/dude/0041-BB6B/Calibrations/lanterne/LP01/boiss_1.raw"
Bscan_file_LP11 = "/media/dude/0041-BB6B/Calibrations/lanterne/LP11/boiss_0.raw"


calibration_file_LP01 = "/media/dude/0041-BB6B/Calibrations/lanterne/LP01/calibration_parameters.json"
calibration_file_LP11 = "/media/dude/0041-BB6B/Calibrations/lanterne/LP11/calibration_parameters.json"


Bscan_spectra_LP01 = load_Bscan_spectra(Bscan_file_LP01)
Bscan_spectra_LP11 = load_Bscan_spectra(Bscan_file_LP11)

calibration_LP01 = load_calibration(dir = calibration_file_LP01)
calibration_LP11 = load_calibration(dir = calibration_file_LP11)

Pdispersion_LP01 = np.array( calibration_LP01['dispersion'] )
Pdispersion_LP11 = np.array( calibration_LP11['dispersion'] )



Bscan_LP01 = []
Spectra_LP01 = []
Aline_intensity_LP01 = []

for i, spectra_LP01 in enumerate(Bscan_spectra_LP01):

    Aline_intensity_LP01.append( np.sum( spectra2aline(spectra_LP01) ) )
    spectra_LP01 = np.array(spectra_LP01) + np.array(calibration_LP01['dark_not']) - np.array(calibration_LP01['dark_ref']) - np.array(calibration_LP01['dark_sample'])
    #Spectra_LP01 = butter_highpass_filter(Spectra_LP01, cutoff=180, fs=30000, order=5)
    spectra_LP01 = linearize_spectra(spectra_LP01, calibration_LP01['klinear'])
    spectra_LP01 = compensate_dispersion( np.array(spectra_LP01), arguments.dispersion * Pdispersion_LP01 )
    Spectra_LP01.append(Spectra_LP01)
    Aline_LP01 = spectra2aline(spectra_LP01)
    Aline_LP01 = Aline_LP01[0:len(Aline_LP01)//2]
    Bscan_LP01.append(Aline_LP01)



Bscan_LP11 = []
Spectra_LP11 = []
Aline_intensity_LP11 = []

for i, spectra_LP11 in enumerate(Bscan_spectra_LP11):

    Aline_intensity_LP11.append( np.sum( spectra2aline(spectra_LP11) ) )
    spectra_LP11 = np.array(spectra_LP11) + np.array(calibration_LP11['dark_not']) - np.array(calibration_LP11['dark_ref']) - np.array(calibration_LP11['dark_sample'])
    #Spectra_LP11 = butter_highpass_filter(Spectra_LP11, cutoff=180, fs=30000, order=5)
    spectra_LP11 = linearize_spectra(spectra_LP11, calibration_LP11['klinear'])
    spectra_LP11 = compensate_dispersion( np.array(spectra_LP11), arguments.dispersion * Pdispersion_LP11 )
    Spectra_LP11.append(Spectra_LP11)
    Aline_LP11 = spectra2aline(spectra_LP11)
    Aline_LP11 = Aline_LP11[0:len(Aline_LP11)//2]
    Bscan_LP11.append(Aline_LP11)



Aline_intensity_LP11 = smooth(Aline_intensity_LP11,10)
Aline_intensity_LP01 = smooth(Aline_intensity_LP01,10)

Bscan_LP01 = np.array(Bscan_LP01)
Bscan_LP11 = np.array(Bscan_LP11)


F1_LP01 = fp.fft2((Bscan_LP01).astype(float))
F1_LP11 = fp.fft2((Bscan_LP11).astype(float))

F2_LP01 = fp.fftshift(F1_LP01)
F2_LP11 = fp.fftshift(F1_LP11)



F2_LP01[500:540,:], F2_LP01[511,:] = 0, 0
F2_LP11[500:540,:], F2_LP11[511,:] = 0, 0

(w, h) = Bscan_LP01.shape

half_w, half_h = int(w/2), int(h/2)

F2_LP01[0 :1024, half_h -1 : half_h + 1] = 0
F2_LP11[0 :1024, half_h -1 : half_h + 1] = 0

Bscan_LP01 = np.abs(fp.ifft2(fp.ifftshift(F2_LP01)).real)
Bscan_LP11 = np.abs(fp.ifft2(fp.ifftshift(F2_LP11)).real)


frac = np.array(Aline_intensity_LP11)/np.array(Aline_intensity_LP01)
print(np.max(frac), np.min(frac))

Bscan_plots(Aline_intensity_LP01, Aline_intensity_LP11, Bscan_LP01, arguments=arguments)





#-
