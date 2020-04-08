# -MPdSH

'''_____Standard imports_____'''
import numpy as np
import cupy as cp
from scipy.interpolate import interp1d
import cupyx
import cupyx.scipy.ndimage

'''_____Project imports_____'''
from src.toolbox._arguments import Arguments

def process_3D(Volume_spectra: np.ndarray, calibration: dict) -> np.array:
    """
    GPU accelerated
    """

    Volume_spectra = detrend_3D(Volume_spectra)

    Volume_spectra = linearize_spectra_3D(cp.asnumpy(Volume_spectra), calibration)

    temp = cp.array(Volume_spectra)

    temp = compensate_dispersion_3D(temp, calibration)

    if Arguments.shift:

        temp = spectrum_shift(temp)

    temp  = cp.fft.rfft(temp, axis=2)[:,:,:Arguments.dimension[2]//2]

    temp = cp.absolute(temp)

    cp.cuda.Device().synchronize()

    return cp.asnumpy(temp)


def linearize_spectra_3D(temp: np.ndarray, calibration: dict):

    x = np.arange(start=0, stop=Arguments.dimension[2])

    interpolation = interp1d(x,
                             temp,
                             axis=2,
                             kind='cubic',
                             fill_value="extrapolate")

    return interpolation(calibration['klinear'][:])


def spectrum_shift_3D(temp: cp.ndarray):

    spectrum_shift = cp.exp(complex(0,1) * cp.arange( start=0, stop=Arguments.dimension[2] ) * shift )

    temp = cp.multiply(temp, spectrum_shift)

    temp = cp.real(temp)


def hilbert_3D(temp: cp.ndarray) -> cp.array:

    temp = cp.fft.rfft(temp, axis=2)[:,:,:Arguments.dimension[2]//2]

    dum =  cp.zeros_like(temp)

    temp = cp.concatenate( (temp*2,dum), axis=2)

    return cp.fft.ifft(temp, axis=2)


def detrend_3D(Volume_spectra):

     Volume_spectra = cp.fft.rfft(Volume_spectra, axis=1)

     Volume_spectra[:,:10,:] = 0

     Volume_spectra = cp.fft.irfft(Volume_spectra, axis=1)

     return Volume_spectra



def compensate_dispersion_3D(spectra: np.ndarray, calibration: dict) -> cp.array:

    calib = cp.asarray(calibration['dispersion'])

    Pdispersion = cp.asarray( calib * complex(0,1) * Arguments.dispersion )

    return cp.real( hilbert_3D(spectra) * cp.exp( Pdispersion ) )



###############______2D_______##################################################


def process_2D(Volume_spectra: cp.ndarray, coordinates: cp.ndarray, dispersion: cp.array) -> np.array:
    """
    This function process 2D array of spectrum to return adjusted Bscan.

    :param Volume_spectra: 2nd order tensor containing spectras raw data. Last dimension is depth encoding.
    :type Volume_spectra: cp.ndarray
    :param coordinates: 2D array containing coordinates for k-linearization interpolation.
    :type coordinates: cp.ndarray
    :param dispersion: Array with value for dispersion compensation.
    :type dispersion: cp.array
    """

    dtype = Volume_spectra.dtype

    Volume_spectra = detrend_2D(Volume_spectra)

    Volume_spectra = compensate_dispersion_2D(Volume_spectra, dispersion)

    Volume_spectra = linearize_spectra_2D(Volume_spectra, coordinates)

    if Arguments.shift:

        temp = spectrum_shift(Volume_spectra)

    Volume_spectra  = cp.fft.rfft(Volume_spectra.astype(dtype), axis=1)[:,:Arguments.dimension[2]//2]

    Volume_spectra = cp.absolute(Volume_spectra)

    return cp.asnumpy( Volume_spectra[:,:Arguments.dimension[2]//2] )


def linearize_spectra_2D(Volume_spectra: cp.ndarray, coordinates: cp.ndarray) -> cp.ndarray:

    res = cupyx.scipy.ndimage.map_coordinates(Volume_spectra,
                                              coordinates=coordinates,
                                              output=None,
                                              order=1,
                                              mode='nearest')

    return cp.reshape(res,(Arguments.dimension[1],Arguments.dimension[2]))


def spectrum_shift_2D(Volume_spectra: cp.ndarray):

    spectrum_shift = cp.exp(complex(0,1) * cp.arange( start=0, stop=Arguments.dimension[2] ) * shift )

    Volume_spectra = cp.multiply(Volume_spectra, spectrum_shift)

    Volume_spectra = cp.real(Volume_spectra)


def hilbert_2D(Volume_spectra: cp.ndarray) -> cp.array:

    Volume_spectra = cp.fft.rfft(Volume_spectra, axis=1)[:,:Arguments.dimension[2]//2]

    dum =  cp.zeros_like(Volume_spectra)

    Volume_spectra = cp.concatenate( (Volume_spectra*2,dum), axis=1)

    return cp.fft.ifft(Volume_spectra, axis=1)


def detrend_2D(Volume_spectra):

     Volume_spectra = cp.fft.rfft(Volume_spectra, axis=0)

     Volume_spectra[:10,:] = 0

     Volume_spectra = cp.fft.irfft(Volume_spectra, axis=0)

     return Volume_spectra



def compensate_dispersion_2D(Volume_spectra: np.ndarray, dispersion) -> cp.array:

    Pdispersion = cp.asarray( dispersion * complex(0,1) * Arguments.dispersion )

    return cp.real( hilbert_2D(Volume_spectra) * cp.exp( Pdispersion ) )



# ---
