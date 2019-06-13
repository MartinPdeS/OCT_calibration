
'''_____Standard imports_____'''
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons


'''_____Project imports_____'''
from toolbox.fits import gauss


def dB_plot(data1, data2=None, arguments=None):

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


def interactive_shift(spectra1, param1, spectra2, param2, arguments=None):


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


def Bscan_plots(fig1, fig2, Bscan, arguments=None):

    Bscan = np.array(Bscan)
    dBscan = 10*np.log(Bscan)

    fig = plt.figure(figsize=(16,10))


    ax0 = fig.add_subplot(221)
    ax0.grid()
    ax0.set_ylabel('Magnitude [dB]')
    ax0.set_xlabel('Wavenumber k [U.A]')
    ax0.set_title("Spectra")
    ax0.plot(fig1)



    ax1 = fig.add_subplot(222)
    ax1.grid()
    ax1.set_ylabel('Magnitude [dB]')
    ax1.set_xlabel('Wavenumber k [U.A]')
    ax1.set_title("Aline")
    ref = np.min(dBscan[200])
    ax1.plot(fig2)
    #ax1.invert_xaxis()


    print('###############')



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
        save_dir = "results/"
        extent = ax2.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
        plt.savefig(save_dir + arguments.input_file, bbox_inches=extent)


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









# -
