# opencv-dnn-flask
Restful API on Flask-RestX for OpenCV DNN such as YOLO

## Contents

* main.py - Main program initiating Flask endpoint from inference/api.py
   * inference/api.py - Defines the SWAGGER document, and the invocation for the `/prediction` endpoint
      * inference/data_source - Source of images, such as Video camera or staic images
      * inference/predictions - The prediction model and the DTO for the prediction result

## How to use

1. Git clone this repository
2. Creates a Python virtual environment, such as `python3 -m venv .`
3. Enter the virtual environment. If using `venv` the command is `source bin/activate`
4. Install all dependencies using PIP with command `python3 -m pip install -r requirements`

### Update the image source
1. Edit the file `inference/data_source/camera.py` with the right Video camera source, or extend the file `inference/data_source/source.py` with your own, such as to read from a folder
2. Run the main.py to run the self-hosted Flask server with command `python3 main.py`

### Test out the Rest API
1. Open a browser and go to `http://127.0.0.1:5000/`
2. Expand the `Detection` -> hit the `GET` -> `Try it out` -> `Execute`. If the invocation is successful you should receive a response with code 200.