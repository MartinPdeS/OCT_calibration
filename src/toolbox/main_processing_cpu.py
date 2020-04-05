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


def process(spectra: np.ndarray, calibration: dict, shift: float):
    """
    CPU based
    """

    #spectra = np.array(spectra) + np.array(calibration['dark_not']) - np.array(calibration['dark_ref']) - np.array(calibration['dark_sample'])

    spectra = compensate_dispersion( spectra, Arguments.dispersion * np.array( calibration['dispersion'] ) )

    spectra = linearize_spectra(spectra, calibration['klinear'])

    if Arguments.shift:
        spectra = shift_spectra()

    return spectra2aline(spectra)


def process_Bscan(Bscan_spectra: np.ndarray, calibration: dict, shift: int=0):
    """
    CPU based
    """

    Bscan_spectra = scipy.signal.detrend(Bscan_spectra, axis=0)

    return process(Bscan_spectra, calibration, shift=shift)


def shift_spectra(spectra: np.ndarray, calibration: dict):

    j = complex(0,1)

    shift = calibration['peak_shift1']

    return np.real( spectra * np.exp(j * np.arange(Arguments.dimension[2]) * shift ) )

# ---
