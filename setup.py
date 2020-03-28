from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize

ext_modules=[
    Extension("test_fits",            ["src/toolbox/fits.pyx"]),
    Extension("test_filters",         ["src/toolbox/filters.pyx"]),
]

setup(
        name='PyOCTCalibration',
        version="1.1dev",
        license='Creative Commons Attribution-Noncommercial-Share Alike license',
        ext_modules = cythonize(ext_modules) #cythonize("src/toolbox/fits.pyx")
)
