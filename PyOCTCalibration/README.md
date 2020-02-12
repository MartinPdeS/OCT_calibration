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
    OCT/
        - dispersion/                   (contain the compiled code)
            - .temporary_data/          (contain temporary json data from geometry and solver)
            - calibration/              (this folder is to contain .png image for uploading index profil)
            - results/                  (contain python classes and functions)
            - toolbox/                  (contain files to actually run geometry, solver, and data collector)
            - src/                      (contain Unittest for gitlab continous integration)
            - Examples/                 (contain python code to run simulation)

        - Doc/                          (contain documentation)

```


## Run example

In order to run example one can tape the following command on command prompt:

```console

>>> python3 calibration.py --dispersion=normal
>>> python process_Bscan --dispersion=normal --input-file=example

```

Arguments are:

Markup : * Bullet --dispersion : shows debug printout
         * Bullet --input-file : print computed propagation modes



Here is an example of output give by:

```console

>>> python3 process_Bscan.py -f=cible_6 -d=anormal

```

![Alt text](results/example.png?raw=true "Title")

## Pep8 coding convention

In order to keep a clean and consistent code, one can follow the convention as presented in the following link:

https://www.python.org/dev/peps/pep-0008/#documentation-strings
