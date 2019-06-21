
'''_____Standard imports_____'''
import os
import sys
import numpy as np
import json
import scipy.fftpack as fp
import matplotlib.pyplot as plt


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)


'''_____Project imports_____'''
from toolbox.parsing import Bscan_parse_arguments
from toolbox.loadings import load_Bscan_spectra, load_calibration
from toolbox.plottings import Bscan_plots
import toolbox.directories as directories
from toolbox.spectra_processing import process_Bscan, denoise_Bscan



arguments = Bscan_parse_arguments()

dimension = (1, 1049,1024)

Bscan_spectra = load_Bscan_spectra(arguments.input_file, dimension = dimension)


calibration = load_calibration(dir =  arguments.calibration_file)

Bscan = []

if len(dimension) >= 3:

    for iteration in range(dimension[0]):

        print( "########## iteration [{0}/{1}]".format( iteration, dimension[0] ) )

        tmp = process_Bscan(Bscan_spectra[iteration], calibration, shift=0, arguments=arguments)

        Bscan.append( denoise_Bscan(tmp) )

Bscan_output = np.mean(Bscan, axis=0)
import cv2

print(np.shape(Bscan_output))
from PIL import Image
import matplotlib
import matplotlib.colors as colors
matplotlib.image.imsave('name.png', np.log(Bscan_output))
img = cv2.imread('name.png')

img =  cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21)

img=-np.array(img).T[0]

plt.imshow(img, cmap="gray",vmin=0, vmax=255)
plt.show()


#Bscan_plots(img, arguments=arguments)





#-
