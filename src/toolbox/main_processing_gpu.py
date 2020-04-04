# -MPdSH

'''_____Standard imports_____'''
import numpy as np
import scipy.signal
import cupy as cp
from scipy.interpolate import interp1d
import cupyx
import cupyx.scipy.ndimage

'''_____Project imports_____'''
from src.toolbox._arguments import Arguments
from src.toolbox.filters import butter_highpass_filter

def process_Bscan(Volume_spectra: np.ndarray, calibration: dict):
    """
    GPU accelerated
    """

    x = np.arange(start=0,
                  stop=Arguments.dimension[2])

    j = complex(0,1)
    print(np.shape(Volume_spectra))
    import matplotlib.pyplot as plt
    plt.plot(Volume_spectra[1,1,:])
    plt.show()
    temp = scipy.signal.detrend(Volume_spectra, axis=(0,1), type='constant').astype("float64")
    #temp = butter_highpass_filter(Volume_spectra, cutoff=1000, fs=30000, order=5)
    plt.plot(temp[1,1,:])
    plt.show()
    interpolation = interp1d(x, temp, axis=2, kind='cubic', fill_value="extrapolate")

    temp = interpolation(calibration['klinear'][:])

    """ CUPY solution can't choose axis!
    temp = cupyx.scipy.ndimage.map_coordinates(input=temp,
                                               coordinates=x,
                                               output=None,
                                               order=1,
                                               mode='nearest')
    """


    temp = cp.array(temp)

    temp = compute_analytical(temp)

    if Arguments.shift:

        temp = spectrum_shift(temp)

    temp = cp.real(temp)

    temp  = cp.fft.fft(temp, axis=2)

    temp = temp[:,:,:Arguments.dimension[2]//2]

    temp = cp.absolute(temp)

    cp.cuda.Device().synchronize()

    temp = cp.asnumpy(temp)

    return temp


def spectrum_shift(temp: cp.ndarray):

    spectrum_shift = np.exp(j * np.arange( Arguments.dimension[2] ) * shift )

    temp = cp.multiply(temp, spectrum_shift)


def compute_analytical(temp: cp.ndarray):

    temp = cp.fft.fft(temp, axis=2)

    temp[:,:,:Arguments.dimension[2]//2] = 0

    temp = cp.fft.ifft(temp, axis=2)

    return temp


# ---
