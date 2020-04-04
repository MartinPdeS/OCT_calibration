


HOST=127.0.0.1
TEST_PATH=./
.PHONY = clean

build_project:
		python setup.py build_ext --inplace
		mv ./src/toolbox/*.html ./doc/cython

test: test_Calibration test_Bscan_gpu test_Cscan_cpu test_Cscan_gpu

test_calibration:
		python src/processing/calibration.py --dispersion=1 --input-dir=data/calibration/example/ --output-file=data/calibration/example/calib.json

#####Bscan test#####
test_Bscan_cpu:
		python src/processing/Cscan.py -d=1 -id=data/Bscan/example -c=data/calibration/example/calib.json -dim 1 3147 1024

test_Bscan_gpu:
		python src/processing/Cscan.py --silent -gpu -d=1 -id=data/Bscan/example -c=data/calibration/example/calib.json -dim 1 3147 1024

test_Bscan_cpu_compiled:
		python src/processing/Cscan.py --compile -d=1 -id=data/Bscan/example -c=data/calibration/example/calib.json -dim 1 3147 1024

test_Bscan_gpu_compiled:
		python src/processing/Cscan.py --silent --compile -gpu -d=1 -id=data/Bscan/example -c=data/calibration/example/calib.json -dim 1 3147 1024


#####Cscan test#####
test_Cscan_cpu_compiled:
		python src/processing/Cscan.py --silent --compiled --dispersion=1 --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 100 1024

test_Cscan_cpu:
		python src/processing/_Cscan.py --silent --dispersion=1 --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 100 1024

test_Cscan_gpu:
		python src/processing/_Cscan.py --silent --dispersion=1 -gpu --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 100 1024

test_Cscan_gpu_compiled:
		python src/processing/Cscan.py --silent --compiled --dispersion=1 -gpu --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 100 1024



test_Cscan_result:
		python ./src/processing/post_process.py -v -if="data/Cscan/example.h5"

cython_html:
		cython -a src/toolbox/main_processing_gpu.pyx


clean:
		rm -rf ./build/
		rm -rf ./src/toolbox/*.c
