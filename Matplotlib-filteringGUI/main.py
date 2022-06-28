import matplotlib.pyplot as plt
import pydicom
from skimage import feature
from skimage.filters import gaussian, sobel, scharr
from matplotlib.colors import NoNorm
import numpy as np 
import pyvista as pv
import cv2
import os

#import neck_length functions
from select_img import select_img
from guiclasses import *

vessel=Vessel()

#root=r'C:\Users\zaina\Documents\Masters-new\git\neck_length\data\twh1433\OYCDLVQQ\XVKSBCHO'
root=r'C:\Users\zaina\Documents\Masters-new\git\neck_length\data\2D DSA DICOM\2D DSA DICOM\twh1317\0RBHFGDV\PDLLNNPK'
arr = os.listdir(root)
print(arr)
#open 2DRA format
filename= root + "\\" + arr[0]
print("Reading" + filename)
file= pydicom.dcmread(filename)
img=file.pixel_array
x_len=len(arr)
y_len,z_len= img.shape
img_mat = np.empty([x_len,y_len,z_len])

for i in range(x_len):
    filename=root + "\\" + arr[i]
    #print("Reading" + filename)
    try:
        file= pydicom.dcmread(filename)
    except:
        print("warning: Non DICOM file")
    img_mat[i,:,:]=file.pixel_array


vessel.dataset=img_mat
select_img(vessel)

#img[img>1000]=0
#plt.hist(img, bins = 50)
#plt.show()

#plt.imshow(scimg,cmap='gray')
#plt.show()
#Apply threshold

#compute gradient

#display gradient image
'''
#apply sobel
g= sobel(img)
#gr=scharr(img)
print(g.min())
print(g.max())
    #divide by maximum value? Normalize maybe
gr = g / g.max()
gr_g = gaussian(gr, 1.0, truncate=4.0)
supergrad = gr - gr_g
supergrad = supergrad / supergrad.max()
print(supergrad.max())
edges1 = feature.canny(g)
print(edges1.max())
print(edges1.min())
#plt.hist(edges, bins = 50)
#plt.show()
#compute binary

ret,thresh_img = cv2.threshold(supergrad, 1, 255, 0)
#find contours
image,contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

cv2.drawContours(image, contours, -1, (0,255,0), 3)
cv2.imwrite('sobel_contours.jpg',image)
img=img/img.max()
print(img.max())
added=img + (g)
#figure screen and subplot definition
fig, ax = plt.subplots(1,1)
ax.axis('off')
plt.imshow(edges1, cmap='gray')
#plt.imshow(scimg,cmap='gray')
plt.show()
'''






'''
fig, (ax1,ax2) = plt.subplots(1,2)
fig.subplots_adjust(top=0.9, bottom=0.3, left=0.02, right=0.98, hspace=0.0, wspace=0.07)
#ax1.axis('off')
myobj1=ax1.imshow(img,cmap='gray')
myobj2=ax2.imshow(gr,cmap='gray')
plt.show()



#add marker

#compute length

    def set_threshold(self, value):
        """ Set approx value of surface contour.
        """
        self.threshold_value = value
        self.temp_contour_val = value

    def compute_DoG_gradient(self, im):
        """ Compute difference-of-Gaussians of gradient.
        """
        dims = np.array(im.dimensions)
        im_up = im.point_data['image'].reshape(dims, order="F")
        gr = sobel(im_up)
        
        gr = gr / gr.max()
        gr_g = gaussian(gr, 1.0, truncate=4.0)

        supergrad = gr - gr_g
        supergrad = supergrad / supergrad.max()

        im.point_data['gradient'] = gr.flatten(order="F")
        im.point_data['DoG_gradient'] = supergrad.flatten(order="F")
'''
