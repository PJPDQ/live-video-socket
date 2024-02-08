import sys
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import cv2
import base64
app = Flask(__name__)
sio = SocketIO(app)

@app.route('/')
def index():
    '''
    To establish the client connection
    '''
    return render_template("index.html")

def message(json, methods=['GET','POST']):
    '''
    Sends message into frame-by-frame into .jpg format through websocket.
    '''
    print("Recieved message")
    sio.emit('image', json)
      
@sio.on('live_feed')
def live_feed(json):
    '''
    Send live feed from opencv video webcam to bytes jpg.
    '''
    cap=cv2.VideoCapture(0)	
    while(cap.isOpened()):
        ret,img=cap.read()
        if ret:
            img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            frame= base64.encodebytes(frame).decode("utf-8")
            message(frame)
            sio.sleep(0)
        else:
            break
          
@sio.on('connected')
def connected():
    '''
    To connect to websocket
    '''
    print("%s connected!" & request.sid)

@sio.on('disconnected')
def disconnected():
    '''
    To disconnect from open socket
    '''
    print("%s disconnected!" % request.sid)

if __name__ == "__main__":
    try:
        sio.run(app, debug=True, host="0.0.0.0", port=5000)
    except KeyboardInterrupt:
        print("Goodbye!")
        sys.exit(0)
    except Exception as e:
        import traceback
        import time
        print(time.ctime())
        print(traceback.format_exc())
        time.sleep(10)