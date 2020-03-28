
'''_____Standard imports_____'''
import numpy as np
cimport numpy as cnp


def hilbert(cnp.ndarray[cnp.double_t, ndim=1] data):

    cdef cnp.ndarray[cnp.cdouble_t, ndim=1] temp

    temp = np.fft.fft(np.array(data))

    temp[0: len(temp)//2] = 0

    return np.fft.fft(temp)


def unwrap_phase(cnp.ndarray[cnp.double_t, ndim=1] spectra):

    spectra = np.array(spectra)

    fft_spectra = hilbert(spectra)

    phase = np.angle( fft_spectra )

    unwrapped_phase = np.unwrap( phase )

    phase[0] = 0

    return unwrapped_phase


def apodization(cnp.ndarray[cnp.double_t, ndim=1] spectra):

    hanning = np.hanning( len(spectra) )

    spectra = hanning *  spectra

    return spectra


def spectra2aline(cnp.ndarray[cnp.double_t, ndim=1] spectra):

    cdef cnp.ndarray[cnp.cdouble_t, ndim=1] temp

    temp = np.fft.fft(spectra)

    temp = np.fft.fftshift( temp )

    return np.abs( temp )
