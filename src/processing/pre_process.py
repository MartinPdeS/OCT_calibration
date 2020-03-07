import numpy as np
import matplotlib.pyplot as plt
import os, sys


def convert_calib_files(dir):
    filename = "dark_not"
    dir0 = "data/calibration/feb_2020/LP01/{0}.data"
    dir1 = "data/calibration/feb_2020/LP01/{0}.npy"



    data = np.fromfile(dir0.format(filename),dtype="float32")
    np.save(dir1.format(filename), np.array(data))

    print(np.shape(data))
    plt.plot(data)
    plt.show()


def pre_process_data(input_path, dimension=[1049,1024]):
    file_list = os.listdir(input_path)

    for n_i, input_file_name in enumerate(file_list):

        sys.stdout.write("Pre processing ... [{0}/{1}] \n".format(n_i, len(file_list)))
        input_file = os.path.join(input_path, input_file_name)
        output_file = os.path.join(input_path, '{:03d}'.format(n_i) )
        data = np.fromfile(input_file, dtype=np.float32)#.reshape([537,1024])
        data = data.reshape([1024+25,1024])
        data = data[25:,:]
        np.save(output_file, np.array(data))


if __name__ == "__main__":
    pre_process_data("data/Cscan/retina/")
