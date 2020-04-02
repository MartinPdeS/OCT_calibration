from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import numpy, scipy

ext_modules=[
    Extension("cython_fits",                     ["src/toolbox/fits.pyx"]),
    Extension("cython_filters",                  ["src/toolbox/filters.pyx"]),
    Extension("cython_maths",                    ["src/toolbox/maths.pyx"]),
    Extension("cython_loadings",                 ["src/toolbox/loadings.pyx"]),
    Extension("cython_main_processing_cpu",      ["src/toolbox/main_processing_cpu.pyx"]),
    Extension("cython_main_processing_gpu",      ["src/toolbox/main_processing_gpu.pyx"]),
    Extension("cython_plottings",                ["src/toolbox/plottings.pyx"]),
    Extension("cython_calibration_processing",   ["src/toolbox/calibration_processing.pyx"]),
    Extension("cython_PySpectra",                ["src/toolbox/PySpectra.pyx"]),
]

setup(
        name='PyOCTCalibration',
        version="1.1dev",
        license='Creative Commons Attribution-Noncommercial-Share Alike license',
        ext_package='src/toolbox/',
        ext_modules = cythonize(ext_modules), #cythonize("src/toolbox/fits.pyx"),
        include_dirs=[numpy.get_include(), scipy.get_include()],
)
