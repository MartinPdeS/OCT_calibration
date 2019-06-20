
'''_____Standard imports_____'''
import argparse
import sys

'''_____Project imports_____'''
import toolbox.directories as directories


def Calibration_parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-id',
                        '--input-file',
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


    arguments.output_file = directories.calib + "calibration_parameters_" + arguments.input_dir + ".json"

    arguments.input_dir = directories.calib + "spectra/" + arguments.input_dir + "/"

    print(arguments.output_file)



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
    if ".raw" in arguments.input_file:
        arguments.input_file = directories.raw + arguments.input_file
    if ".img" in arguments.input_file:
        arguments.input_file = directories.img + arguments.input_file


    return arguments



def Cscan_parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-if',
                        '--input-file',
                        help='Input .Raw Cscan file',
                        dest='input_file',
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
    arguments.output_file = directories.csv + arguments.output_file


    if ".raw" in arguments.input_file:
        arguments.input_file = directories.raw + arguments.input_file
    if ".img" in arguments.input_file:
        arguments.input_file = directories.img + arguments.input_file


    return arguments








# --
