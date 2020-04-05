# -

'''_____Standard imports_____'''
import numpy as np
import scipy.signal

'''_____Project imports_____'''
from src.toolbox._arguments import Arguments


def hilbert(spectra: np.array):
    #temp = np.fft.fft(spectra)
    #temp[512:] = 0
    #temp = np.fft.ifft(temp)
    #return temp

    return scipy.signal.hilbert(spectra)


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
    print(np.shape(spectra))

    ctemp = np.fft.fft(spectra)

    return np.abs( ctemp[:,:,0:Arguments.dimension[2]//2] )
