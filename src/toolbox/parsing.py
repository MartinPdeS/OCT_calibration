
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
                        required=False)

    parser.add_argument('-of',
                        '--output-file',
                        help='Output calibration files directory [JSON]',
                        dest='output_file',
                        default=None,
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
                        required=False)



    arguments = parser.parse_args()

    if arguments.dispersion not in [-1,1]:
        raise ValueError('\n \n Invalide disperions [-d] input. try [-d=normal] or [-d=anormal]\n \n')

    if arguments.output_file:
        arguments.output_file = os.path.join(arguments.output_file + ".json")


    return arguments


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
                        '--calibration_file',
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
                        default='test.raw',
                        required=False)

    parser.add_argument('-m',
                        '--mean',
                        help='Number of Bscan',
                        dest='mean_number',
                        type=int,
                        default=1,
                        required=False)

    parser.add_argument('-c',
                        '--calibration_file',
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



    arguments = parser.parse_args()

    if arguments.dispersion not in [-1,1]:
        raise ValueError('\n \n Invalide disperions [-d] input. try [-d=normal] or [-d=anormal]\n \n')



    return arguments



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
                        help='Output .csv Cscan file',
                        dest='output_file',
                        type=str,
                        default='output.csv',
                        required=False)

    parser.add_argument('-c',
                        '--calibration_file',
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



    arguments = parser.parse_args()

    if arguments.dispersion not in [-1,1]:
        raise ValueError('\n \n Invalide disperions [-d] input. try [-d=normal] or [-d=anormal]\n \n')



    return arguments








# --
