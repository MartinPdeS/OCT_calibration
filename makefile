


HOST=127.0.0.1
TEST_PATH=./
.PHONY = clean

build_project:
		python setup.py build_ext --inplace
		mv ./src/toolbox/*.html ./doc/cython

build_doc:
		$(MAKE) -C docs/documentation clean
		$(MAKE) -C docs/documentation html

test: test_Calibration test_Bscan_gpu test_Cscan_cpu test_Cscan_gpu


#####################_____Calibration test______#####################
test_calibration:
		python src/processing/calibration.py  --dispersion=1 --input-dir=data/calibration/example/ --output-file=temp_calibration.json -dim 1 1 1024
		rm temp_calibration.json

#####################_____Aline test______#####################
test_Aline_gpu:
		python src/processing/Cscan.py --silent --dispersion=-1 -gpu --input-dir=data/Aline/example/ --calibration=./data/calibration/feb_2020/LP01/calib.json  -dim 1 1 1024

test_Aline_cpu:
		python src/processing/Cscan.py --silent --dispersion=-1 --input-dir=data/Aline/example/ --calibration=./data/calibration/feb_2020/LP01/calib.json  -dim 1 1 1024


#####################_____Bscan test______#####################
test_Bscan_cpu:
		python src/processing/Cscan.py -d=1 -id=data/Bscan/example -c=data/calibration/example/calib.json -dim 1 3147 1024

test_Bscan_gpu:
		python src/processing/Cscan.py --silent -gpu -d=1 -id=data/Bscan/example -c=data/calibration/example/calib.json -dim 1 3147 1024


#####################_____Cscan test______#####################
test_Cscan_cpu:
		python src/processing/Cscan.py --silent --dispersion=1 --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 100 1024

test_Cscan_gpu:
		python src/processing/Cscan.py --silent --dispersion=1 -gpu --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 100 1024



test_Cscan_result:
		python ./src/processing/post_process.py -v -if="data/Cscan/example.h5"

cython_html:
		cython -a src/toolbox/main_processing_gpu.pyx


profiling:
		python -m cProfile -o ./doc/profiling/Cscan_gpu.prof src/processing/Cscan.py --silent --dispersion=1 -gpu --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 100 1024
		runsnake ./doc/profiling/Cscan_gpu.prof

clean:
		rm -rf ./build/
		rm -rf ./src/toolbox/*.c
