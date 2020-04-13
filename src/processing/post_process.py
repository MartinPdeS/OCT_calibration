'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
from functools import partial
import napari
from mpl_toolkits.mplot3d import Axes3D
import os, sys, tables
from matplotlib.ticker import LinearLocator
napari.gui_qt()

'''_____Add package_____'''
p = os.path.abspath('.')
if p not in sys.path:
    sys.path.append(p)


'''_____Project imports_____'''
from src.toolbox.parsing import Post_processing_parse_arguments
from src.toolbox.post_processing import Segment


arguments = Post_processing_parse_arguments()
dir1 = "data/Cscan/orange_LP01_noshift.h5"
dir2 = "data/Cscan/orange_LP11_noshift.h5"

dir3 = "data/Cscan/orange_LP01_shift.h5"
dir4 = "data/Cscan/orange_LP11_shift.h5"

dir5 = "data/Cscan/orange_LP01_fullshift.h5"
dir6 = "data/Cscan/orange_LP11_fullshift.h5"

sys.stdout.write('Creating object 1 from {0} \n'.format(dir1))
obj1 = Segment()
obj1.load_data(dir1)


obj2 = Segment()
obj2.load_data(dir2)

obj3 = Segment()
obj3.set_data(obj1.data - obj2.data)
#obj3.data = obj3.data.clip(min=0)


if arguments.segmentation:
    obj1.bound_bottom()
    obj1.bound_top()

if arguments.view:
    with napari.gui_qt():
        viewer = napari.view_image(obj3.data[:,:,2:-100])



#np.save('data/Cscan/segmented_image.npy', obj3.data)
