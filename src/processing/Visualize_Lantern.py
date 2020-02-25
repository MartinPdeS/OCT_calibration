
'''_____Standard imports_____'''
import numpy as np
import pandas as pd


'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)



'''_____Project imports_____'''
from src.toolbox.parsing import Bscan_parse_arguments
from src.toolbox.loadings import load_Bscan_spectra, load_calibration
from src.toolbox.plottings import Lantern_vizualiser
from src.toolbox.spectra_processing import process_Bscan, denoise_Bscan
import src.toolbox.directories as directories



arguments = Bscan_parse_arguments()

dir_LP01 = directories.csv + "Cscan_LP01.csv"
dir_LP11 = directories.csv + "Cscan_LP11.csv"

dir_LP01 = directories.csv + "Cscan_LP01.csv"
dir_LP11 = directories.csv + "Cscan_LP11.csv"


DataFrame_LP01 = pd.read_pickle(dir_LP01)
DataFrame_LP11 = pd.read_pickle(dir_LP11)

data_LP01 = DataFrame_LP01.to_numpy().reshape(20,1049,508)
data_LP11 = DataFrame_LP11.to_numpy().reshape(20,1049,508)

I_01 = data_LP01
I_11 = data_LP11

I_norm = I_01 + I_11

bra  = I_11 / I_norm

Brad_ratio = I_01 / I_11

A = Lantern_vizualiser(fig1=[0,1,2], Bscan_LP01=Brad_ratio, Bscan_LP11=data_LP11, arguments=arguments)

A.Bscan_lanterne_plots()






#-
