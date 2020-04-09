# -MPdSH

'''_____Standard imports_____'''
import numpy as np
import scipy.fftpack as fp
import scipy

'''_____Project imports_____'''
from src.toolbox.maths import spectra2aline, hilbert
from scipy.interpolate import interp1d
from src.toolbox._arguments import Arguments


def linearize_spectra(spectra: np.ndarray, x_klinear: list) -> list:
    """
    This method interpolate the input spectra with the input x_klinear.

    Args:
        :param spectra: OCT spectra of mirror.
        :type spectra1: list
        :param x_klinear: The fractional indexes.
        :type x_klinear: list

    Return:
        :rname: klinear_spectra: The interpolated spectra.
        :rtype: list

    """
    x = np.arange( Arguments.dimension[2] )

    interpolation = interp1d(x,
                             spectra,
                             kind='cubic',
                             fill_value="extrapolate",
                             axis=-1)

    return interpolation(x_klinear[:])


def compensate_dispersion(spectra: np.ndarray, Pdispersion: np.ndarray) -> np.array:
    """
    This method compensate the input spectra with the input phase dispersion.

    Args:
        :param spectra: OCT spectra of mirror.
        :type: spectra1: list
        :param Pdispersion: Phase dispersion.
        :type Pdispersion: list

    Return:
        :rname: compensated_spectra : The compensated spectra.
        :rtype: list

    """
    j = complex(0,1)

    return np.real( hilbert(spectra) * np.exp( j * Pdispersion ) )
