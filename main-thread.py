import PySimpleGUI as sg
from ultralytics import YOLO
import cv2
from postprocessing import *

#   dP   dP                                        dP
#   88   88                                        88
# d8888P 88d888b. 88d888b. .d8888b. .d8888b. .d888b88
#   88   88'  `88 88'  `88 88ooood8 88'  `88 88'  `88
#   88   88    88 88       88.  ... 88.  .88 88.  .88
#   dP   dP    dP dP       `88888P' `88888P8 `88888P8

def running_thread(window:sg.Window):
    global run_model
    # global results, frame

    while run_model :
        ret, frame = video.read()
        if ret :
            results = model.predict(frame, verbose=verbose)
            window.write_event_value(('-THREAD-', '-FRAME-'), (results, frame))
        else:
            # Break the loop if not read
            video.release()
            run_model = False


#                     oo                        oo          
#                                                           
# 88d8b.d8b. .d8888b. dP 88d888b.    dP  dP  dP dP 88d888b. 
# 88'`88'`88 88'  `88 88 88'  `88    88  88  88 88 88'  `88 
# 88  88  88 88.  .88 88 88    88    88.88b.88' 88 88    88 
# dP  dP  dP `88888P8 dP dP    dP    8888P Y8P  dP dP    dP

# Create Layouy of the GUI
layout = [  
            [sg.Text('GUI Object Detection with Yolo V8', font='_ 14 bold')],
            [sg.Text('Enter Model Name', s=15, justification='r'), sg.InputText(default_text="yolov8s.pt",key='model_name')],
            [sg.Text('Scale to Show', s=15, justification='r'), sg.InputText(default_text="100", key= 'scale_percent')],
            [sg.Checkbox('Verbose status messages', key='-VERBOSE-')],
            [sg.Button('Run'), sg.Button('Stop'), sg.Button('Close')],
            [sg.Image(filename='', key='image')]
            ]
print(sg.framework_version)
# Create the Window
window = sg.Window('GUIYoloV8', layout)
run_model, verbose = False, False
# Event Loop to process "events"
while True:
    event, values = window.read()
    # When press Run
    if event == 'Run' and not run_model:
        # Set up model and parameter
        model = YOLO(values['model_name'])
        class_list = model.model.names
        scale_show = int(values['scale_percent'])
        # Read Video
        video = cv2.VideoCapture(0)
        # Run Signal
        run_model, verbose = True, values['-VERBOSE-']
        window.start_thread(lambda: running_thread(window), ('-THREAD-', '-END-'))
    # When press Stop or close window or press Close
    elif event in ('Stop', sg.WIN_CLOSED, 'Close'):
        if run_model : 
            run_model = False # Stop running
            video.release() # Release video
            if event != sg.WIN_CLOSED:
                window['image'].update(filename='') # Destroy picture
        # When close window or press Close
        if event in (sg.WIN_CLOSED, 'Close'):
            break
    elif event[0] == '-THREAD-':
        if event[1] == '-END-':
            continue
        elif event[1] == '-FRAME-':
            results, frame = values[event]
            labeled_img = draw_box(frame, results[0], class_list)
            display_img = resize_image(labeled_img, scale_show)
            # Show Image
            imgbytes = cv2.imencode('.ppm', display_img)[1].tobytes()
            window['image'].update(data=imgbytes)

# Close window
window.close()