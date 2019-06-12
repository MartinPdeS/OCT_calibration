
'''_____Standard imports_____'''
import numpy as np
import json
import sys
import matplotlib.pyplot as plt


'''_____Project imports_____'''
from toolbox.PySpectra import Spectra
from toolbox.parsing import parse_arguments
from toolbox.spectra_processing import compute_dispersion, k_linearization, shift_spectra, compensate_dispersion, compute_PSF
from toolbox.loadings import load_data
from toolbox.plottings import dB_plot
from toolbox.maths import spectra2aline, apodization

arguments = parse_arguments()


spectra_dir = "/Volumes/Untitled/Calibrations/lanterne/LP11/"
calibration_dir = "/Volumes/Untitled/OCT_calibration/PyOCTCalibration/calibration/"

Mirror1 = Spectra(data_dir=spectra_dir + "mirror1.txt",
                  background_dir=spectra_dir + "dark_not.txt",
                  sample_dir=spectra_dir + "dark_sample1.txt",
                  ref_dir=spectra_dir + "dark_ref.txt")

Mirror1.load_data()
Mirror1.process_data()

Mirror2 = Spectra(data_dir=spectra_dir + "mirror2.txt",
                  background_dir=spectra_dir + "dark_not.txt",
                  sample_dir=spectra_dir + "dark_sample2.txt",
                  ref_dir=spectra_dir + "dark_ref.txt")

Mirror2.load_data()
Mirror2.process_data()


x_new, interpolated_spectra_1, interpolated_spectra_2 = k_linearization(Mirror1.sub_raw,
                                                                      Mirror2.sub_raw,
                                                                      arguments=arguments)


dB_plot(data1=spectra2aline(interpolated_spectra_1),
        data2=spectra2aline(Mirror1.sub_raw),
        arguments=arguments)

dB_plot(data1=spectra2aline(interpolated_spectra_2),
        data2=spectra2aline(Mirror2.sub_raw),
        arguments=arguments)



sys.stdout.write('Procesing spectral shift')
z_space, shifted_spectra_1, shifted_spectra_2, shift_1, shift_2 = shift_spectra(interpolated_spectra_1,
                                                                      interpolated_spectra_2,
                                                                      N_pad=100,
                                                                      arguments=arguments)

sys.stdout.write('Computing dispersion')
Pdispersion = compute_dispersion(interpolated_spectra_1,
                                 interpolated_spectra_2,
                                 shift_1,
                                 shift_2,
                                 arguments=arguments)


compensated_spectra_1 = compensate_dispersion(interpolated_spectra_1,
                                             arguments.dispersion * Pdispersion)


compensated_spectra_2 = compensate_dispersion(interpolated_spectra_2,
                                             -arguments.dispersion * Pdispersion)

kernel = compute_PSF(spectra2aline(compensated_spectra_1))

dB_plot(data1=spectra2aline(compensated_spectra_1),
        data2=spectra2aline(Mirror1.sub_raw),
        arguments=arguments)

dB_plot(data1=spectra2aline(compensated_spectra_2),
        data2=spectra2aline(Mirror2.sub_raw),
        arguments=arguments)


calib_dict = {"klinear":     list(x_new),
              "dispersion":  list(Pdispersion),
              "dark_not":    load_data(spectra_dir + "dark_not.txt"),
              "dark_ref":    load_data(spectra_dir + "dark_ref.txt"),
              "dark_sample": load_data(spectra_dir + "dark_sample1.txt"),
              "psf_kernel" : list(kernel)
              }


sys.stdout.write('Writting json file...')
with open(calibration_dir + 'calibration_parameters.json', 'w') as outfile:
    json.dump(calib_dict, outfile)
















#---
