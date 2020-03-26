
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('qt4agg')
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
import matplotlib.gridspec as gridspec

'''_____Project imports_____'''
from src.toolbox.fits import gauss
import src.toolbox.directories as directories



def dB_plot(data1, data2=None):

    fig = plt.figure(figsize=(15, 6))

    if data2 is None:
        ax = fig.add_subplot(111)
        ref1 = np.min(data1)
        dB1 = 10 * np.log(data1/ref1)
        ax.plot(dB1)
        ax.grid()
        ax.set_ylabel('Magnitude [dB]')
        ax.set_xlabel('Wavenumber k [U.A]')


    else:
        ax0 = fig.add_subplot(121)
        ax1 = fig.add_subplot(122)

        ref1 = np.max(data1)
        ref2 = np.max(data2)

        dB1 = 10 * np.log(data1/ref1)
        dB2 = 10 * np.log(data2/ref2)

        ax0.plot(dB1)
        ax0.set_title('Processed Aline')
        ax0.grid()
        ax0.set_ylabel('Magnitude [dB]')
        ax0.set_xlabel('Wavenumber k [U.A]')


        ax1.plot(dB2)
        ax1.set_title('Raw Aline')
        ax1.grid()
        ax1.set_ylabel('Magnitude [dB]')
        ax1.set_xlabel('Wavenumber k [U.A]')
        ax1.set_ylim(ax0.get_ylim())

    plt.waitforbuttonpress()
    plt.close()


def interactive_shift(spectra1, param1, spectra2, param2):


    shift1_condition = False
    shift2_condition = False

    while shift1_condition is False:

        shifted_spectra_plots( spectra1,
                               param1,
                               spectra2,
                               param2 )

        shift1 = input("Shift mirror1? [>0:Left, 0:None, <0:Right]")
        shift1 = eval(shift1)

        if shift1 == 0:
            shift1_condition = True
        else:
            print(param1[2])
            param1[2] += shift1
        plt.close()


    while shift2_condition is False:

        shifted_spectra_plots( spectra1,
                               param1,
                               spectra2,
                               param2 )

        shift2 = input("Shift mirror2? [>0:Left, 0:None, <0:Right]")
        shift2 = eval(shift2)

        if shift2 == 0:
            shift2_condition = True
        else:
            param2[2] += shift2
        plt.close()

    return param1[2], param2[2]


def shifted_spectra_plots(spectra1, param1, spectra2, param2):

    plt.ion()
    fig = plt.figure(figsize=(15, 6))
    ax0 = fig.add_subplot(121)
    ax1 = fig.add_subplot(122)


    ax0.plot( spectra1, label='Shifted raw' )
    ax0.grid()
    ax0.set_title('Shifted raw spectra mirror 1')

    ax0.plot( gauss(*param1),'r-', label='gaussian fit' )
    ax0.grid()
    ax0.set_title('Fitted gaussian curve mirror 1')

    ax1.plot( spectra2, label='Shifted raw' )
    ax1.grid()
    ax1.set_title('Shifted raw spectra mirror 2')

    ax1.plot( gauss(*param2), 'r-', label='gaussian fit' )
    ax1.grid()
    ax1.set_title('Fitted gaussian curve mirror 2')

    print("click the image to exit")
    ax0.legend()
    ax0.grid()

    ax1.legend()
    ax1.grid()
    fig.canvas.draw()


def phase_dispersion_plot(exp_dispersion, fit_dispersion):

    fig = plt.figure(figsize=(15, 6))
    ax0 = fig.add_subplot(111)

    ax0.plot(fit_dispersion, label = 'fitted ')
    ax0.plot(exp_dispersion,'-',label = 'experimental')

    ax0.set_ylabel('Unwrapped phase [U.A]')
    ax0.set_title('System phase dispersion')
    plt.grid()
    plt.legend()

    print("click the image to exit")
    plt.waitforbuttonpress()
    plt.close()


def Bscan_plots(Bscan):

    Bscan = np.array(Bscan)
    dBscan = 10*np.log(Bscan)

    fig = plt.figure(figsize=(16,10))


    ax0 = fig.add_subplot(221)
    ax0.grid()
    ax0.set_ylabel('Aline depth Intensity [U.A]')
    ax0.set_xlabel('Wavenumber k [U.A]')
    ax0.set_title("Spectra")
    ax0.plot(Bscan[200])



    ax1 = fig.add_subplot(222)
    ax1.grid()
    ax1.set_ylabel('Aline depth Magnitude [dB]')
    ax1.set_xlabel('Wavenumber k [U.A]')
    ax1.set_title("Aline")
    ref = np.min(dBscan[200])
    ax1.plot(dBscan[200])


    data = dBscan.T
    ax2 = fig.add_subplot(223)
    l = ax2.imshow(data,
                   cmap = "gray",
                   vmin=None,
                   vmax=None)
    ax2.invert_yaxis()
    ax2.set_title("Processed Bscan")

    axVmin = plt.axes([0.6, 0.1, 0.3, 0.03])
    axVmax = plt.axes([0.6, 0.15, 0.3, 0.03])
    axsave = plt.axes([0.7, 0.25, 0.1, 0.075])

    Min, Max = np.min(data)*0.7, np.max(data)*1.2
    Nstep = (Max - Min)/100

    SVmin = Slider(axVmin, 'Vmin', Min, Max, valinit=Min, valstep=Nstep)
    SVmax = Slider(axVmax, 'Vmax', Min, Max, valinit=Max, valstep=Nstep)
    bsave = Button(axsave, 'Save Bscan')


    def update(val):
        Vmax = SVmax.val
        Vmin = SVmin.val
        l.set_clim(vmin=Vmin, vmax=Vmax)
        fig.canvas.draw_idle()

    def save(event):
        save_dir = directories.png + "image.png"
        extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir, bbox_inches=extent)


    bsave.on_clicked(save)
    SVmin.on_changed(update)
    SVmax.on_changed(update)

    plt.show()


def plots_signals(data, sub_data, ref, sample, dark):

    fig = plt.figure()
    ax0 = fig.add_subplot(111)
    ax0.plot(data, label='raw data')
    ax0.plot(sub_data, 'k', label='substracted raw data')
    ax0.plot(ref, 'r', label='reference noise')
    ax0.plot(sample, 'b', label='sample noise')
    ax0.plot(dark, 'g', label='background noise')

    plt.grid()
    plt.legend()
    print("click the image to exit")
    plt.waitforbuttonpress()
    plt.close()




def plot_klinearization(phase1, phase2, Plin, Pfit=None):

    plt.ion()
    fig = plt.figure(figsize=(8,10))
    ax = fig.add_subplot(111)

    ax.plot(phase1,'r', label='Mirror1')
    ax.plot(phase2,'b', label='Mirror2')
    ax.plot(Plin, 'k', label='Linear phase')
    if Pfit is not None:
        ax.plot(Pfit, 'g', label='Fitted linear phase')
    plt.grid()
    ax.set_ylabel('Phase [rad]')
    ax.set_xlabel('Points space [U.A]')
    plt.legend()
    print("click the image to exit")
    plt.waitforbuttonpress()
    plt.close()




class Lantern_Bscan_vizualiser(object):


    def __init__(self, fig1, Bscan_LP01, Bscan_LP11):
        self.fig1 = fig1
        self.Bscan_LP01 = Bscan_LP01
        self.Bscan_LP11 = Bscan_LP11


    def update_intensity(self, event):
        Vmax_LP11 = self.SVmax_LP11.val
        Vmin_LP11 = self.SVmin_LP11.val
        self.l_LP11.set_clim(vmin=Vmin_LP11, vmax=Vmax_LP11)
        Vmax_LP01 = self.SVmax_LP11.val
        Vmin_LP01 = self.SVmin_LP11.val
        self.l_LP01.set_clim(vmin=Vmin_LP01, vmax=Vmax_LP01)
        self.fig.canvas.draw_idle()


    def next(self, event):
        self.N_plot += 1
        self.l_LP01.set_data(self.dBscan_LP01[self.N_plot].T)
        self.l_LP11.set_data(self.dBscan_LP11[self.N_plot].T)
        self.fig.canvas.draw_idle()


    def previous(self, event):
        self.N_plot -= 1
        self.l_LP01.set_data(self.dBscan_LP01[self.N_plot].T)
        self.l_LP11.set_data(self.dBscan_LP11[self.N_plot].T)
        self.fig.canvas.draw_idle()


    def save_LP11(self, event):
        save_dir = "results/"
        extent = self.ax2.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir + "figure_" + 'LP11', bbox_inches=extent)


    def save_LP01(self, event):
        save_dir = "results/"
        extent = self.ax1.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir + "figure_" + 'LP01', bbox_inches=extent)


    def Bscan_lanterne_plots(self):

        self.Bscan_LP01 = np.array(self.Bscan_LP01)
        self.Bscan_LP11 = np.array(self.Bscan_LP11)

        self.dBscan_LP11 = 10*np.log(self.Bscan_LP11)
        self.dBscan_LP01 = 10*np.log(self.Bscan_LP01)

        self.fig = plt.figure(figsize=(16,10))

        self.N_plot = 0


        axVmin_intensity = plt.axes([0.6, 0.1, 0.3, 0.03])
        axVmax_intensity = plt.axes([0.6, 0.15, 0.3, 0.03])
        axsave_LP11 = plt.axes([0.7, 0.25, 0.1, 0.075])

        axsave_LP01 = plt.axes([0.7, 0.80, 0.1, 0.075])

        axnext = plt.axes([0.8, 0.5, 0.1, 0.075])
        axprevious = plt.axes([0.6, 0.5, 0.1, 0.075])

        Min_LP11, Max_LP11 = np.min(self.dBscan_LP11)*0.7, np.max(self.dBscan_LP11)*1.2
        Min_LP01, Max_LP01 = np.min(self.dBscan_LP01)*0.7, np.max(self.dBscan_LP01)*1.2

        Nstep_LP11 = (Max_LP11 - Min_LP11)/100
        Nstep_LP01 = (Max_LP01 - Min_LP01)/100

        self.SVmin_LP11 = Slider(axVmin_intensity, 'Vmin', Min_LP11, Max_LP11, valinit=Min_LP11, valstep=Nstep_LP11)
        self.SVmax_LP11 = Slider(axVmax_intensity, 'Vmax', Min_LP11, Max_LP11, valinit=Max_LP11, valstep=Nstep_LP11)
        bsave_LP11 = Button(axsave_LP11, 'Save Bscan')

        bsave_LP01 = Button(axsave_LP01, 'Save Bscan')

        self.Bnext = Button(axnext, 'Next')
        self.Bprevious = Button(axprevious, 'Previous')


        self.ax1 = self.fig.add_subplot(221)
        self.l_LP01 = self.ax1.imshow(self.dBscan_LP01.T,
                                cmap = "gray",
                                vmin=None,
                                vmax=None)
        self.ax1.invert_yaxis()

        self.ax1.set_title("Processed Bscan LP01")

        self.ax2 = self.fig.add_subplot(223)
        self.l_LP11 = self.ax2.imshow(self.dBscan_LP11.T,
                                   cmap = "gray",
                                   vmin=None,
                                   vmax=None)
        self.ax2.invert_yaxis()
        self.ax2.set_title("Processed Bscan LP11")




        bsave_LP11.on_clicked(self.save_LP11)
        self.SVmin_LP11.on_changed(self.update_intensity)
        self.SVmax_LP11.on_changed(self.update_intensity)

        bsave_LP01.on_clicked(self.save_LP01)
        #self.SVmin_LP01.on_changed(self.update_LP01)
        #self.SVmax_LP01.on_changed(self.update_LP01)

        self.Bnext.on_clicked(self.next)
        self.Bprevious.on_clicked(self.previous)

        plt.show()





class Lantern_Bscan_vizualiser(object):


    def __init__(self, fig1, Bscan_LP01, Bscan_LP11):
        self.fig1 = fig1
        self.Bscan_LP01 = Bscan_LP01
        self.Bscan_LP11 = Bscan_LP11


    def update_intensity(self, event):
        Vmax_LP11 = self.SVmax_LP11.val
        Vmin_LP11 = self.SVmin_LP11.val
        self.l_LP11.set_clim(vmin=Vmin_LP11, vmax=Vmax_LP11)
        Vmax_LP01 = self.SVmax_LP11.val
        Vmin_LP01 = self.SVmin_LP11.val
        self.l_LP01.set_clim(vmin=Vmin_LP01, vmax=Vmax_LP01)
        self.fig.canvas.draw_idle()


    def next(self, event):
        self.N_plot += 1
        self.l_LP01.set_data(self.dBscan_LP01[self.N_plot].T)
        self.l_LP11.set_data(self.dBscan_LP11[self.N_plot].T)
        self.fig.canvas.draw_idle()


    def previous(self, event):
        self.N_plot -= 1
        self.l_LP01.set_data(self.dBscan_LP01[self.N_plot].T)
        self.l_LP11.set_data(self.dBscan_LP11[self.N_plot].T)
        self.fig.canvas.draw_idle()


    def save_LP11(self, event):
        save_dir = "results/"
        extent = self.ax2.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir + "figure_" + 'LP11', bbox_inches=extent)


    def save_LP01(self, event):
        save_dir = "results/"
        extent = self.ax1.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir + "figure_" + 'LP01', bbox_inches=extent)


    def Bscan_lanterne_plots(self):

        self.Bscan_LP01 = np.array(self.Bscan_LP01)
        self.Bscan_LP11 = np.array(self.Bscan_LP11)

        self.dBscan_LP11 = 10*np.log(self.Bscan_LP11)
        self.dBscan_LP01 = 10*np.log(self.Bscan_LP01)

        self.fig = plt.figure(figsize=(16,10))

        self.N_plot = 0


        axVmin_intensity = plt.axes([0.6, 0.1, 0.3, 0.03])
        axVmax_intensity = plt.axes([0.6, 0.15, 0.3, 0.03])
        axsave_LP11 = plt.axes([0.7, 0.25, 0.1, 0.075])

        axsave_LP01 = plt.axes([0.7, 0.80, 0.1, 0.075])

        axnext = plt.axes([0.8, 0.5, 0.1, 0.075])
        axprevious = plt.axes([0.6, 0.5, 0.1, 0.075])

        Min_LP11, Max_LP11 = np.min(self.dBscan_LP11)*0.7, np.max(self.dBscan_LP11)*1.2
        Min_LP01, Max_LP01 = np.min(self.dBscan_LP01)*0.7, np.max(self.dBscan_LP01)*1.2

        Nstep_LP11 = (Max_LP11 - Min_LP11)/100
        Nstep_LP01 = (Max_LP01 - Min_LP01)/100

        self.SVmin_LP11 = Slider(axVmin_intensity, 'Vmin', Min_LP11, Max_LP11, valinit=Min_LP11, valstep=Nstep_LP11)
        self.SVmax_LP11 = Slider(axVmax_intensity, 'Vmax', Min_LP11, Max_LP11, valinit=Max_LP11, valstep=Nstep_LP11)
        bsave_LP11 = Button(axsave_LP11, 'Save Bscan')

        bsave_LP01 = Button(axsave_LP01, 'Save Bscan')

        self.Bnext = Button(axnext, 'Next')
        self.Bprevious = Button(axprevious, 'Previous')


        self.ax1 = self.fig.add_subplot(221)
        self.l_LP01 = self.ax1.imshow(self.dBscan_LP01.T,
                                cmap = "gray",
                                vmin=None,
                                vmax=None)
        self.ax1.invert_yaxis()

        self.ax1.set_title("Processed Bscan LP01")

        self.ax2 = self.fig.add_subplot(223)
        self.l_LP11 = self.ax2.imshow(self.dBscan_LP11.T,
                                   cmap = "gray",
                                   vmin=None,
                                   vmax=None)
        self.ax2.invert_yaxis()
        self.ax2.set_title("Processed Bscan LP11")




        bsave_LP11.on_clicked(self.save_LP11)
        self.SVmin_LP11.on_changed(self.update_intensity)
        self.SVmax_LP11.on_changed(self.update_intensity)

        bsave_LP01.on_clicked(self.save_LP01)
        #self.SVmin_LP01.on_changed(self.update_LP01)
        #self.SVmax_LP01.on_changed(self.update_LP01)

        self.Bnext.on_clicked(self.next)
        self.Bprevious.on_clicked(self.previous)

        plt.show()






class Lantern_Bscan_vizualiser(object):


    def __init__(self, fig1, Bscan_LP01, Bscan_LP11):
        self.fig1 = fig1
        self.Bscan_LP01 = Bscan_LP01
        self.Bscan_LP11 = Bscan_LP11


    def update_intensity(self, event):
        Vmax_LP11 = self.SVmax_LP11.val
        Vmin_LP11 = self.SVmin_LP11.val
        self.l_LP11.set_clim(vmin=Vmin_LP11, vmax=Vmax_LP11)
        Vmax_LP01 = self.SVmax_LP11.val
        Vmin_LP01 = self.SVmin_LP11.val
        self.l_LP01.set_clim(vmin=Vmin_LP01, vmax=Vmax_LP01)
        self.fig.canvas.draw_idle()


    def next(self, event):
        self.N_plot += 1
        self.l_LP01.set_data(self.dBscan_LP01[self.N_plot].T)
        self.l_LP11.set_data(self.dBscan_LP11[self.N_plot].T)
        self.fig.canvas.draw_idle()


    def previous(self, event):
        self.N_plot -= 1
        self.l_LP01.set_data(self.dBscan_LP01[self.N_plot].T)
        self.l_LP11.set_data(self.dBscan_LP11[self.N_plot].T)
        self.fig.canvas.draw_idle()


    def save_LP11(self, event):
        save_dir = "results/"
        extent = self.ax2.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir + "figure_" + 'LP11', bbox_inches=extent)


    def save_LP01(self, event):
        save_dir = "results/"
        extent = self.ax1.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir + "figure_" + 'LP01', bbox_inches=extent)


    def Bscan_lanterne_plots(self):

        self.Bscan_LP01 = np.array(self.Bscan_LP01)
        self.Bscan_LP11 = np.array(self.Bscan_LP11)

        self.dBscan_LP11 = 10*np.log(self.Bscan_LP11)
        self.dBscan_LP01 = 10*np.log(self.Bscan_LP01)

        self.fig = plt.figure(figsize=(16,10))

        self.N_plot = 0


        axVmin_intensity = plt.axes([0.6, 0.1, 0.3, 0.03])
        axVmax_intensity = plt.axes([0.6, 0.15, 0.3, 0.03])
        axsave_LP11 = plt.axes([0.7, 0.25, 0.1, 0.075])

        axsave_LP01 = plt.axes([0.7, 0.80, 0.1, 0.075])

        axnext = plt.axes([0.8, 0.5, 0.1, 0.075])
        axprevious = plt.axes([0.6, 0.5, 0.1, 0.075])

        Min_LP11, Max_LP11 = np.min(self.dBscan_LP11)*0.7, np.max(self.dBscan_LP11)*1.2
        Min_LP01, Max_LP01 = np.min(self.dBscan_LP01)*0.7, np.max(self.dBscan_LP01)*1.2

        Nstep_LP11 = (Max_LP11 - Min_LP11)/100
        Nstep_LP01 = (Max_LP01 - Min_LP01)/100

        self.SVmin_LP11 = Slider(axVmin_intensity, 'Vmin', Min_LP11, Max_LP11, valinit=Min_LP11, valstep=Nstep_LP11)
        self.SVmax_LP11 = Slider(axVmax_intensity, 'Vmax', Min_LP11, Max_LP11, valinit=Max_LP11, valstep=Nstep_LP11)
        bsave_LP11 = Button(axsave_LP11, 'Save Bscan')

        bsave_LP01 = Button(axsave_LP01, 'Save Bscan')

        self.Bnext = Button(axnext, 'Next')
        self.Bprevious = Button(axprevious, 'Previous')


        self.ax1 = self.fig.add_subplot(221)
        self.l_LP01 = self.ax1.imshow(self.dBscan_LP01.T,
                                cmap = "gray",
                                vmin=None,
                                vmax=None)
        self.ax1.invert_yaxis()

        self.ax1.set_title("Processed Bscan LP01")

        self.ax2 = self.fig.add_subplot(223)
        self.l_LP11 = self.ax2.imshow(self.dBscan_LP11.T,
                                   cmap = "gray",
                                   vmin=None,
                                   vmax=None)
        self.ax2.invert_yaxis()
        self.ax2.set_title("Processed Bscan LP11")




        bsave_LP11.on_clicked(self.save_LP11)
        self.SVmin_LP11.on_changed(self.update_intensity)
        self.SVmax_LP11.on_changed(self.update_intensity)

        bsave_LP01.on_clicked(self.save_LP01)
        #self.SVmin_LP01.on_changed(self.update_LP01)
        #self.SVmax_LP01.on_changed(self.update_LP01)

        self.Bnext.on_clicked(self.next)
        self.Bprevious.on_clicked(self.previous)

        plt.show()



class Lantern_Cscan_vizualiser(object):


    def __init__(self, fig1, Cscan_LP01, Cscan_LP11):
        self.fig1 = fig1
        self.dCscan_LP01 = np.array(10*np.log(Cscan_LP01))
        self.dCscan_LP11 = np.array(10*np.log(Cscan_LP11))


    def update_intensity(self, event):

        self.l_LP11.set_clim(vmin=self.SVmin.val, vmax=self.SVmax.val)
        self.l_LP01.set_clim(vmin=self.SVmin.val, vmax=self.SVmax.val)

        self.fig.canvas.draw_idle()


    def submit(self, text):
        self.N_plot = eval(text)
        self.dBscan = self.dCscan_LP01[:,:,self.N_plot].T

        self.l_LP01.set_data(self.dBscan)
        self.l_LP11.set_data(self.dBscan)

        self.normalize_image()


        self.textbox.set_val(self.N_plot)
        self.fig.canvas.draw_idle()


    def next(self, event):
        self.N_plot += 1

        self.dBscan = self.dCscan_LP01[:,:,self.N_plot].T

        self.normalize_image()

        self.l_LP01.set_data(self.dBscan - np.mean(self.dBscan))
        self.l_LP11.set_data(self.dBscan - np.mean(self.dBscan))
        self.textbox.set_val(self.N_plot)
        self.fig.canvas.draw_idle()


    def normalize_image(self):

        self.dBscan -= np.mean(self.dBscan) - 255/2

        self.ax3.cla()
        self.ax3.hist(self.dBscan.ravel(),255)

        range = max( np.abs(np.max(self.dBscan)-255/2), np.abs(np.min(self.dBscan)-255/2) )
        std_range = 3 * np.std(self.dBscan)
        range = 5 * std_range
        print(std_range)

        self.ax3.set_xlim(255/2 - range,255/2 + range)




        self.SVmin.valmin = 255/2 - range
        self.SVmin.valmax = 255/2 + range
        self.SVmax.valmin = 255/2 - range
        self.SVmax.valmax = 255/2 + range

        self.SVmin.ax.set_xlim(self.SVmin.valmin,
                               self.SVmin.valmax)

        self.SVmax.ax.set_xlim(self.SVmax.valmin,
                               self.SVmax.valmax)



        self.SVmin.val = 255/2 - std_range
        self.SVmax.val = 255/2 + std_range
        self.SVmax.set_value = 1


        self.l_LP01.set_clim(vmin=255/2 - std_range,
                             vmax=255/2 + std_range)

        self.l_LP11.set_clim(vmin=255/2 - std_range,
                             vmax=255/2 + std_range)



    def previous(self, event):
        self.N_plot -= 1

        self.dBscan = self.dCscan_LP01[:,:,self.N_plot].T

        self.normalize_image()

        self.l_LP01.set_data(self.dBscan)
        self.l_LP11.set_data(self.dBscan)

        self.textbox.set_val(self.N_plot)
        self.fig.canvas.draw_idle()


    def save_LP11(self, event):
        save_dir = "results/"
        extent = self.ax2.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir + "figure_" + 'LP11', bbox_inches=extent)


    def save_LP01(self, event):
        save_dir = "results/"
        extent = self.ax1.get_window_extent().transformed(self.fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir + "figure_" + 'LP01', bbox_inches=extent)


    def Bscan_lanterne_plots(self):

        self.fig = plt.figure(figsize=(16,10))
        gs = gridspec.GridSpec(5,5)

        self.N_plot = 0
        self.dBscan = self.dCscan_LP11[:,:,self.N_plot].T



        self.ax3 = self.fig.add_subplot(gs[4,0:5])
        self.l_hist = self.ax3.hist(self.dBscan.ravel(),256)

        axVmin_intensity = plt.axes([0.1, 0.01, 0.8, 0.03])
        axVmax_intensity = plt.axes([0.1, 0.05, 0.8, 0.03])

        axsave_LP11 = plt.axes([0.8, 0.79, 0.1, 0.075])
        axsave_LP01 = plt.axes([0.8, 0.9, 0.1, 0.075])

        axnext = plt.axes([0.8, 0.3, 0.1, 0.075])
        axprevious = plt.axes([0.8, 0.41, 0.1, 0.075])

        Min_LP11, Max_LP11 = np.min(self.dBscan)*1, np.max(self.dBscan)*1.
        Min_LP01, Max_LP01 = np.min(self.dBscan)*1, np.max(self.dBscan)*1.

        Nstep_LP11 = (Max_LP11 - Min_LP11)/200
        Nstep_LP01 = (Max_LP01 - Min_LP01)/200

        self.SVmin = Slider(axVmin_intensity, 'Vmin', 0, 255, valinit=Min_LP11, valstep=Nstep_LP11)
        self.SVmax = Slider(axVmax_intensity, 'Vmax', 0, 255, valinit=Max_LP11, valstep=Nstep_LP11)

        temp_descr = 'wow'
        axLabel = plt.axes([0.5, 0.9, 0.11, 0.075])
        self.textbox = TextBox(axLabel, '# Scan: ', temp_descr)

        self.textbox.set_val(self.N_plot)

        bsave_LP11 = Button(axsave_LP11, 'Save Bscan')

        bsave_LP01 = Button(axsave_LP01, 'Save Bscan')

        self.Bnext = Button(axnext, 'Next')
        self.Bprevious = Button(axprevious, 'Previous')


        self.ax1 = self.fig.add_subplot(gs[1:4,0:2])
        print(np.shape(self.dBscan))
        self.l_LP01 = self.ax1.imshow(self.dBscan[:,:],
                                cmap = "gray",
                                vmin=None,
                                vmax=None)
        self.ax1.invert_yaxis()




        self.ax1.set_title("Processed Bscan LP01")

        self.ax2 = self.fig.add_subplot(gs[1:4,2:4])
        self.l_LP11 = self.ax2.imshow(self.dBscan[:,:],
                                   cmap = "gray",
                                   vmin=None,
                                   vmax=None)
        self.ax2.invert_yaxis()
        self.ax2.set_title("Processed Bscan LP11")



        self.SVmin.on_changed(self.update_intensity)
        self.SVmax.on_changed(self.update_intensity)

        self.textbox.on_submit(self.submit)

        bsave_LP11.on_clicked(self.save_LP11)
        bsave_LP01.on_clicked(self.save_LP01)

        self.Bnext.on_clicked(self.next)
        self.Bprevious.on_clicked(self.previous)

        plt.show()




# -
