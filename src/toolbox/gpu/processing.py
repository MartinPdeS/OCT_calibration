# -MPdSH

'''_____Standard imports_____'''
import numpy as np
import cupy as cp
from scipy.interpolate import interp1d
import cupyx.scipy.fftpack as fftpack
import cupyx.scipy.ndimage


'''_____Project imports_____'''
from src.toolbox._arguments import Arguments
from src.toolbox.gpu.algorithm import detrend_2D, detrend_1D, compensate_dispersion_2D, linearize_spectra_2D, linearize_spectra_1D, spectrum_shift_2D

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

    if Arguments.dimension[1] == 1:
        Volume_spectra = cp.expand_dims(Volume_spectra, axis=0)
        coordinates = cp.array([coordinates[1]])
        Volume_spectra = detrend_1D(Volume_spectra)

    else:
        Volume_spectra = detrend_2D(Volume_spectra)

    Volume_spectra = compensate_dispersion_2D(Volume_spectra, dispersion)

    if Arguments.dimension[1] == 1:
        Volume_spectra = linearize_spectra_1D(Volume_spectra, coordinates)

    else:
        Volume_spectra = linearize_spectra_2D(Volume_spectra, coordinates)

    Volume_spectra  = fftpack.fft(Volume_spectra,
                                   axis=1,
                                   overwrite_x=True)[:,:Arguments.dimension[2]//2]



    return cp.asnumpy( cp.absolute(Volume_spectra[:,:Arguments.dimension[2]//2] ) )






# ---
