## Sign Language Detection System
Areal-time **hand gesture recognition** system using **CNN** and **computer vision**. It detects and classifies the **American sign language** from webcam feed.

## How to run
### Locally
To run locally, execute the app.py script : 'python app.py'. The app will start to webcam which detects and classifies the hand gestures.
### In Docker
Build a docker image
'sudo docker build -t hand-gesture:latest .'\
Run the following command before starting Docker:
'xhost +local:'\
Run the image by giving webcam access to the container:\
'docker run --rm -it \ \
    --device=/dev/video0:/dev/video0 \ \
    --env DISPLAY=$DISPLAY \ \
    --env QT_X11_NO_MITSHM=1 \ \
    --volume /tmp/.X11-unix:/tmp/.X11-unix \ \
    hand_gesture'\
This will start real-time hand gesture classification.

## Sample Classification
