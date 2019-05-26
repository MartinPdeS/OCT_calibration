
'''_____Standard imports_____'''
import numpy as np
import json
import sys


'''_____Project imports_____'''
from toolbox.PySpectra import Spectra
from toolbox.parsing import parse_arguments
from toolbox.spectra_processing import compute_dispersion, k_linearization, shift_spectra
from toolbox.loadings import load_data
from toolbox.plottings import dB_plot
from toolbox.maths import spectra2aline

args = parse_arguments()


calibration_dir = "/Volumes/USBEBE/data/calibration/"
calibration_dir = "calibration/spectra/20_mai/"


Mirror1 = Spectra(data_dir=calibration_dir + "mirror-.txt",
                  background_dir=calibration_dir + "dark_not.txt",
                  sample_dir=calibration_dir + "dark_sample.txt",
                  ref_dir=calibration_dir + "dark_ref.txt")

Mirror1.load_data()
Mirror1.process_data()
Mirror1.get_phase()
Mirror1.plot_phase()

Mirror2 = Spectra(data_dir=calibration_dir + "mirror+.txt",
                  background_dir=calibration_dir + "dark_not.txt",
                  sample_dir=calibration_dir + "dark_sample.txt",
                  ref_dir=calibration_dir + "dark_ref.txt")

Mirror2.load_data()
Mirror2.process_data()
Mirror2.get_phase()
Mirror2.plot_phase()

x_new, interpolated_spectra1, interpolated_spectra2 = k_linearization(Mirror1.raw,
                                                                      Mirror2.raw,
                                                                      args=args)

sys.stdout.write('Procesing spectral shift')
z_space, shifted_spectra1, shifted_spectra2, c1, c2 = shift_spectra(interpolated_spectra1,
                                                                    interpolated_spectra2,
                                                                    N_pad=10,
                                                                    args=args)

sys.stdout.write('Computing dispersion')
spectra1, spectra2, Pdispersion = compute_dispersion(shifted_spectra1,
                                                     shifted_spectra2,
                                                     c1,
                                                     c2,
                                                     sign_dispersion=args.dispersion,
                                                     args=args)


dB_plot(spectra2aline(spectra1), spectra2aline(Mirror1.raw))
dB_plot(spectra2aline(spectra2), spectra2aline(Mirror2.raw))


calib_dict = {"klinear":     list(x_new),
              "dispersion":  list(Pdispersion),
              "dark_not":    load_data(calibration_dir + "dark_not.txt"),
              "dark_ref":    load_data(calibration_dir + "dark_ref.txt"),
              "dark_sample": load_data(calibration_dir + "dark_sample.txt")
              }


sys.stdout.write('Writting json file...')
with open('calibration/calibration_parameters.json', 'w') as outfile:
    json.dump(calib_dict, outfile)
















#---
