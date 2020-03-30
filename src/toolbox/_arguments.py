from argparse import Namespace 
global Arguments 
Arguments = Namespace(calibration_file='./data/calibration/example/calib.json', dimension=[100, 100, 1024], dispersion=1, gpu=True, input_directory='data/Cscan/example', output_file='Cscan_temp.h5', shift=False, silent=False)