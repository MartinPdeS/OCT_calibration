
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
import copy
import json
import argparse


'''_____Project imports_____'''
from toolbox.PySpectra import Spectra
from toolbox.parsing import parse_arguments
from toolbox.loadings import load_Bscan_spectra
from toolbox.spectra_processing import process_Bscan



args = parse_arguments()


Beta = {'B1': -0.4151697340967216,
        'B2': 0.0004651524028133154,
        'B3': 4.1227160200685674e-07,
        'B4': -5.30274776612886e-10,
        'B5': 2.165488418343404e-13}


x = np.arange(1024)

betaN = None
for i in range(100):


    if betaN is None or factor is None:
        betaN = input("What beta?")

    factor = input("What multiplicative factor for betaN? [type q to quit or press to change betaN]")

    if factor == 'q':
        break

    if betaN is None or factor is '':
        betaN = input("What beta?")
        factor = input("What multiplicative factor for betaN? [type q to quit or press to change betaN]")

    print(betaN)
    Beta[betaN] *= eval(factor)
    sim_dispersion = Beta['B1'] * x + Beta['B2'] * x **2 + Beta['B3'] * x **3 + Beta['B4'] * x **4 + Beta['B5'] * x**5


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


    fig.canvas.draw()
    print( '{ \n B1:{0},\n B2:{1},\n B3:{2},\n B4:{3},\n B5:{4},\n Next iteration?\n }'.format(Beta['B1'],
                                                                                           Beta['B2'],
                                                                                           Beta['B3'],
                                                                                           Beta['B4'],
                                                                                           Beta['B5']) )











    # -
