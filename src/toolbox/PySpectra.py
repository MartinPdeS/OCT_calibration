
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt

'''_____Project imports_____'''
from src.toolbox.maths import unwrap_phase
from src.toolbox.loadings import load_data
from src.toolbox.filters import butter_highpass_filter
from src.toolbox.plottings import plots_signals


class Spectra(object):

    def __init__(self, data_dir, background_dir = None, ref_dir = None, sample_dir = None):

        self.data_dir = data_dir

        self.background_dir = background_dir

        self.ref_dir = ref_dir

        self.sample_dir = sample_dir


    def load_data(self):
        """ This method serve to load the data, i.e, mirror, darf_ref, dark_not,
        dark_sample.

        """

        self.raw = []

        self.raw = np.load(self.data_dir)


    def get_phase(self):
        """ This method compute the phase of the processed spectra.

        """
        self.phase = unwrap_phase(self.sub_raw)

        self.phase -= self.phase[0]


    def process_data(self, plot=True):
        """ This method compute the processing of data, i.e,
        background removal + high pass filter.

        """

        self.sub_raw = self.raw


        if self.background_dir:
            self.background = load_data(self.background_dir)
            self.sub_raw += self.background

        if self.sample_dir:
            self.sample = load_data(self.sample_dir)
            self.sub_raw -= self.sample

        if self.ref_dir:
            self.ref = load_data(self.ref_dir)
            self.sub_raw -= self.ref

        self.sub_raw = butter_highpass_filter(self.sub_raw,
                                              cutoff=280,
                                              fs=40000,
                                              order=4)


        if plot:

            plots_signals(self.raw,
                          self.sub_raw,
                          self.ref,
                          self.sample,
                          self.background)






# 0
