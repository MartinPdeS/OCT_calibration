
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
import copy
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

'''_____Project imports_____'''
from toolbox.maths import unwrap_phase, apodization
from toolbox.spectra_processing import shift_spectra
from toolbox.loadings import load_data
from toolbox.filters import butter_lowpass_filter, butter_highpass_filter


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

        self.phase = unwrap_phase(self.raw)
        self.phase[0] = 0


    def plot_phase(self, plot=False):

        if plot:

            fig = plt.figure()
            ax = fig.add_subplot(111)
            ax.plot(self.phase)
            ax.set_ylabel('Phase [rad]')
            ax.set_xlabel('Points space [U.A]')
            plt.grid()
            plt.waitforbuttonpress()
            plt.close()


    def process_data(self):
        self.sub_background()
        self.sub_sample()
        self.sub_ref()
        self.raw = apodization(self.raw)
        self.raw = butter_highpass_filter(self.raw,
                                          cutoff=2000,
                                          fs=80000,
                                          order=4)

        #self.raw = butter_lowpass_filter(self.raw,
        #                                 cutoff=3000,
        #                                 fs=30000,
        #                                 order=2)
        self.get_phase()


    def sub_background(self):

        background = load_data(self.background_dir)

        self.raw = self.raw + background


    def sub_sample(self):

        sample = load_data(self.sample_dir)

        self.raw = self.raw - sample


    def sub_ref(self):

        ref = load_data(self.ref_dir)

        self.raw = self.raw - ref
