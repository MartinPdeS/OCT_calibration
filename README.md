# Py-OCT-Calibration

This project aims to produce an easy to use tool to calibrate any SD or SS-OCT. By calibrate I mean substracting background - k-linearize spectra - evaluate and compensate dispersion.

## Packages depedencies

In order to use the Py-OCT-Calibration Library, one must have installed the following packages:

```
    - Numpy
    - Scipy
    - json
    - matplotlib
    - sphynx (for developer only)
    - git (for developer only)

```

Using pip3 one can use the following commands:

```console
>>> pip3 install Numpy
>>> pip3 install Scipy
>>> pip3 install matplotlib
>>> pip3 install gitpython
>>> apt-get install python-sphinx (for Unix OS)
>>> sudo port install py27-sphinx (for Mac OS)
```

## Project architecture

The folder architecture is presented as :

```
    PyOCTCalibration/
            - data/                         (contain all data)
                - calibration/
                - img/
            - processing/                
                - calibration.py            (compute the k-linear., dispersion, spectrum shift, noise)
                - Aline.py                  (process one Aline)
                - Bscan.py                  (process one Bscan)
                - Cscan.py                  (process one Cscan)
            - toolbox/                      (contain tools to do all the processing)

            - Doc/                          (not yet added)

```


## Run example

### Calibration

In order to run a calibration example one can tape the following command on command prompt:

```console

>>> python3 processing/calibration.py --dispersion=1 --input-dir = ../ --output-file=test.json

```

Arguments for processing/calibration.py are:

* --dispersion : [1] for normal dispersion, [-1] for anormal
* --input-dir : directory of the input files for calibration
* --output-file : directory for the output .json file containing all the calibration parameters



### Aline

In order to process one example of Aline, one can tape the following command on command prompt:

```console

>>> python3 processing/Aline.py --dispersion=1 --input-dir = ../ --calibration=calib.json

```

Arguments for processing/Aline.py are:

* --dispersion : [1] for normal dispersion, [-1] for anormal
* --input-file : directory of the input Aline file
* --calibration : directory for the output .json file containing all the calibration parameters
* --output-file : directory for the processed Aline file

### Bscan

In order to process one example of Bscan, one can tape the following command on command prompt:

```console

>>> python3 processing/Aline.py --dispersion=1 --input-dir = ../ --calibration=calib.json --output-file=...

```

Arguments for processing/Aline.py are:

* --dispersion : [1] for normal dispersion, [-1] for anormal
* --input-file : directory of the input Aline file
* --calibration : directory for the output .json file containing all the calibration parameters
* --output-file : directory for the processed Bscan file



### Cscan

In order to process one example of Aline, one can tape the following command on command prompt:

```console

>>> python3 processing/Aline.py --dispersion=1 --input-dir = ../ --calibration=calib.json --output-file=...

```

Arguments for processing/Aline.py are:

* --dispersion : [1] for normal dispersion, [-1] for anormal
* --input-file : directory of the input Aline file
* --calibration : directory for the output .json file containing all the calibration parameters
* --output-file : directory for the processed Cscan file


Here is an example of output give by:

```console

>>> python3 process_Bscan.py -f=cible_6 -d=-1

```


## Pep8 coding convention

In order to keep a clean and consistent code, one can follow the convention as presented in the following link:

https://www.python.org/dev/peps/pep-0008/#documentation-strings
