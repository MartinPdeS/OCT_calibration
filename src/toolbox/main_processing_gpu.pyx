
'''_____Standard imports_____'''
import numpy as np
import scipy.fftpack as fp
import scipy
import cupy as cp
from scipy.interpolate import interp1d

'''_____Project imports_____'''
from src.toolbox.maths import spectra2aline, hilbert
from src.toolbox._arguments import Arguments



def process_Bscan(Bscan_spectra, calibration, shift=0):
    """
    GPU accelerated
    """

    j = complex(0,1)

    Bscan_spectra = scipy.signal.detrend(Bscan_spectra, axis=0)

    hil = operation1(Bscan_spectra)

    if Arguments.shift:
        shift = calibration['peak_shift1']

    spectrum_shift = np.exp(j * np.arange(len(Bscan_spectra[0,:])) * shift )

    x = np.arange( len(Bscan_spectra[0,:]) )

    interpolation = interp1d(x, Bscan_spectra, kind='cubic', fill_value="extrapolate")

    Bscan = interpolation(calibration['klinear'][:])

    Bscan = operation1(Bscan)

    Bscan = np.multiply(Bscan, spectrum_shift)

    Bscan = np.real(Bscan)

    Bscan = cp.array(Bscan)

    data_output1  = cp.fft.fft(Bscan, axis=1)

    cp.cuda.Device().synchronize()

    Bscan = cp.asnumpy(data_output1)[:,:len(Bscan[0,:])//2]

    return np.flip( np.abs(Bscan), 1)


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



# ---
