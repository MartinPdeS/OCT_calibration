
'''_____Standard imports_____'''
import numpy as np
import json


'''_____Project imports_____'''
from toolbox.parsing import parse_arguments
from toolbox.spectra_processing import process_Bscan
from toolbox.loadings import load_Bscan_spectra
from toolbox.plottings import Bscan_plots
from toolbox.fits import get_fit_curve


args = parse_arguments()

file = "/Volumes/USBEBE/data/" + args.input_file + '.raw'

Bscan_spectra = load_Bscan_spectra(file)

B1=-0.4151697340967216
B2=0.0004651524028133154
B3=4.1227160200685674e-07
B4=-5.30274776612886e-10
B5=2.165488418343404e-13

sim_dispersion = get_fit_curve([B1, B2, B3, B4, B5])

Bscan, Spectra = process_Bscan(Bscan_spectra, sign_dispersion=args.dispersion, Pdispersion=sim_dispersion)

Bscan_plots(Spectra, Bscan, args=args)
















#-
