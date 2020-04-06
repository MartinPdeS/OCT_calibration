# -MPdSH

'''_____Standard imports_____'''
import numpy as np
import scipy.fftpack as fp
import scipy

'''_____Project imports_____'''
from src.toolbox.filters import butter_highpass_filter
from src.toolbox.calibration_processing import linearize_spectra, compensate_dispersion
from src.toolbox.maths import spectra2aline, hilbert
from src.toolbox._arguments import Arguments




def process_2D(Volume_spectra: np.ndarray, calibration: dict, shift: int=0):
    """
    CPU based
    """

    Volume_spectra = scipy.signal.detrend(Volume_spectra, axis=0, type='linear')

    Volume_spectra = compensate_dispersion(Volume_spectra, Arguments.dispersion * np.array( calibration['dispersion'] ))

    Volume_spectra = linearize_spectra(Volume_spectra, calibration['klinear'])

    if Arguments.shift:
        spectra = shift_spectra(Volume_spectra, calibration)

    return spectra2aline([Volume_spectra])[0,:,:Arguments.dimension[2]//2]


def shift_spectra(Volume_spectra: np.ndarray, calibration: dict):

    j = complex(0,1)

    shift = calibration['peak_shift1']

    return np.real( Volume_spectra * np.exp(j * np.arange(Arguments.dimension[2]) * shift ) )



# ---
