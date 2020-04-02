# -

'''_____Standard imports_____'''
import numpy as np


def hilbert(spectra: np.array):

    temp = np.fft.fft(np.array(spectra))

    temp[0: len(temp)//2] = 0

    return np.fft.fft(temp)


def unwrap_phase(spectra: np.array):

    temp = hilbert(spectra)

    temp = np.angle( temp )

    temp = np.unwrap( temp )

    temp[0] = np.float64(0)

    return temp


def apodization(spectra: np.array):

    hanning = np.hanning( len(spectra) )

    spectra = hanning *  spectra

    return spectra


def spectra2aline(spectra: np.array):

    ctemp = np.fft.fft(spectra)

    ctemp = np.fft.fftshift( ctemp )

    return np.abs( ctemp )
