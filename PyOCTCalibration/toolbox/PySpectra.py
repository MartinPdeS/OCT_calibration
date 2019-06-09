
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
import copy
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

'''_____Project imports_____'''
from toolbox.maths import unwrap_phase, apodization, spectra2aline
from toolbox.spectra_processing import shift_spectra
from toolbox.loadings import load_data
from toolbox.filters import butter_lowpass_filter, butter_highpass_filter, compressor
from toolbox.plottings import plots_signals


class Spectra(object):

    def __init__(self, data_dir, background_dir = None, ref_dir = None, sample_dir = None):

        self.data_dir = data_dir
        self.background_dir = background_dir
        self.ref_dir = ref_dir
        self.sample_dir = sample_dir


    def load_data(self):

        self.raw = []
        file = open(self.data_dir,'r')
        for line in file:
            self.raw.append(float(line))

        self.raw = np.array(self.raw)


    def get_phase(self):

        self.phase = unwrap_phase(self.sub_raw)
        self.phase -= self.phase[0] + 1


    def process_data(self, plot=True):

        self.background = load_data(self.background_dir)
        self.sample = load_data(self.sample_dir)
        self.ref = load_data(self.ref_dir)
        self.sub_raw = self.raw + self.background - self.ref - self.sample
        #self.sub_raw = apodization(self.sub_raw)




        if 1:
            self.sub_raw = butter_highpass_filter(self.sub_raw,
                                                  cutoff=280,
                                                  fs=40000,
                                                  order=4)


        if 0:
            self.sub_raw = butter_lowpass_filter(self.sub_raw,
                                                 cutoff=5000,
                                                 fs=40000,
                                                 order=2)

        if plot:
            plots_signals(self.raw,
                          self.sub_raw,
                          self.ref,
                          self.sample,
                          self.background)
