
'''_____Standard imports_____'''
import numpy as np
cimport numpy as cnp
import scipy.signal
import cupy as cp
from scipy.interpolate import interp1d

'''_____Project imports_____'''
from src.toolbox.maths import spectra2aline, hilbert
from src.toolbox._arguments import Arguments

ctypedef cnp.cdouble_t CDTYPE_t
ctypedef cnp.double_t DTYPE_t


def process_Bscan(cnp.ndarray Bscan_spectra, calibration):
    """
    GPU accelerated
    """

    cdef cnp.ndarray[cnp.double_t, ndim=2] temp

    cdef cnp.ndarray[cnp.cdouble_t, ndim=2] ctemp

    j = complex(0,1)

    temp = scipy.signal.detrend(Bscan_spectra, axis=0).astype("float64")

    x = np.arange( len(Bscan_spectra[0,:]) )

    interpolation = interp1d(x, temp, kind='cubic', fill_value="extrapolate")

    temp = interpolation(calibration['klinear'][:])

    ctemp = operation1(temp)

    if Arguments.shift:

        shift = calibration['peak_shift1']

        spectrum_shift = np.exp(j * np.arange(len(Bscan_spectra[0,:])) * shift )

        ctemp = np.multiply(ctemp, spectrum_shift)

    temp = np.real(ctemp)

    cp_temp = cp.array(temp)

    cp_temp  = cp.fft.fft(cp_temp, axis=1)

    cp.cuda.Device().synchronize()

    ctemp = cp.asnumpy(cp_temp)[:,:len(ctemp[0,:])//2]

    return np.flip( np.abs(ctemp), 1)


cdef cnp.ndarray[CDTYPE_t, ndim=1] operation1(cnp.ndarray[cnp.double_t, ndim=2] Bscan_spectra):

    cdef cnp.ndarray[cnp.double_t, ndim=2] temp_t

    cdef cnp.ndarray[cnp.cdouble_t, ndim=2] ctemp_t

    temp = cp.array(Bscan_spectra)

    temp = cp.fft.fft(temp, axis=1)

    cp.cuda.Device().synchronize()

    ctemp_t = cp.asnumpy(temp)

    ctemp_t[:, 0: len(ctemp_t[0,:])//2] = 0

    temp = cp.array(ctemp_t)

    temp = cp.fft.fft(temp,axis=1)

    cp.cuda.Device().synchronize()

    ctemp_t = cp.asnumpy(temp)

    return ctemp_t


# ---
