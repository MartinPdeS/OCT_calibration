


HOST=127.0.0.1
TEST_PATH=./
.PHONY = clean

test: test_Calibration test_Bscan_gpu test_Cscan_cpu test_Cscan_gpu

test_Calibration:
		python src/processing/calibration.py -d=1 -id=./data/calibration/example/ --silent
		rm --force temp_calibration.json.json

#####Bscan test#####
test_Bscan_cpu:
		python src/processing/Bscan.py -d=1 -if=data/Bscan/example.npy -c=data/calibration/example/calib.json -dim 3147 1024

test_Bscan_gpu:
		python src/processing/Bscan.py --silent -gpu -d=1 -if=data/Bscan/example.npy -c=data/calibration/example/calib.json -dim 3147 1024

#####Cscan test#####
test_Cscan_cpu_compiled:
		python src/processing/Cscan.py --compiled --dispersion=1 --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 1024

test_Cscan_cpu:
		python src/processing/Cscan.py --dispersion=1 --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 1024

test_Cscan_gpu:
		python src/processing/Cscan.py --dispersion=1 -gpu --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 1024

test_Cscan_gpu_compiled:
		python src/processing/Cscan.py --compiled --dispersion=1 -gpu --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 1024

test_calibration:
		python src/processing/calibration.py --dispersion=1 --input-dir=data/calibration/example/ --output-file=data/calibration/example/calib.json

test_Cscan_result:
		python ./src/processing/post_process.py -v -if="data/Cscan/example.h5"

cython_html:
		cython -a src/toolbox/main_processing_gpu.pyx

clean:
		rm -rf *.c
		rm ".\src\processing\*.c"
		rm -rf ".\build\"

		clean:
		    @echo "clean project"
		    -$(RM)  *.c
		    @echo "clean completed"
