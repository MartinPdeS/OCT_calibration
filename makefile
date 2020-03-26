HOST=127.0.0.1
TEST_PATH=./


test: test_calibration test_bscan

test_calibration:
		python src/processing/calibration.py -d=1 -id=./data/calibration/example/ --silent
		rm --force temp_calibration.json.json

test_bscan:
		python src/processing/Bscan.py -d=1 -if=data/Bscan/example.npy -c=data/calibration/example/calib.json --silent
