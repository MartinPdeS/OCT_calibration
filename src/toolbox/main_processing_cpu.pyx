
'''_____Standard imports_____'''
import numpy as np
import scipy.fftpack as fp
import scipy
cimport numpy as cnp

'''_____Project imports_____'''
from src.toolbox.filters import butter_highpass_filter
from src.toolbox.calibration_processing import linearize_spectra, compensate_dispersion
from src.toolbox cimport maths
#from src.toolbox.maths import hilbert, spectra2aline
from src.toolbox.cython_maths import spectra2aline, hilbert
from src.toolbox._arguments import Arguments



def process_Aline(spectra, calibration, int shift):
    """
    CPU based
    """

    #spectra = np.array(spectra) + np.array(calibration['dark_not']) - np.array(calibration['dark_ref']) - np.array(calibration['dark_sample'])

    spectra = butter_highpass_filter(spectra.astype(np.float), cutoff=180, fs=30000, order=5)

    spectra = linearize_spectra(spectra, calibration['klinear'])

    j = complex(0,1)

    spectra = np.real( hilbert(spectra) * np.exp(j * np.arange(len(spectra)) * shift ) )

    spectra = compensate_dispersion( np.array(spectra), Arguments.dispersion * np.array( calibration['dispersion'] ) )

    Aline = spectra2aline(spectra)

    Aline = Aline[0:len(Aline)//2]

    return Aline


def process_Bscan(cnp.ndarray Bscan_spectra, calibration, shift=0):
    """
    CPU based
    """

    cdef cnp.ndarray[cnp.float_t, ndim=2] Bscan = np.zeros((Arguments.dimension[0], Arguments.dimension[-1]//2)).astype(np.float)

    Bscan_spectra = scipy.signal.detrend(Bscan_spectra, axis=0)

    for i, spectrum in enumerate(Bscan_spectra):

        Aline = process_Aline(spectrum, calibration, shift= shift)

        Bscan[i,:] = Aline

    Bscan = np.array(Bscan)

    return Bscan



# ---
