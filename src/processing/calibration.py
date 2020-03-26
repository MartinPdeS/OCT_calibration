
'''_____Standard imports_____'''
import numpy as np
import json
import os
import sys
import matplotlib.pyplot as plt
import pprint
import pickle
pp = pprint.PrettyPrinter(width=41, compact=True)

'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)



'''_____Project imports_____'''
from src.toolbox.PySpectra import Spectra
from src.toolbox.parsing import Calibration_parse_arguments
Calibration_parse_arguments()
from src.toolbox.calibration_processing import compute_dispersion, k_linearization, shift_spectra, compensate_dispersion, compute_PSF, shift_1_spectra
from src.toolbox.loadings import load_data
from src.toolbox.plottings import dB_plot
from src.toolbox.maths import spectra2aline, apodization
import src.toolbox.directories as directories
from src.toolbox._arguments import Arguments


Mirror1 = Spectra(data_dir      = Arguments.input_dir + "mirror1.npy",
                  background_dir= Arguments.input_dir + "dark_not.npy",
                  sample_dir    = Arguments.input_dir + "dark_sample1.npy",
                  ref_dir       = Arguments.input_dir + "dark_ref.npy")

Mirror1.load_data()
Mirror1.process_data()

if Arguments.silent is False:

    Mirror1.plot()

Mirror2 = Spectra(data_dir       = Arguments.input_dir + "mirror2.npy",
                  background_dir = Arguments.input_dir + "dark_not.npy",
                  sample_dir     = Arguments.input_dir + "dark_sample2.npy",
                  ref_dir        = Arguments.input_dir + "dark_ref.npy")

Mirror2.load_data()
Mirror2.process_data()


if Arguments.silent is False:

    Mirror2.plot()


x_new, interpolated_spectra_1, interpolated_spectra_2 = k_linearization(Mirror1.sub_raw,
                                                                        Mirror2.sub_raw)

if Arguments.silent is False:

    dB_plot(data1=spectra2aline(interpolated_spectra_1),
            data2=spectra2aline(Mirror1.sub_raw)
            )

    dB_plot(data1=spectra2aline(interpolated_spectra_2),
            data2=spectra2aline(Mirror2.sub_raw)
            )


sys.stdout.write('Procesing spectral shift')
z_space, shifted_spectra_1, shifted_spectra_2, shift_1, shift_2 = shift_spectra(interpolated_spectra_1,
                                                                                interpolated_spectra_2,
                                                                                N_pad=100)

sys.stdout.write('Computing dispersion ...')
Pdispersion = compute_dispersion(interpolated_spectra_1,
                                 interpolated_spectra_2,
                                 shift_1,
                                 shift_2)


compensated_spectra_1 = compensate_dispersion(interpolated_spectra_1,
                                             Arguments.dispersion * Pdispersion)


compensated_spectra_2 = compensate_dispersion(interpolated_spectra_2,
                                             -Arguments.dispersion * Pdispersion)

kernel = compute_PSF(spectra2aline(compensated_spectra_1))

if Arguments.silent is False:

    dB_plot(data1=spectra2aline(compensated_spectra_1),
            data2=spectra2aline(Mirror1.sub_raw))

    dB_plot(data1=spectra2aline(compensated_spectra_2),
            data2=spectra2aline(Mirror2.sub_raw))


calib_dict = {"klinear":     list(x_new),
              "dispersion":  list(Pdispersion),
              "dark_not":    list(load_data(Arguments.input_dir + "dark_not.npy")),
              "dark_ref":    list(load_data(Arguments.input_dir + "dark_ref.npy")),
              "dark_sample": list(load_data(Arguments.input_dir + "dark_sample1.npy")),
              "peak_shift1": shift_1,
              "peak_shift2": shift_2,
              "psf_kernel" : list(kernel)
              }
if Arguments.output_file:
    sys.stdout.write('Writting json file to {0}...'.format(Arguments.output_file))
    with open(Arguments.output_file, 'wb') as outfile:
        pickle.dump(calib_dict, outfile, protocol=pickle.HIGHEST_PROTOCOL)
else:
    sys.stdout.write('Calibration file not saved... no output file declared')











#---
