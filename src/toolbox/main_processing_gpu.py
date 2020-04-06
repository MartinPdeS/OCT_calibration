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

def process_volume(Volume_spectra: np.ndarray, calibration: dict) -> np.array:
    """
    GPU accelerated
    """

    Volume_spectra = detrend(Volume_spectra)

    Volume_spectra = linearize_spectra(cp.asnumpy(Volume_spectra), calibration)

    temp = cp.array(Volume_spectra)

    temp = compensate_dispersion(temp, calibration)

    if Arguments.shift:

        temp = spectrum_shift(temp)

    temp  = cp.fft.rfft(temp, axis=2)[:,:,:Arguments.dimension[2]//2]

    temp = cp.absolute(temp)

    cp.cuda.Device().synchronize()

    return cp.asnumpy(temp)


def linearize_spectra(temp: np.ndarray, calibration: dict):

    x = np.arange(start=0, stop=Arguments.dimension[2])

    interpolation = interp1d(x,
                             temp,
                             axis=2,
                             kind='cubic',
                             fill_value="extrapolate")

    return interpolation(calibration['klinear'][:])


def spectrum_shift(temp: cp.ndarray):

    spectrum_shift = cp.exp(complex(0,1) * cp.arange( start=0, stop=Arguments.dimension[2] ) * shift )

    temp = cp.multiply(temp, spectrum_shift)

    temp = cp.real(temp)


def hilbert(temp: cp.ndarray) -> cp.array:

    temp = cp.fft.rfft(temp, axis=2)[:,:,:Arguments.dimension[2]//2]

    dum =  cp.zeros_like(temp)

    temp = cp.concatenate( (temp*2,dum), axis=2)

    return cp.fft.ifft(temp, axis=2)


def detrend(Volume_spectra):

     Volume_spectra = cp.fft.rfft(Volume_spectra, axis=1)

     Volume_spectra[:,:10,:] = 0

     Volume_spectra = cp.fft.irfft(Volume_spectra, axis=1)

     return Volume_spectra



def compensate_dispersion(spectra: np.ndarray, calibration: dict) -> cp.array:

    calib = cp.asarray(calibration['dispersion'])

    Pdispersion = cp.asarray( calib * complex(0,1) * Arguments.dispersion )

    return cp.real( hilbert(spectra) * cp.exp( Pdispersion ) )


# ---
