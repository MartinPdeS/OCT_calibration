

'''_____Standard imports_____'''
from scipy import signal
import numpy as np
import scipy.fftpack as fp



def butter_highpass(cutoff, fs, order=5):

    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order,
                         normal_cutoff,
                         btype='high',
                         analog=False)
    return b, a


def butter_lowpass(cutoff, fs, order=5):

    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = signal.butter(order,
                         normal_cutoff,
                         btype='low',
                         analog=False)
    return b, a


def butter_highpass_filter(data, cutoff, fs, order=5):

    b, a = butter_highpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


def butter_lowpass_filter(data, cutoff, fs, order=5):

    b, a = butter_lowpass(cutoff, fs, order=order)
    y = signal.filtfilt(b, a, data)
    return y


def image_high_pass(data, axis):

    data = np.array(data)
    for i in range(len(data)):
        data[i] = butter_highpass_filter(data[i],
                                           cutoff=0.1,
                                           fs=80000,
                                           order=1)



    return data


def denoise_Bscan(Bscan):

    F1 = fp.fft2((Bscan).astype(float))

    F2 = fp.fftshift(F1)

    F2[500:530,:] = 0

    (w, h) = Bscan.shape

    half_w, half_h = int(w/2), int(h/2)

    F2[0 :1024, half_h -1 : half_h + 1] = 0

    Bscan = np.abs(fp.ifft2(fp.ifftshift(F2)).real)

    return Bscan

def compressor(data, factor=3, threshold=None):

    data = np.array(data)

    max = np.max(data)
    min = np.min(data)
    if threshold is None:
        threshold = (max - min) / 3

    tmp = []

    for i, array in enumerate(data):
        if array < threshold:
            array /= factor

        tmp.append(array)

    return tmp




"""
def CV_denoise(img):

    img =  cv2.fastNlMeansDenoising(src=image,
                                   dst=None,
                                   h=0,
                                   templateWindowSize=7,
                                   searchWindowSize=21)

"""

# -
