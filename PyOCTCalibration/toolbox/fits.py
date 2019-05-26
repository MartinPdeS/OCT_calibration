
'''_____Standard imports_____'''
import numpy as np
from scipy.optimize import curve_fit


def gauss(x, *p):
    A, mu, sigma = p
    return A*np.exp(-(x-mu)**2/(2.*sigma**2))


def beta(x, *p):
    B1, B2, B3, B4, B5 = p
    return B1 * x + B2 * x**2 + B3 * x**3 + B4 * x**4 + B5 * x**5


def make_poly_fit(x=[],y=[], order = 5):

    coefs = np.polynomial.polynomial.polyfit(x, y, order)
    ffit = np.poly1d(coefs[::-1])
    return ffit


def fit_dispersion(Pdispersion):

    p0 = [0., 0., 0., 0., 0.]
    x = np.arange( len(Pdispersion) )

    coeff, var_matrix = curve_fit(beta, x, Pdispersion, p0=p0, maxfev = 20000)
    B1, B2, B3, B4, B5 = coeff[0], coeff[1], coeff[2], coeff[3], coeff[4]

    sim_dispersion = B1 * x + B2 * x**2 + B3 * x**3 + B4 * x**4 + B5 * x**5

    print('\n B1: {0},\n B2: {1},\n B3: {2},\n B4: {3}\n B5:{4}'.format(coeff[0],
                                                                      coeff[1],
                                                                      coeff[2],
                                                                      coeff[3],
                                                                      coeff[4]))

    return sim_dispersion


def get_fit_curve(coeff, length=1024):

    B1 = coeff[0]
    B2= coeff[1]
    B3= coeff[2]
    B4= coeff[3]
    B5= coeff[4]
    x=np.arange(length)
    sim_dispersion = B1 * x + B2 * x **2 + B3 * x **3 + B4 * x **4 + B5 * x**5

    return sim_dispersion
