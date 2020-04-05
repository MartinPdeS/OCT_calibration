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

def process_volume(Volume_spectra: np.ndarray, calibration: dict):
    """
    GPU accelerated
    """

    Volume_spectra = scipy.signal.detrend(Volume_spectra, axis=1, type='linear').astype("float64")

    Volume_spectra = linearize_spectra(Volume_spectra, calibration)


    """ CUPY solution can't choose axis!
    temp = cupyx.scipy.ndimage.map_coordinates(input=temp,
                                               coordinates=x,
                                               output=None,
                                               order=1,
                                               mode='nearest')
    """

    temp = cp.array(Volume_spectra)

    temp = compensate_dispersion(temp, calibration)

    if Arguments.shift:

        temp = spectrum_shift(temp)

    temp  = cp.fft.rfft(temp, axis=2)[:,:,:Arguments.dimension[2]//2]

    temp = cp.absolute(temp * 2)

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


def hilbert(temp: cp.ndarray):

    temp = cp.fft.rfft(temp, axis=2)[:,:,:Arguments.dimension[2]//2]

    dum =  cp.zeros_like(temp)

    temp = cp.concatenate( (temp*2,dum), axis=2)

    return cp.fft.ifft(temp, axis=2)


def compensate_dispersion(spectra: np.ndarray, calibration: dict):

    calib = cp.asarray(calibration['dispersion'])

    Pdispersion = cp.asarray( calib * complex(0,1) * Arguments.dispersion )

    return cp.real( hilbert(spectra) * cp.exp( Pdispersion ) )


# ---
