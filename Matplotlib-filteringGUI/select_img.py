import matplotlib.pyplot as plt
import pydicom
#from matplotlib.widgets import Cursor
from matplotlib.widgets import Button,Slider,CheckButtons,RadioButtons
import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtCore import pyqtSlot
from skimage.filters import gaussian, sobel, scharr
import sys
#import neck_length functions
from guiclasses import *

import matplotlib as mpl

mpl.rcParams['keymap.back'].remove('left')
mpl.rcParams['keymap.forward'].remove('right')

def select_img(vessel):
    grad_flag=0
    print("selecting image")
    #figure out how to plot it with the colored plots
    #pg.image(g)
    #pg.image(new_img)

    img_full = vessel.dataset
    new_img=np.empty(img_full.shape)
    super_img=np.empty(img_full.shape)

    for i in range(img_full.shape[0]):
        new_img[i,:,:]=sobel(img_full[i])

    for i in range(img_full.shape[0]):
        g=new_img[i].copy()
        gr = g / g.max()
        gr_g = gaussian(gr, 1.0, truncate=4.0)
        supergrad = gr - gr_g
        super_img[i,:,:]= supergrad / supergrad.max()

    print(img_full.max(), new_img.max(), super_img.max())


    frame1=img_full[0,:,:]
    frame2=new_img[0,:,:]
    frame3=super_img[0,:,:]

    dim1=img_full.shape[0]-1
    #dim2=img_full.shape[1]-1
    #dim3=img_full.shape[2]-1

    #put this inside the checkbutton loop if statements
    dim=dim1
    fig, (ax,ax2,ax3) = plt.subplots(1,3)
    #fig.tight_layout(pad=0.1, w_pad=0.2, h_pad=0.5)
    fig.subplots_adjust(top=0.9, bottom=0.3, left=0.02, right=0.98, hspace=0.0, wspace=0.07)
    ax.axis('off')
    ax2.axis('off')
    ax3.axis('off')

    myobj=ax.imshow(frame1,cmap='gray')
    myobj2=ax2.imshow(frame2,cmap='gray')
    myobj3=ax3.imshow(frame3,cmap='gray')
    fig.suptitle('regular, grad, supergrad',fontsize=16)
    #ax.set_title('Select a View',fontsize=12)

    #keyboard press
    def on_press(event):
        print('press', event.key)
        sys.stdout.flush()
        if event.key == "g":
            grad_flag=1
            print("switched to gradient")
        if event.key == "r":
            grad_flag=0
            print("switched to regular")
        update(vessel.sliderval[0])

    fig.canvas.mpl_connect('key_press_event', on_press)

    #button controlled slider changes
    def prev(event):
        vessel.sliderval[0]= vessel.sliderval[0] - 1
        update(vessel.sliderval[0])
        samp.set_val(vessel.sliderval[0])

    def next(event):
        vessel.sliderval[0]= vessel.sliderval[0] + 1
        update(vessel.sliderval[0])
        samp.set_val(vessel.sliderval[0])

    # .axes(offset from left, verctical placement, horizontal thickness, vertical thickness)
    axamp  = plt.axes([0.1, 0.25, 0.65, 0.03])

    samp = Slider(axamp, 'Slice', 1, dim, valinit=0,valstep=1,color="purple")

    #slider 1 buttons
    axprev = plt.axes([0.80, 0.25, 0.05, 0.03])
    axnext = plt.axes([0.86, 0.25, 0.05, 0.03])

    bprev= Button(axprev, 'Prev')
    bprev.on_clicked(prev)
    bnext= Button(axnext, 'Next')
    bnext.on_clicked(next)


    def update(val):
        print(val)
        vessel.sliderval[0]=val
        vessel.view=1
        vessel.slice=val


        frame1=img_full[val,:,:]
        frame2=new_img[val,:,:]
        frame3=super_img[val,:,:]

        myobj.set_data(frame1)
        myobj2.set_data(frame2)
        myobj3.set_data(frame3)

    samp.on_changed(update)
    plt.show()
    plt.close()
    print(vessel.slice)
