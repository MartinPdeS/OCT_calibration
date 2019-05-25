

import argparse
import sys


def parse_arguments():

    parser = argparse.ArgumentParser()

    parser.add_argument('-f',
                        '--filename',
                        help='Input .Raw Bscan file',
                        dest='input_file',
                        type=str,
                        default='test.raw',
                        required=False)

    parser.add_argument('-s',
                        '--save-plots',
                        help='save plots',
                        dest='save_plots',
                        action='store_true',
                        required=False)

    parser.add_argument('-d',
                        '--dispersion',
                        help='Dispersion normal or anormal',
                        dest='dispersion',
                        type=str,
                        default='pos',
                        required=False)

    args = parser.parse_args()

    if args.dispersion == 'normal':
        args.dispersion = 1
    elif args.dispersion == 'anormal':
        args.dispersion = -1
    else:
        raise ValueError('\n \n Invalide disperions [-d] input. try [-d=normal] or [-d=anormal]\n \n')


    return args
