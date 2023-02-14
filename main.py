import PySimpleGUI as sg
from ultralytics import YOLO
import cv2
from postprocessing import *

# Create Layouy of the GUI
layout = [  
            [sg.Text('GUI Object Detection with Yolo V8', font='_ 14 bold')],
            [sg.Text('Enter Model Name', s=15, justification='r'), sg.InputText(default_text="yolov8s.pt",key='model_name')],
            [sg.Text('Scale to Show', s=15, justification='r'), sg.InputText(default_text="100", key= 'scale_percent')],
            [sg.Button('Run'), sg.Button('Stop'), sg.Button('Close')],
            [sg.Image(filename='', key='image')]
            ]

# Create the Window
window = sg.Window('GUIYoloV8', layout, finalize=True)
run_model = False
# Event Loop to process "events"
while True:
    event, values = window.read(timeout=0)
    # When press Run
    if event == 'Run' : 
        # Set up model and parameter
        model = YOLO(values['model_name'])
        class_list = model.model.names
        scale_show = int(values['scale_percent'])
        # Read Video
        video = cv2.VideoCapture(0)
        # Run Signal
        run_model = True
    # When press Stop or close window or press Close
    elif event in ('Stop', sg.WIN_CLOSED, 'Close'):
        if run_model : 
            run_model = False # Stop running
            video.release() # Release video
            if event != sg.WIN_CLOSED : window['image'].update(filename='') # Destroy picture
        # When close window or press Close
        if event in (sg.WIN_CLOSED, 'Close'): break
    # Run Model
    if run_model : 
        ret, frame = video.read()
        if ret :
            results = model.predict(frame,verbose = False)
            labeled_img = draw_box(frame, results[0], class_list)
            display_img = resize_image(labeled_img, scale_show)
            # Show Image
            imgbytes = cv2.imencode('.png', display_img)[1].tobytes()
            window['image'].update(data=imgbytes)
        else: 
            # Break the loop if not read
            video.release()
            run_model = False

# Close window
window.close()