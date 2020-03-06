
'''_____Standard imports_____'''
import numpy as np
import json
import scipy.fftpack as fp
import matplotlib.pyplot as plt
import sys
import sys
import numba
from numba import jit

'''_____Project imports_____'''
from src.toolbox.filters import butter_highpass_filter
from src.toolbox.calibration_processing import linearize_spectra, compensate_dispersion
from src.toolbox.maths import spectra2aline, hilbert


def process_Aline(spectra, calibration, shift, arguments):

    #spectra = np.array(spectra) + np.array(calibration['dark_not']) - np.array(calibration['dark_ref']) - np.array(calibration['dark_sample'])

    spectra = butter_highpass_filter(spectra, cutoff=180, fs=30000, order=5)

    spectra = linearize_spectra(spectra, calibration['klinear'])

    j = complex(0,1)

    spectra = np.real( hilbert(spectra) * np.exp(j * np.arange(len(spectra)) * shift ) )

    spectra = compensate_dispersion( np.array(spectra), arguments.dispersion * np.array( calibration['dispersion'] ) )

    Aline = spectra2aline(spectra)

    Aline = Aline[0:len(Aline)//2]

    return Aline


def process_Bscan(Bscan_spectra, calibration, shift=0, arguments=None):

    Bscan = []

    for i, spectrum in enumerate(Bscan_spectra):

        Aline = process_Aline(spectrum, calibration, shift=shift, arguments=arguments)

        Bscan.append(Aline)

    Bscan = np.array(Bscan)

    #temp = np.fft.fftshift(np.fft.fft2(Bscan))
    #mid = np.shape(temp)[0]//2
    #temp[mid-10:mid+10,:]=0
    #temp = np.fft.fft2(temp)

    #return np.abs(temp[:,::-1])
    return Bscan


def denoise_Bscan(Bscan):

    F1 = fp.fft2((Bscan).astype(float))

    F2 = fp.fftshift(F1)

    F2[500:530,:] = 0

    (w, h) = Bscan.shape

    half_w, half_h = int(w/2), int(h/2)

    F2[0 :1024, half_h -1 : half_h + 1] = 0

    Bscan = np.abs(fp.ifft2(fp.ifftshift(F2)).real)

    return Bscan


def process_Cscan(Cscan_spectra, calibration, shift, arguments):

    output_Cscan = []

    for iteration, Bscan_spectra in enumerate(Cscan_spectra):

        sys.stdout.write('Computing Cscan {0}{1}\n'.format(iteration, np.shape(Cscan_spectra)) )

        Bscan = process_Bscan(Bscan_spectra, calibration, shift=shift, arguments=arguments)

        Bscan = denoise_Bscan(Bscan)

        output_Cscan.append(Bscan)

    return output_Cscan



# ---
