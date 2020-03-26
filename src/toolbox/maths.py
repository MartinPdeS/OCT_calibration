

'''_____Standard imports_____'''
import numpy as np
import numba
from numba import jit


def hilbert(data):
    tmp = np.fft.fft(np.array(data))
    tmp[0: len(tmp)//2] = 0
    return np.fft.fft(tmp)


@jit(nopython=False)
def unwrap_phase(spectra):

    spectra = np.array(spectra)
    fft_spectra = hilbert(spectra)
    phase = np.angle( fft_spectra )
    unwrapped_phase = np.unwrap( phase )
    phase[0] = 0

    return unwrapped_phase


@jit(nopython=True)
def apodization(spectra):

    hanning = np.hanning( len(spectra) )
    spectra = hanning *  spectra

    return spectra


def spectra2aline(spectra):

    tmp0 = np.fft.fft(spectra)
    tmp1 = np.fft.fftshift( tmp0 )

    return np.abs( tmp1 )
