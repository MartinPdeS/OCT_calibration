
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

from scipy.interpolate import interp1d

'''_____Project imports_____'''
from toolbox.plottings import interactive_shift, phase_dispersion_plot
from toolbox.fits import gauss, make_poly_fit, fit_dispersion
from toolbox.maths import hilbert, unwrap_phase, apodization, spectra2aline
from toolbox.filters import butter_lowpass_filter, butter_highpass_filter
from toolbox.loadings import load_calibration


def shift_spectra(spectra1, spectra2, N_pad, plot=True, args=None):


    L = len(spectra1)
    x = np.arange(L)
    j = complex(0,1)

    z_space = np.linspace(-np.pi, np.pi, L * N_pad)
    z_space = z_space[len(z_space)//2:-1]

    ff1 = np.abs( np.fft.fftshift( np.fft.fft(spectra1, L * N_pad ) ) )
    ff2 = np.abs( np.fft.fftshift( np.fft.fft(spectra2, L * N_pad ) ) )

    ff1 = ff1[len(ff1)//2:-1]
    ff2 = ff2[len(ff2)//2:-1]

    p0 = [10., 0., 1.]

    coeff1, var_matrix1 = curve_fit(gauss, z_space, ff1, p0=p0, maxfev = 20000)
    coeff2, var_matrix2 = curve_fit(gauss, z_space, ff2, p0=p0, maxfev = 20000)


    shift1_condition = False
    shift2_condition = False


    interactive_shift( ff1,
                       [z_space, *coeff1],
                       ff2,
                       [z_space, *coeff2] )



    x_shift = ( coeff1[1] + coeff2[1])/2

    c1 = ( -coeff1[1] + x_shift )
    c2 = ( -coeff2[1] + x_shift )

    shifted_spectra1 = np.real( hilbert(spectra1) * np.exp(j * x * c1 ) )
    shifted_spectra2 = np.real( hilbert(spectra2) * np.exp(j * x * c2 ) )

    return z_space, shifted_spectra1, shifted_spectra2, c1, c2


def compute_dispersion(spectra1, spectra2, c1, c2, sign_dispersion, plot=True, args=None):
    """ Compute and conpense dispersion

    """

    j = complex(0,1)
    x = np.arange( len(spectra1) )

    p1 = unwrap_phase(spectra1) + np.arange(len(spectra2))*c1
    p2 = unwrap_phase(spectra2) + np.arange(len(spectra2))*c2

    Pdisp = (p1-p2)/2
    fit_disp = make_poly_fit( x = x, y = Pdisp, order = 7 )

    Pdispersion = fit_disp(x)
    Pdispersion = Pdispersion - Pdispersion[0]

    sim_dispersion = fit_dispersion(Pdispersion)

    compensated_spectra1 = compensate_dispersion(spectra1, args.dispersion * Pdispersion)
    compensated_spectra2 = compensate_dispersion(spectra2, -args.dispersion *  Pdispersion)


    if plot:
        phase_dispersion_plot(Pdispersion, sim_dispersion)


    return compensated_spectra1, compensated_spectra2, Pdispersion



def k_linearization(spectra1, spectra2, args=None):

    phase1 = unwrap_phase(spectra1)
    phase2 = unwrap_phase(spectra2)

    x = np.arange( len(phase1) )
    Plin = (phase1 + phase2) / 2

    fit_x = make_poly_fit( x=Plin, y = x, order = 6 )
    x_klinear = fit_x( np.linspace( Plin[0], Plin[-1], len(Plin) ) )

    interpolated_spectra1 = linearize_spectra(spectra1, x_klinear)
    interpolated_spectra2 = linearize_spectra(spectra2, x_klinear)


    return x_klinear, interpolated_spectra1, interpolated_spectra2



def linearize_spectra(spectra, x_klinear):

    x = np.arange( len(spectra) )
    phase = unwrap_phase(spectra)

    interpolation = interp1d(x, spectra)
    klinear_spectra = interpolation(x_klinear)


    return klinear_spectra


def compensate_dispersion(spectra, Pdispersion):

    j = complex(0,1)

    tmp = np.real( hilbert(spectra) * np.exp( j * Pdispersion ) )

    return tmp


def process_Bscan(Bscan_spectra, sign_dispersion, Pdispersion=None):


    calibration = load_calibration()

    if Pdispersion is None:
        Pdispersion = np.array( calibration['dispersion'] )

    Bscan = []
    Spectra = []

    for i, spectra in enumerate(Bscan_spectra):

        #spectra = np.array(spectra)  - np.array(calibration['dark_not']) - np.array(calibration['dark_ref']) + np.array(calibration['dark_sample'])
        spectra = apodization(spectra)
        spectra = butter_highpass_filter(spectra, cutoff=800, fs=30000, order=6)
        spectra = butter_lowpass_filter(spectra, cutoff=5000, fs=30000, order=6)
        spectra = linearize_spectra(spectra, calibration['klinear'])
        spectra = compensate_dispersion( np.array(spectra), sign_dispersion * Pdispersion )
        Spectra.append(spectra)
        Aline = spectra2aline(spectra)
        Aline = Aline[0:len(Aline)//2]
        Bscan.append(Aline)

    return Bscan, Spectra






# -
