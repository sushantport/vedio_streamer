import time
import argparse
import socketio
import cv2
import base64

from cv import *


def _convert_image_to_jpeg(image):
        # Encode frame as jpeg
        frame = cv2.imencode('.jpg', image)[1].tobytes()
        # Encode frame in base64 representation and remove
        # utf-8 encoding
        frame = base64.b64encode(frame).decode('utf-8')
        return "data:image/jpeg;base64,{}".format(frame)
def data_tranfer(frame,msg):
    stream = _convert_image_to_jpeg(frame)
    sio.emit(
        'cv2server',
        {
            'image':stream,
            'text': msg
        })
    time.sleep(2)
    


sio = socketio.Client()


# sio.connect(
#                 'http://localhost:5001')
# #while True:

try:
    sio.connect('http://127.0.0.1:5000')
    print("connected")
    #call opencv vedio handler
    cap = cv2.VideoCapture(0)

    while(True):
        #get all opencv frame
        # Capture frame-by-frame
        ret, frame = cap.read()
        frame=convert_gray_scale(frame)
        msg={'key':1,
             'dst':10}
        
        data_tranfer(frame,msg)
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
except Exception as e:
    print("cant connetc to server")
finally:
    sio.disconnect()

    print("disconnected")



