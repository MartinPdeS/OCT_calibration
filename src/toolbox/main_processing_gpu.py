# -MPdSH

'''_____Standard imports_____'''
import numpy as np
import scipy.signal
import cupy as cp
from scipy.interpolate import interp1d


'''_____Project imports_____'''
from src.toolbox._arguments import Arguments



def process_Bscan(Bscan_spectra: np.ndarray, calibration: dict):
    """
    GPU accelerated
    """

    x = np.arange( Arguments.dimension[2] )

    print(Arguments.dimension[2])
    j = complex(0,1)

    temp = scipy.signal.detrend(Bscan_spectra, axis=0).astype("float64")

    print(np.shape(temp))

    interpolation = interp1d(x, temp, kind='cubic', fill_value="extrapolate")

    temp = interpolation(calibration['klinear'][:])

    ctemp = operation1(temp)

    if Arguments.shift:

        shift = calibration['peak_shift1']

        spectrum_shift = np.exp(j * np.arange( Arguments.dimension[2] ) * shift )

        ctemp = np.multiply(ctemp, spectrum_shift)

    temp = np.real(ctemp)

    cp_temp = cp.array(temp)

    cp_temp  = cp.fft.fft(cp_temp, axis=1)

    cp.cuda.Device().synchronize()

    ctemp = cp.asnumpy(cp_temp)[:,:len(ctemp[0,:])//2]

    return np.flip( np.abs(ctemp), 1)



def operation1(Bscan_spectra: np.ndarray):

    temp = cp.array(Bscan_spectra)

    temp = cp.fft.fft(temp, axis=1)

    cp.cuda.Device().synchronize()

    ctemp_t = cp.asnumpy(temp)

    ctemp_t[:, 0: len(ctemp_t[0,:])//2] = 0

    temp = cp.array(ctemp_t)

    temp = cp.fft.fft(temp,axis=1)

    cp.cuda.Device().synchronize()

    ctemp_t = cp.asnumpy(temp)

    return ctemp_t


# ---
