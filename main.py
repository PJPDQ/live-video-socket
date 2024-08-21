import sys
import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import cv2
import base64
import time
from pathlib import Path
import getopt

app = Flask(__name__)
sio = SocketIO(app)

cwd = os.getcwd()
save_dir = f'{cwd}\\saved_dir'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

def check_camera(source):
    source = str(source).strip()
    chunks = source.split(':')
    # handle drive letter ('c:', ...)
    if len(chunks) > 1 and len(chunks[0]) == 1 and chunks[0].isalpha():
        chunks[1] = chunks[0] + ':' + chunks[1]
        del chunks[0]

    source = chunks[0]
    try: source = int(source)
    except ValueError: pass
    params = dict( s.split('=') for s in chunks[1:] )

    cap = None
    try:
        return source
    except Exception as e:
        print(f"error = {e}")
        return None

args, sources = getopt.getopt(sys.argv[1:], '', 'shotdir=')
args = dict(args)
shotdir = args.get('--shotdir', '.')
if len(sources) == 0:
    sources = [ 0 ]

print(check_camera(sources))


@app.route('/')
def index():
    '''
    To establish the client connection
    '''
    return render_template("index.html")


def message(json, methods=['GET', 'POST']):
    '''
    Sends message into frame-by-frame into .jpg format through websocket.
    '''
    # print("Recieved message")
    sio.emit('image', json)

@sio.on('live_feed')
def live_feed(json):
    '''
    Send live feed from opencv video webcam to bytes jpg.
    '''

    # source = check_camera(source)
    os.chdir(save_dir)
    cap = cv2.VideoCapture(0)
    digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))
    n = 0
    if not cap.isOpened():
        print("error!")
    while (cap.isOpened()):
        ret, img = cap.read()
        if ret:
            img_file = f"sample_{str(n).zfill(digit)}.jpg"
            img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
            is_write = cv2.imwrite(img_file, img)
            # for debugging purpose to see if the image is saved and stored.
            # if is_write:
            #     print(f"image saved and can be found in {img_file}")
            frame = cv2.imencode('.jpg', img)[1].tobytes()
            frame = base64.encodebytes(frame).decode("utf-8")
            message(frame)
            n += 1
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
