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


class Segment(object):


    def __init__(self, dim=100):
        self.dim = dim


    def load_data(self, dir):
        f = tables.open_file(dir)
        data = f.root.data
        data = np.array(data) - np.min(data) + 1
        print(np.max(data), np.min(data))
        data = np.log(data)
        data = data/np.max(data)*255

        self.data = data.astype(np.int)
        self.dim = np.shape(self.data)[0]
        self.update_slices()


    def set_data(self, data):
        self.data = data
        self.dim = np.shape(self.data)[0]
        self.update_slices()


    def update_slices(self):
        self.slice_XZ = self.data[0,:,:].T
        self.slice_YZ = self.data[:,0,:].T


    def YZ_onclick(self, event):


        self.YZ_coordinates.append((event.xdata, event.ydata))
        print( event.xdata, event.ydata )

        if len(self.YZ_coordinates) == 4:
            self.fig.canvas.mpl_disconnect(self.cid)
            plt.close()
        return


    def XZ_onclick(self, event):

        self.XZ_coordinates.append((event.xdata, event.ydata))
        print( event.xdata, event.ydata )

        if len(self.XZ_coordinates) == 4:
            self.fig.canvas.mpl_disconnect(self.cid)
            plt.close()
        return



    def plot_Bscan(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(self.data[0,:,:], cmap='gray')
        plt.show()


    def get_XZ_points(self, num=4):
        self.num = num
        self.XZ_coordinates = []

        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        ax.imshow(self.slice_XZ, cmap='gray')
        ax.set_title('Click on 4 point for bottom segmentation in Y-Z plane')
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.XZ_onclick)
        plt.show()

    def get_YZ_points(self, num=4):
        self.num = num
        self.YZ_coordinates = []
        self.YZ_coordinates.append( (0, self.XZ_coordinates[0]) )

        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        ax.imshow(self.slice_YZ, cmap='gray')
        ax.scatter([0], self.XZ_coordinates[0])
        ax.set_title('Click on 4 point for bottom segmentation in Y-Z plane')
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.YZ_onclick)
        plt.show()


    def make_XZ_fit(self):
        self.XZ_coordinates = np.array(self.XZ_coordinates)
        coef = np.polyfit(self.XZ_coordinates[:,0],
                          self.XZ_coordinates[:,1],
                          deg=self.num-1)
        fit = np.poly1d(coef)
        x = np.arange(self.dim)
        self.XZ_coordinates = fit(x)
        self.XZ_coordinates = np.clip(self.XZ_coordinates, a_max=511, a_min=1)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(self.slice_XZ, cmap='gray')
        ax.plot(x, self.XZ_coordinates)
        plt.show()


    def make_YZ_fit(self):
        self.YZ_coordinates = np.array(self.YZ_coordinates)
        coef = np.polyfit(self.YZ_coordinates[:,0],
                          self.YZ_coordinates[:,1],
                          deg=self.num-1)
        fit = np.poly1d(coef)
        x = np.arange(self.dim)
        self.YZ_coordinates = fit(x)
        self.YZ_coordinates = np.clip(self.YZ_coordinates, a_max=511, a_min=1)
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.imshow(self.slice_YZ, cmap='gray')
        ax.plot(x, self.YZ_coordinates)
        plt.show()


    def def_lim_mesh(self):

        XX = np.array([self.XZ_coordinates]*self.dim)
        YY = np.array([self.YZ_coordinates]*self.dim) - self.YZ_coordinates[0]
        t = np.linspace(0, self.dim, self.dim)
        T, _ = np.meshgrid(t,t)
        self.mesh = XX + YY.transpose()


    def apply_limit(self, lim='bottom'):
        print(np.shape(self.mesh))

        if lim == 'bottom':
            max = int( np.max(self.mesh) )
            print(max)
            for i in range(self.dim):
                for j in range(self.dim):
                    self.data[j,i,int(self.mesh[j,i]):] = 0
            self.data = self.data[:,:,0:max]

        if lim == 'top':
            min = int( np.min(self.mesh) )
            for i in range(self.dim):
                for j in range(self.dim):
                    self.data[j,i,:int(self.mesh[j,i])] = 0

            self.data = self.data[:,:,min:]

        with napari.gui_qt():
            viewer = napari.view_image(self.data)


    def bound_bottom(self):
        self.get_XZ_points()
        self.make_XZ_fit()
        self.get_YZ_points()
        self.make_YZ_fit()
        self.def_lim_mesh()
        self.apply_limit('bottom')
        self.update_slices()

    def bound_top(self):
        self.get_XZ_points()
        self.make_XZ_fit()
        self.get_YZ_points()
        self.make_YZ_fit()
        self.def_lim_mesh()
        self.apply_limit('top')
        self.update_slices()


arguments = Post_processing_parse_arguments()
dir1 = "data/Cscan/retina_LP01.h5"
dir2 = "data/Cscan/retina_LP11.h5"

sys.stdout.write('Creating object 1 from {0} \n'.format(dir1))
obj1 = Segment()
obj1.load_data(dir1)

sys.stdout.write('Creating object 2 from {0} \n'.format(dir2))
obj2 = Segment()
obj2.load_data(dir2)

obj3 = Segment()
obj3.set_data(obj1.data - obj2.data)
obj3.bound_bottom()
obj3.bound_top()

np.save('data/Cscan/segmented_image.npy', obj3.data)
