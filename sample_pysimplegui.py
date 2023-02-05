# https://www.pysimplegui.org/en/latest/#jump-start
import PySimpleGUI as sg

# Create Layouy of the GUI
layout = [  
            [sg.Text('GUI Object Detection with Yolo V8')],
            [sg.Text('Enter Model Name'), sg.InputText(key='model_name')],
            [sg.Text('Scale to Show'), sg.InputText(key= 'scale_percent')],
            [sg.Button('Run'), sg.Button('Stop'), sg.Button('Close')],
            [sg.Text('Will Show Result in This Section')],
            [sg.Text(text_color='black', key='out')]
            ]

# Create the Window
window = sg.Window('GUIYoloV8', layout)
# Event Loop to process "events"
while True:
    event, values = window.read()
    # When press Run
    if event == 'Run' : 
        print(values)
        window['out'].update(str(values))
    # When close window or press Close
    if event in (sg.WIN_CLOSED, 'Close'): break

# Close window
window.close()