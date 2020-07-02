import time
import argparse
import socketio
import cv2
import base64
import multiprocessing
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
    print("data emited")
    time.sleep(2)
    
def streamer(uri):
    sio.connect('http://127.0.0.1:5000')
    print("connected")
    cap = cv2.VideoCapture(uri)
    print("process running")

    while(True):
        #get all opencv frame
        # Capture frame-by-frame
        ret, frame = cap.read()
        print(ret)
        frame=convert_gray_scale(frame)
        msg={'key':1,
             'dst':10}
        
        data_tranfer(frame,msg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    sio.disconnect()

sio = socketio.Client()


# sio.connect(
#                 'http://localhost:5001')
# #while True:

try:
    
    
    #call opencv vedio handler
    procs=1
    jobs=[]
    for i in range (1):
       
        process=multiprocessing.Process(target=streamer,args=(0,))
        jobs.append(process)
        print("prepared job")
    for j in jobs:
        j.start()
    for j in jobs:
        j.join()

    
except Exception as e:
    print("cant connetc to server")
finally:
    

    print("disconnected")



