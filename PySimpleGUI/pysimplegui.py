import numpy as np 
import pydicom
import PySimpleGUI as sg
import cv2

'''
This script uses the PySimpleGUI library to allow the user to view slices of the DICOM image from 3 points of view. 
The radio object must be selected so that the progame knows what slider to be listening to.
'''

#https://realpython.com/pysimplegui-python/
def selectview():
    #read image
    filename = "IM_0001.dcm"
    dataset = pydicom.dcmread(filename)
    img_full = dataset.pixel_array
    
    print(img_full.shape)
    #get dimensions
    dim1=img_full.shape[0]-1
    dim2=img_full.shape[1]-1
    dim3=img_full.shape[2]-1

    thickness=10
    dimstr="Resolution= " + str(img_full.shape[0]) + "x" + str(img_full.shape[1]) + "x" + str(img_full.shape[2]) + "\nSlice Thickness=" + str(thickness)

    sg.theme("LightGreen")

    #panel_flag=1
    # Define the window layout #need to add key to cropping input
    layout = [
        [sg.Text("Vessel Segmentation", size=(60, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE1-"),sg.Image(filename="", key="-IMAGE2-"),sg.Image(filename="", key="-IMAGE3-"),sg.Text(dimstr, size=(25, 2), justification="left")],
        [sg.Button('Crop res1', size =(8, 1)), sg.InputText(size =(5, 1))],
        [sg.Radio("None", "Radio", True, size=(10, 1))],
        [
            sg.Radio("dim1", "Radio", size=(10, 1), key="-DIM1-"),
            sg.Slider(
                (0, dim1),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-DIM1 SLIDER-",
            ),
        ],
        [
            sg.Radio("dim2", "Radio", size=(10, 1), key="-DIM2-"),
            sg.Slider(
                (0, dim2),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-DIM2 SLIDER-",
            ),
        ],
        [
            sg.Radio("dim3", "Radio", size=(10, 1), key="-DIM3-"),
            sg.Slider(
                (0, dim3),
                0,
                1,
                orientation="h",
                size=(40, 15),
                key="-DIM3 SLIDER-",
            ),
        ],
        [sg.Button("Exit", 'Centre', size=(10, 1))],
    ]

    # Create the window and show it without the plot
    window = sg.Window("OpenCV Integration", layout, location=(0, 0))
    x=0
    y=0
    z=0
    while True:
        event, values = window.read(timeout=20)
        if event == sg.WIN_CLOSED:
            break

        if event == "Exit":
            panel_flag=2
            print("pressed")
            break
            print("next panel")

        if values["-DIM1-"]:
            x=int(values["-DIM1 SLIDER-"])

        elif values["-DIM2-"]:
            y=int(values["-DIM2 SLIDER-"])

        elif values["-DIM3-"]:
            z=int(values["-DIM3 SLIDER-"])
        
        frame1=img_full[x,:,:]
        frame2=img_full[:,y,:]
        frame3=img_full[:,:,z]

        imgbytes1 = cv2.imencode(".png", frame1)[1].tobytes()
        window["-IMAGE1-"].update(data=imgbytes1)

        imgbytes2 = cv2.imencode(".png", frame2)[1].tobytes()
        window["-IMAGE2-"].update(data=imgbytes2)

        imgbytes3 = cv2.imencode(".png", frame3)[1].tobytes()
        window["-IMAGE3-"].update(data=imgbytes3)
    window.close()




selectview()