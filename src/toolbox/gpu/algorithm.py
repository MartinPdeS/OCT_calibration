# -MPdSH

'''_____Standard imports_____'''
import numpy as np
import cupy as cp
import cupyx.scipy.ndimage
import cupyx.scipy.fftpack as fftpack

'''_____Project imports_____'''
from src.toolbox._arguments import Arguments


def linearize_spectra_2D(Volume_spectra: cp.ndarray, coordinates: cp.ndarray) -> cp.ndarray:
    """
    This methode resample each of the spectrum of the Bscan simultaneously \
    in order to compensate for nonk-linear spectrum.

    Args:
        :param Volume_spectra: 2nd order tensor containing spectras raw data. Last dimension is depth encoding.
        :type Volume_spectra: cp.ndarray
        :param coordinates: 2D array containing coordinates for k-linearization interpolation.
        :type coordinates: cp.ndarray
        :param dispersion: Array with value for dispersion compensation.
        :type dispersion: cp.array

    Return:
        :rparam: Resampled (linearized) array of spectrum.
        :rtype: cp.ndarray
    """
    res = cupyx.scipy.ndimage.map_coordinates(Volume_spectra,
                                              coordinates=coordinates,
                                              output=None,
                                              order=1,
                                              mode='nearest')

    return cp.reshape(res,(Arguments.dimension[1],Arguments.dimension[2]))


def spectrum_shift_2D(Volume_spectra: cp.ndarray) -> cp.ndarray:

    spectrum_shift = cp.exp(complex(0,1) * cp.arange( start=0, stop=Arguments.dimension[2] ) * shift )

    Volume_spectra = cp.multiply(Volume_spectra, spectrum_shift)

    Volume_spectra = cp.real(Volume_spectra)


def hilbert_2D(Volume_spectra: cp.ndarray) -> cp.array:
    """
    Compute the analytic signal, using the Hilbert transform. \
    The transformation is done along the last axis.

    Args:
        Volume_spectra::cp.ndarray
        2nd order tensor containing spectras raw data. Last dimension is depth encoding.

    Returns:
        Analytical signal of Volume_spectra::cp.ndarray
        :rtype: cp.ndarray

    Notes
    -----
    The analytic signal ``x_a(t)`` of signal ``x(t)`` is:
    .. math:: x_a = F^{-1}(F(x) 2U) = x + i y

    """

    if cp.iscomplexobj(Volume_spectra):
        raise ValueError("x must be real.")

    Volume_spectra = fftpack.fft(Volume_spectra,
                                  axis=-1,
                                  overwrite_x=True)[:,:Arguments.dimension[2]//2]

    dum =  cp.zeros_like(Volume_spectra)

    Volume_spectra = cp.concatenate( (Volume_spectra*2,dum), axis=1)

    return cp.fft.ifft(Volume_spectra, axis=1)


def detrend_2D(Volume_spectra):
    """
    This methode remove lateral DC component of Bscan, this way it get \
    rid of recurent noise from one Aline to the other.

    Args:
        :param Volume_spectra: 2nd order tensor containing spectras raw data. Last dimension is depth encoding.
        :type Volume_spectra: cp.ndarray

    Return:
        :rparam: Laterally DC-removed Volume_spectra.
        :rtype: cp.ndarray
    """

    Volume_spectra = fftpack.rfft(Volume_spectra,
                                   axis=0,
                                   overwrite_x=True)

    Volume_spectra[:10,:] = 0


    Volume_spectra = fftpack.irfft(Volume_spectra,
                                   axis=0,
                                   overwrite_x=True)

    return Volume_spectra


def compensate_dispersion_2D(Volume_spectra: np.ndarray, dispersion) -> cp.array:

    Pdispersion = cp.asarray( dispersion * complex(0,1) * Arguments.dispersion )

    return cp.real( hilbert_2D(Volume_spectra) * cp.exp( Pdispersion ) )


def resampling_2Dmapping(coordinates):
    """
    Knowing resampling fractionale indices this methode generate the 2-D list \
    for the methode map_coordinates to use.

    Args:
        :param coordinates: 2D array containing coordinates for k-linearization interpolation.
        :type coordinates: cp.ndarray

    Return:
        :rparam: Array of 2D coordinates for interpolation.
        :rtype: cp.ndarray
    """

    a = np.concatenate([coordinates]*Arguments.dimension[1])

    b = np.repeat(np.arange(Arguments.dimension[1]), Arguments.dimension[2])

    c = np.swapaxes( list(zip(b,a)), 1,0 )

    return cp.asarray(c)
