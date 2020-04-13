'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
import os, sys, re


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)


'''_____Project imports_____'''
from src.toolbox.parsing import Pre_processing_parse_arguments


def convert_calib_files(dir):
    filename = "dark_not"
    dir0 = "data/calibration/feb_2020/LP01/{0}.data"
    dir1 = "data/calibration/feb_2020/LP01/{0}.npy"



    data = np.fromfile(dir0.format(filename),dtype="float32")
    np.save(dir1.format(filename), np.array(data))

    print(np.shape(data))
    plt.plot(data)
    plt.show()


def pre_process_filename(input_path):
    file_list = os.listdir(input_path)

    for n_i, input_filename in enumerate(file_list):
        number_string = re.findall(r'\d+', input_filename)
        zero_filled_number = number_string[0].zfill(4)

        output_filename = re.sub(r'\d+', zero_filled_number, input_filename, 1)

        print(input_filename, output_filename)
        os.rename(input_path + input_filename, input_path + output_filename)



def pre_process_data(input_path, output_path, dimension=[1049,1024]):
    file_list = os.listdir(input_path)

    for n_i, input_file_name in enumerate(file_list):
        input_file = os.path.join(input_path, input_file_name)
        sys.stdout.write("Pre processing file {2} ... [{0}/{1}] \n".format(n_i, len(file_list), input_file))
        output_file = os.path.join(output_path, '{:03d}'.format(n_i) )
        data = np.fromfile(input_file, dtype=np.float32)
        data = data.reshape(dimension)
        data = data[25:,:]

        np.save(output_file+'.npy', np.array(data))


if __name__ == "__main__":

    arguments = Pre_processing_parse_arguments()


    pre_process_filename(arguments.input_dir)
    pre_process_data(input_path=arguments.input_dir,
                     output_path=arguments.output_dir,
                     dimension = np.array(arguments.dimension).astype(int))
