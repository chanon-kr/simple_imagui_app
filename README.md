# simple_imagui_app
Simple sample of Object Detection GUI with YOLOv8 and PySimpleGUI
<br><br>
![image](https://user-images.githubusercontent.com/64777509/218513865-331b56c7-1447-4366-ae94-077fa368b9bc.png)
<br><br>
## Medium Article
https://medium.com/@chanon.krittapholchai/build-object-detection-gui-with-yolov8-and-pysimplegui-76d5f5464d6c
<br><br>
# How to use
## Git Clone
```
git clone https://github.com/chanon-kr/simple_imagui_app.git
cd simple_imagui_app
```

<br>

## Virtual Environment (Optional)
```
# Create Virtual Environment
python -m venv yologui
# Activate Virtual Environment
yologui\Scripts\activate
```

<br>

## Install Dependencies
```
# Dependencies for YOLOv8
pip install -r https://raw.githubusercontent.com/ultralytics/ultralytics/main/requirements.txt
# YOLOv8
pip install ultralytics
# PySimpleGUI
pip install pysimplegui
```

<br>

## Run Script
```python main.py```

## Run Script in threaded version
Thanks to PySimpleGUI. <3
```python main-thread.py```