# https://www.pysimplegui.org/en/latest/#jump-start
import PySimpleGUI as sg

# Create Layouy of the GUI
layout = [  
            [sg.Text('GUI Object Counting with Yolo V8')],
            [sg.Text('Enter Model Name', size= (15)), sg.InputText(key='model_name')],
            [sg.Text('X-line for Counting', size= (15)), sg.InputText(key= 'line_position')],
            [sg.Button('Run'), sg.Button('Stop'), sg.Button('Close')],
            [sg.Text('PICTURE')],
            [sg.Text('Left-to-Right', size= (15), key='out1'), sg.Text("0", key='out1-v')],
            [sg.Text('Right-to-Left', size= (15), key='out2'), sg.Text("0", key='out2-v')]
            ]

# Create the Window
window = sg.Window('GUIYoloV8-Counting', layout)
# Event Loop to process "events"
while True:
    event, values = window.read()
    # When press Run
    if event == 'Run' : 
        print(values)
    # When close window or press Close
    if event in (sg.WIN_CLOSED, 'Close'): break

# Close window
window.close()
