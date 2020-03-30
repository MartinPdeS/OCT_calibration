
'''_____Standard imports_____'''
import numpy as np
cimport numpy as cnp


ctypedef cnp.cdouble_t CDTYPE_t
ctypedef cnp.double_t DTYPE_t



def hilbert(cnp.ndarray[DTYPE_t, ndim=1] spectra):

    cdef cnp.ndarray[cnp.cdouble_t, ndim=1] temp

    temp = np.fft.fft(np.array(spectra))

    temp[0: len(temp)//2] = 0

    return np.fft.fft(temp)


def unwrap_phase(cnp.ndarray[CDTYPE_t, ndim=1] spectra):

    fft_spectra = hilbert(spectra)

    phase = np.angle( fft_spectra )

    unwrapped_phase = np.unwrap( phase )

    unwrapped_phase[0] = 0

    return unwrapped_phase


def apodization(cnp.ndarray[CDTYPE_t, ndim=1] spectra):

    hanning = np.hanning( len(spectra) )

    spectra = hanning *  spectra

    return spectra


cdef cnp.ndarray[CDTYPE_t, ndim=1] spectra2aline(cnp.ndarray[CDTYPE_t, ndim=1] spectra):

    cdef cnp.ndarray[cnp.cdouble_t, ndim=1] ctemp

    ctemp = np.fft.fft(spectra)

    ctemp = np.fft.fftshift( ctemp )

    return np.abs( ctemp )
