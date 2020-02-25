import numpy as np
import matplotlib.pyplot as plt

def convert_calib_files():
    filename = "dark_not"
    dir0 = "data/calibration/feb_2020/LP01/{0}.data"
    dir1 = "data/calibration/feb_2020/LP01/{0}.npy"



    data = np.fromfile(dir0.format(filename),dtype="float32")
    np.save(dir1.format(filename), np.array(data))

    print(np.shape(data))
    plt.plot(data)
    plt.show()


dir0 = "data/Bscan/example.data"
dir1 = "data/Bscan/example.npy"

data = np.fromfile(dir0,dtype="float32")
np.save(dir1, data)
