import numpy as np
import matplotlib.pyplot as plt
import os


def convert_calib_files(dir):
    filename = "dark_not"
    dir0 = "data/calibration/feb_2020/LP01/{0}.data"
    dir1 = "data/calibration/feb_2020/LP01/{0}.npy"



    data = np.fromfile(dir0.format(filename),dtype="float32")
    np.save(dir1.format(filename), np.array(data))

    print(np.shape(data))
    plt.plot(data)
    plt.show()




#dir0 = "data/Bscan/example.data"
#dir1 = "data/Bscan/example.npy"

input_path = "data/Cscan/LP11"
file_list = os.listdir(input_path)

for n_i, input_file_name in enumerate(file_list):
    input_file = os.path.join(input_path, input_file_name)
    output_file = os.path.join(input_path, str(n_i) )
    data = np.fromfile(input_file, dtype=np.float32)
    np.save(output_file, np.array(data))

#data = np.fromfile(dir0,dtype="float32")
#np.save(dir1, data)
