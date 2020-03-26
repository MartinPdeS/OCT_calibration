HOST=127.0.0.1
TEST_PATH=./


test: test_Calibration test_Bscan test_Cscan_cpu test_Cscan_gpu

test_Calibration:
		python src/processing/calibration.py -d=1 -id=./data/calibration/example/ --silent
		rm --force temp_calibration.json.json

test_Bscan_cpu:
		python src/processing/Bscan.py -d=1 -if=data/Bscan/example.npy -c=data/calibration/example/calib.json --silent

test_Bscan_gpu:
		python src/processing/Bscan.py -gpu -d=1 -if=data/Bscan/example.npy -c=data/calibration/example/calib.json --silent

test_Cscan_cpu:
		python src/processing/Cscan.py --dispersion=1 --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 100 1024


test_Cscan_gpu:
		python src/processing/Cscan.py --dispersion=1 --input-dir=data/Cscan/example --calibration=./data/calibration/example/calib.json -dim 100 100 1024
