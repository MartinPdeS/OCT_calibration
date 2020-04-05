
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from numpy import inf
from scipy.interpolate import interp1d
from numba import jit

'''_____Project imports_____'''
from src.toolbox.plottings import interactive_shift, phase_dispersion_plot, plot_klinearization, dB_plot
from src.toolbox.fits import gauss, make_poly_fit, fit_dispersion
from src.toolbox.maths import hilbert, unwrap_phase, apodization, spectra2aline
from src.toolbox.filters import butter_lowpass_filter, butter_highpass_filter, compressor
from src.toolbox.loadings import load_calibration
from src.toolbox._arguments import Arguments


def shift_spectra(spectra1, spectra2, N_pad):
    """ This method find the relative position of the FFT of the two spectras
    in order to later k-linearize.

    Args:
        :param spectra1: OCT spectra of first mirror.
        :type spectra1: list

        :param spectra2: OCT spectra of second mirror.
        :type spectra2: list

        :param N_pad: Padding for the FFT.
        :type N_pad: int

    Return:
        :rname: Zspace: - pi to pi linear vector space
        :rtype: list

        :rname: shift_1: spectral relative shift for mirror_1
        :rtype: float

        :rname: shift_2: spectral relative shift for mirror_2
        :rtype: float
    """
    L = len(spectra1)
    x = np.arange(L)
    j = complex(0,1)

    z_space = np.linspace(-np.pi, np.pi, L * N_pad)
    z_space = z_space[len(z_space)//2:-1]

    ff1 = np.abs( np.fft.fftshift( np.fft.fft(spectra1, L * N_pad ) ) )
    ff2 = np.abs( np.fft.fftshift( np.fft.fft(spectra2, L * N_pad ) ) )

    ff1 = ff1[len(ff1)//2:-1]
    ff2 = ff2[len(ff2)//2:-1]

    ff1 = compressor(ff1)
    ff2 = compressor(ff2)

    p0 = [10., 0., 0.1]

    coeff1, var_matrix1 = curve_fit(gauss, z_space, ff1, p0=p0, maxfev = 20000)
    coeff2, var_matrix2 = curve_fit(gauss, z_space, ff2, p0=p0, maxfev = 20000)

    shift1_condition = False
    shift2_condition = False

    if Arguments.interactive:
        coeff1[1], coeff2[1] = interactive_shift(ff1,
                                                 [z_space, *coeff1],
                                                 ff2,
                                                 [z_space, *coeff2])

    x_shift = ( coeff1[1] + coeff2[1]) / 2

    shift_1 = ( -coeff1[1] + x_shift )
    shift_2 = ( -coeff2[1] + x_shift )

    shifted_spectra1 = np.real( hilbert(spectra1) * np.exp(j * x * shift_1 ) )
    shifted_spectra2 = np.real( hilbert(spectra2) * np.exp(j * x * shift_2 ) )

    return z_space, shifted_spectra1, shifted_spectra2, shift_1, shift_2





def shift_1_spectra(spectra, shift):
    """ This method find the relative position of the FFT of the two spectras
    in order to later k-linearize.

    Args:
        :param spectra1: OCT spectra of first mirror.
        :type spectra1: list


    Return:
        :rname: Zspace: - pi to pi linear vector space
        :rtype: list


    """

    L = len(spectra)

    mean = np.max(spectra)

    x = np.arange(L)

    j = complex(0,1)

    shifted_spectra = np.real( hilbert(spectra) * np.exp(j * x * shift ) )

    shift_mean = np.max(shifted_spectra)

    shifted_spectra = (shifted_spectra / shift_mean) * mean

    return shifted_spectra


def compute_dispersion(spectra1, spectra2, shift_1, shift_2):
    """ This method compute the dispersion on a k-linearized OCT spectra of
    two mirror exactly opposed relative to the zero delay point.

    Args:
        :param spectra1: OCT spectra of first mirror.
        :type spectra1: list

        :param spectra2: OCT spectra of second mirror.
        :type spectra2: list

        :param shift_1: spectral relative shift for mirror_1.
        :type float

        :name shift_2: spectral relative shift for mirror_2.
        :type float

    Return:
        :rname: Pdispersion: The phase dispersion.
        :rtype: list
    """
    j = complex(0,1)
    x = np.arange( len(spectra1) )

    p1 = unwrap_phase(spectra1) + np.arange(len(spectra2))*shift_1
    p2 = unwrap_phase(spectra2) + np.arange(len(spectra2))*shift_2

    Pdisp = (p1-p2)/2
    Pdisp -= Pdisp[0]


    fit_disp = make_poly_fit( x = x, y = Pdisp, order = 5 )

    Pdispersion = fit_disp(x)

    if Arguments.silent is False:

        phase_dispersion_plot(Pdisp, Pdispersion)


    return Pdispersion


def k_linearization(spectra1, spectra2):
    """ This method compute the k-linear fractional indexes and interpolate
    the two spectras in order to compensate it.

    Args:
        :param spectra1: OCT spectra of first mirror.
        :type spectra1: list

        :param spectra2: OCT spectra of second mirror.
        :type spectra2: list


    Return:
        :rname: x_klinear: The fractional indexes.
        :rtype: list

        :rname: interpolated_spectra1: First k-linear intepolated spectra.
        :rtype: list

        :rname: interpolated_spectra2: Second k-linear intepolated spectra.
        :rtype: list

    """
    phase1, phase2 = unwrap_phase(spectra1), unwrap_phase(spectra2)

    phase1 -= phase1[0]
    phase2 -= phase2[0]

    x = np.arange( len(phase1) )

    Plin = (phase1 + phase2) / 2

    fit_Plin = make_poly_fit( x=x, y = Plin, order = 5)

    Plin = fit_Plin( x )

    if Arguments.silent is False:

        plot_klinearization(phase1, phase2, Plin)

    weight = np.ones(len(Plin))

    fit_x = make_poly_fit( x=Plin, y = x, order = 5, weight=weight )

    x_klinear = fit_x( np.linspace( Plin[0], Plin[-1], len(Plin) ) )

    coefs3 = np.polynomial.polynomial.polyfit(x, x_klinear, 5)

    ffit3 = np.poly1d(coefs3[::-1])

    x_klinear = ffit3(x)[0:]

    interpolated_spectra1 = linearize_spectra(spectra1, x_klinear)
    interpolated_spectra2 = linearize_spectra(spectra2, x_klinear)

    return x_klinear, interpolated_spectra1, interpolated_spectra2


def linearize_spectra(spectra: np.ndarray, x_klinear):
    """ This method interpolate the input spectra with the input list.

    Args:
        :param spectra: OCT spectra of mirror.
        :type spectra1: list

        :name x_klinear: The fractional indexes.
        :type list

    Return:
        :rname: klinear_spectra: The interpolated spectra.
        :rtype: list

    """
    x = np.arange( Arguments.dimension[2] )

    interpolation = interp1d(x,
                             spectra,
                             kind='cubic',
                             fill_value="extrapolate",
                             axis=-1)

    return interpolation(x_klinear[:])


def compensate_dispersion(spectra: np.ndarray, Pdispersion):
    """ This method compensate the input spectra with the input phase dispersion.

    Args:
        :param spectra: OCT spectra of mirror.
        :type spectra1: list

        :name Pdispersion: Phase dispersion.
        :type list

    Return:
        :rname: compensated_spectra : The compensated spectra.
        :rtype: list

    """
    j = complex(0,1)

    compensated_spectra = np.real( hilbert(spectra) * np.exp( j * Pdispersion ) )

    return compensated_spectra



def compute_PSF(aline):

    N_max = np.argmax(aline)

    N_start = N_max - 12
    N_end = N_max + 12

    kernel = aline[N_start:N_end]

    x = np.arange(len(kernel))

    fit_kernel = make_poly_fit( x=x, y = kernel, order = 8 )

    kernel = fit_kernel( x )

    return kernel


















# -
