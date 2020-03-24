HOST=127.0.0.1
TEST_PATH=./



test_aline:
		python src/processing/calibration.py -d=1 -id=./data/calibration/example/
		rm --force temp_calibration.json.json

test_bscan:
		python src/processing/Bscan.py -d=1 -if=data/Bscan/example.npy -c=data/calibration/example/calib.json
