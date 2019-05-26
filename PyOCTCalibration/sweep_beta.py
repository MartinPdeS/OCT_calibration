
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter
from scipy import signal
import copy
import json
from scipy.interpolate import interp1d
import argparse


'''_____Project imports_____'''
from tools import *
from PySpectra import Spectra
from parsing import parse_arguments



args = parse_arguments()


B1= -0.5433615672020556
B2= 0.0019722375486931633
B3= -5.040153501008985e-06
B4= 6.095879607615912e-09
B5= -2.340301943551366e-12

x = np.arange(1024)


for i in range(20):
    B5 *= (1+0.01)
    sim_dispersion = B1 * x + B2 * x **2 + B3 * x **3 + B4 * x **4 + B5 * x**5


    file = "/Volumes/USBEBE/data/" + args.input_file + '.raw'

    Bscan_spectra = load_Bscan_spectra(file)

    Bscan, Spectra = process_Bscan(Bscan_spectra, sign_dispersion=args.dispersion, Pdispersion=sim_dispersion)
    Bscan = np.array(Bscan)


    fig = plt.figure(figsize=(8,8))
    plt.ion()

    ax0 = fig.add_subplot(121)
    ax0.grid()
    ax0.set_ylabel('Magnitude [dB]')
    ax0.set_xlabel('Wavenumber k [U.A]')
    ax0.set_title("Spectra")
    ax0.plot(Spectra[200])
    ax0.set_autoscale_on(False)



    ax1 = fig.add_subplot(122)
    ax1.grid()
    ax1.set_ylabel('Magnitude [dB]')
    ax1.set_xlabel('Wavenumber k [U.A]')
    ax1.set_title("Aline")
    ref = np.min(Bscan[200])
    ax1.plot( 10*np.log(Bscan[200]/ref) )
    ax1.invert_xaxis()
    #ax1.set_xlim([400,500])


    print(B5)
    fig.canvas.draw()
    input( '\n B1:{0},\n B2:{1},\n B3:{2},\n B4:{3},\n B5:{4},\n Next iteration?\n'.format(B1,
                                                                                           B2,
                                                                                           B3,
                                                                                           B4,
                                                                                           B5) )











    # -
