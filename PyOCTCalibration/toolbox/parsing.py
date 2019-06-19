
'''_____Standard imports_____'''
import argparse
import sys

'''_____Project imports_____'''
import toolbox.directories as directories


def Calibration_parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-if',
                        '--input-dir',
                        help='Input calibration files directory',
                        dest='input_dir',
                        type=str,
                        default='',
                        required=False)

    parser.add_argument('-of',
                        '--output-dir',
                        help='Output calibration files directory',
                        dest='output_dir',
                        type=str,
                        default='./',
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
                        help='Dispersion normal or anormal',
                        dest='dispersion',
                        type=str,
                        default='pos',
                        required=False)



    arguments = parser.parse_args()

    if arguments.dispersion == 'normal':
        arguments.dispersion = 1
    elif arguments.dispersion == 'anormal':
        arguments.dispersion = -1
    else:
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

    parser.add_argument('-c',
                        '--calibration_file',
                        help='Calibration json file.',
                        dest='calibration_file',
                        type=str,
                        default='.calibration/calibration_parameters.json',
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
                        help='Dispersion normal or anormal',
                        dest='dispersion',
                        type=str,
                        default='pos',
                        required=False)



    arguments = parser.parse_args()

    if arguments.dispersion == 'normal':
        arguments.dispersion = 1
    elif arguments.dispersion == 'anormal':
        arguments.dispersion = -1
    else:
        raise ValueError('\n \n Invalide disperions [-d] input. try [-d=normal] or [-d=anormal]\n \n')


    arguments.calibration_file = directories.calib + arguments.calibration_file


    return arguments
