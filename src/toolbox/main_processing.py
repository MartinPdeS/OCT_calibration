
'''_____Standard imports_____'''
import numpy as np
import json
import scipy.fftpack as fp
import matplotlib.pyplot as plt
import sys
import scipy
import cupy as cp
from scipy.interpolate import interp1d

'''_____Project imports_____'''
from src.toolbox.filters import butter_highpass_filter
from src.toolbox.calibration_processing import linearize_spectra, compensate_dispersion
from src.toolbox.maths import spectra2aline, hilbert


def process_Aline(spectra, calibration, shift, arguments):
    """
    CPU based
    """

    #spectra = np.array(spectra) + np.array(calibration['dark_not']) - np.array(calibration['dark_ref']) - np.array(calibration['dark_sample'])

    spectra = butter_highpass_filter(spectra, cutoff=180, fs=30000, order=5)

    spectra = linearize_spectra(spectra, calibration['klinear'])

    j = complex(0,1)

    spectra = np.real( hilbert(spectra) * np.exp(j * np.arange(len(spectra)) * shift ) )

    spectra = compensate_dispersion( np.array(spectra), arguments.dispersion * np.array( calibration['dispersion'] ) )

    Aline = spectra2aline(spectra)

    Aline = Aline[0:len(Aline)//2]

    return Aline


def _process_Bscan(Bscan_spectra, calibration, shift=0, arguments=None):
    """
    GPU accelerated
    """

    j = complex(0,1)

    Bscan_spectra = scipy.signal.detrend(Bscan_spectra, axis=0)

    hil = operation1(Bscan_spectra)

    if arguments.shift:
        shift = calibration['peak_shift1']

    spectrum_shift = np.exp(j * np.arange(len(Bscan_spectra[0,:])) * shift )

    x = np.arange( len(Bscan_spectra[0,:]) )

    interpolation = interp1d(x, Bscan_spectra, kind='cubic')

    Bscan = interpolation(calibration['klinear'][:])

    Bscan = operation1(Bscan)

    Bscan = np.multiply(Bscan, spectrum_shift)

    Bscan = np.real(Bscan)

    Bscan = cp.array(Bscan)

    data_output1  = cp.fft.fft(Bscan, axis=1)

    cp.cuda.Device().synchronize()

    Bscan = cp.asnumpy(data_output1)[:,:len(Bscan[0,:])//2]

    return np.abs(Bscan)


def operation1(Bscan_spectra):

    temp = cp.array(Bscan_spectra)

    data_output = cp.fft.fft(temp,axis=1)

    cp.cuda.Device().synchronize()

    temp = cp.asnumpy(data_output)

    temp[:, 0: len(temp[0,:])//2] = 0

    temp = cp.array(temp)

    temp_output = cp.fft.fft(temp,axis=1)

    cp.cuda.Device().synchronize()

    hil = cp.asnumpy(temp_output)

    return hil


def process_Bscan(Bscan_spectra, calibration, shift=0, arguments=None):
    """
    CPU based
    """

    Bscan = []

    for i, spectrum in enumerate(Bscan_spectra):

        Aline = process_Aline(spectrum, calibration, shift=shift, arguments=arguments)

        Bscan.append(Aline)

    Bscan = np.array(Bscan)

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
