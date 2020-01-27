import os
import sys

p = os.path.abspath('.')
print(p)
if p not in sys.path:
    sys.path.append(p)

raw = p + "/data/raw/"
img = p + "/data/img/"
temp = p + "/data/temp/"
calib = p + "/data/calibration/"
csv = p + "/data/csv/"
png = p + "/data/png/"
