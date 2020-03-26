
'''_____Standard imports_____'''
import argparse
import sys, os


'''_____Project imports_____'''
import src.toolbox.directories as directories


def Calibration_parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-id',
                        '--input-dir',
                        help='Input calibration files directory [DIRECTORY]',
                        dest='input_dir',
                        type=str,
                        default= directories.calib + "spectra/" ,
                        required=True)

    parser.add_argument('-of',
                        '--output-file',
                        help='Output calibration files directory [JSON]',
                        dest='output_file',
                        default="temp_calibration.json",
                        required=False)

    parser.add_argument('-i',
                        '--interactive_shift-plots',
                        help='interactive_shift',
                        dest='interactive',
                        default = False,
                        action='store_true',
                        required=False)

    parser.add_argument('-d',
                        '--dispersion',
                        help='Dispersion normal[1] or anormal[-1]',
                        dest='dispersion',
                        type=float,
                        default=1,
                        required=True)

    parser.add_argument('--silent',
                        help='No verbose mode',
                        dest='silent',
                        action="store_true")



    arguments = parser.parse_args()

    if arguments.dispersion not in [-1,1]:
        raise ValueError('\n \n Invalide disperions [-d] input. try [-d=normal] or [-d=anormal]\n \n')

    if arguments.output_file:
        arguments.output_file = os.path.join(arguments.output_file)


    with open('src/toolbox/_arguments.py', 'w') as f:
        f.write('from argparse import Namespace \nglobal Arguments \nArguments = {0}'.format(arguments))



def Aline_parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-if',
                        '--input-file',
                        help='Input .txt Bscan file',
                        dest='input_file',
                        type=str,
                        default='test.txt',
                        required=False)

    parser.add_argument('-c',
                        '--calibration-file',
                        help='Calibration json file.',
                        dest='calibration_file',
                        type=str,
                        default='.calibration/calibration_parameters.json',
                        required=False)

    parser.add_argument('-d',
                        '--dispersion',
                        help='Dispersion normal[1] or anormal[-1]',
                        dest='dispersion',
                        type=float,
                        default=1,
                        required=False)

    parser.add_argument('--silent',
                        help='No verbose mode',
                        dest='silent',
                        action="store_true")

    arguments = parser.parse_args()

    if arguments.dispersion not in [-1,1]:
        raise ValueError('\n \n Invalide disperions [-d] input. try [-d=normal] or [-d=anormal]\n \n')


    return arguments


def Bscan_parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-if',
                        '--input-file',
                        help='Input .Raw Bscan file',
                        dest='input_file',
                        type=str,
                        required=True)

    parser.add_argument('-m',
                        '--mean',
                        help='Number of Bscan',
                        dest='mean_number',
                        type=int,
                        default=1,
                        required=False)

    parser.add_argument('-gpu',
                        '--gpu-accelerated',
                        help='CUDA coding for accelerating, NVIDIA or NOT',
                        dest='gpu',
                        action="store_true")

    parser.add_argument('-c',
                        '--calibration-file',
                        help='Calibration json file.',
                        dest='calibration_file',
                        type=str,
                        required=True)

    parser.add_argument('-s',
                        '--shift',
                        help="shifting spectum",
                        dest="shift",
                        required=False,
                        action="store_true")

    parser.add_argument('-d',
                        '--dispersion',
                        help='Dispersion normal[1] or anormal[-1]',
                        dest='dispersion',
                        type=int,
                        default=1,
                        required=True)

    parser.add_argument('--silent',
                        help='No verbose mode',
                        dest='silent',
                        action="store_true")

    arguments = parser.parse_args()

    if arguments.dispersion not in [-1,1]:
        raise ValueError('\n \n Invalide disperions [-d] input. try [-d=normal] or [-d=anormal]\n \n')

    with open('src/toolbox/_arguments.py', 'w') as f:
        f.write('from argparse import Namespace \nglobal Arguments \nArguments = {0}'.format(arguments))



def Cscan_parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-id',
                        '--input-directory',
                        help='Input .npy Cscan file',
                        dest='input_directory',
                        type=str,
                        default='test.raw',
                        required=False)

    parser.add_argument('-of',
                        '--output-file',
                        help='Output .h5 Cscan file',
                        dest='output_file',
                        type=str,
                        default='Cscan_temp.h5',
                        required=False)

    parser.add_argument('-c',
                        '--calibration-file',
                        help='Calibration json file.',
                        dest='calibration_file',
                        type=str,
                        required=True)


    parser.add_argument('-d',
                        '--dispersion',
                        help='Dispersion normal[1] or anormal[-1]',
                        dest='dispersion',
                        type=int,
                        default=1,
                        required=True)

    parser.add_argument('-gpu',
                        '--gpu-accelerated',
                        help='CUDA coding for accelerating, NVIDIA or NOT',
                        dest='gpu',
                        action="store_true")

    parser.add_argument('-dim',
                        '--dimension',
                        help="dimension",
                        dest="dimension",
                        required=True,
                        nargs=3)

    parser.add_argument('-s',
                        '--shift',
                        help="shifting spectum",
                        dest="shift",
                        required=False,
                        action="store_true")


    parser.add_argument('--silent',
                        help='No verbose mode',
                        dest='silent',
                        action="store_true")



    arguments = parser.parse_args()

    arguments.dimension = list(map(int,arguments.dimension))

    if arguments.dispersion not in [-1,1]:
        raise ValueError('\n \n Invalide disperions [-d] input. try [-d=normal] or [-d=anormal]\n \n')


    with open('src/toolbox/_arguments.py', 'w') as f:
        f.write('from argparse import Namespace \nglobal Arguments \nArguments = {0}'.format(arguments))

    return arguments


def Post_processing_parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-if',
                        '--input-file',
                        help='Input Cscan file [FILE]',
                        dest='input_file',
                        type=str,
                        default= None ,
                        required=False)

    parser.add_argument('-seg',
                        '--segmentation',
                        help='Segmentate Input Cscan file ',
                        dest='segmentation',
                        action="store_true",
                        required=False)

    parser.add_argument('-v',
                        '--view',
                        help='3D viewer if input Cscan file ',
                        dest='view',
                        action='store_true',
                        required=False)


    return parser.parse_args()



def Pre_processing_parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-id',
                        '--input-directory',
                        help='Input Cscan directory [DIRECTORY]',
                        dest='input_dir',
                        type=str,
                        default= None ,
                        required=True)

    parser.add_argument('-od',
                        '--output-directory',
                        help='Output Cscan directory [DIRECTORY]',
                        dest='output_dir',
                        type=str,
                        default= None,
                        required=True)

    parser.add_argument('-dim',
                        '--dimension',
                        help='Bscan dimension Z-axis last [2-values LIST]',
                        dest='dimension',
                        default= None,
                        required=True,
                        nargs=2)


    return parser.parse_args()




def coords(s):
    try:
        x, y, z = map(int, s.split(','))
        return x, y, z
    except:
        raise argparse.ArgumentTypeError("Dimension must be x,y,z")





# --
