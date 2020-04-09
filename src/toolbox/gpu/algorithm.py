# -MPdSH

'''_____Standard imports_____'''
import numpy as np
import cupy as cp
import cupyx

'''_____Project imports_____'''
from src.toolbox._arguments import Arguments


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


def resampling_2Dmapping(coordinates):

    a = np.concatenate([coordinates]*Arguments.dimension[1])

    b = np.repeat(np.arange(Arguments.dimension[1]), Arguments.dimension[2])

    c = np.swapaxes( list(zip(b,a)), 1,0 )

    return cp.asarray(c)
