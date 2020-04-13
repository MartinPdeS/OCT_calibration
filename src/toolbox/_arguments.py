from argparse import Namespace 
global Arguments 
Arguments = Namespace(calibration_file='./data/calibration/example/calib.json', compiled=False, dimension=(100, 100, 1024), dispersion=1, gpu=True, input_directory='data/Cscan/example', output_dimension=(100, 100, 512), output_file='Cscan_temp.h5', save=False, shift=0.0, silent=True)