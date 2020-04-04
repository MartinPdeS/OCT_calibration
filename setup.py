from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
from Cython.Build import cythonize
import Cython.Compiler.Options
Cython.Compiler.Options.annotate = True
import numpy

ext_modules=[
    Extension("fits",                     ["src/toolbox/fits.pyx"]),
    Extension("filters",                  ["src/toolbox/filters.pyx"]),
    Extension("maths",                    ["src/toolbox/maths.pyx"]),
    Extension("main_processing_cpu",      ["src/toolbox/main_processing_cpu.pyx"]),
    Extension("main_processing_gpu",      ["src/toolbox/main_processing_gpu.pyx"]),
    Extension("plottings",                ["src/toolbox/plottings.pyx"]),
    Extension("calibration_processing",   ["src/toolbox/calibration_processing.pyx"]),
    Extension("PySpectra",                ["src/toolbox/PySpectra.pyx"]),
]

setup(
        name='PyOCTCalibration',
        version="1.1dev",
        license='Creative Commons Attribution-Noncommercial-Share Alike license',
        ext_package='src/toolbox/cython/',
        ext_modules = cythonize(ext_modules), #cythonize("src/toolbox/fits.pyx"),
        include_dirs=[numpy.get_include()],
)
