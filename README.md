# Live Feed Video Socket from Flask Server to HTML
A Live Video Rendering process that sends live images into frames to feed to Web HTML that shows the base64/ jpeg json data that is view in the video.

# Processes
A Video is captured from the device webcam that sends the image into bytes sizes that is being emitted through bi-directional SocketIO. The socketio will then sends the images into the simple website that display the image as it moves and display the data in base64 format jpeg.

# Installation
1. Install the python packages
```bash
pip install -r requirements.txt
```

2. Run the python script
```bash
python main.py
```

3. Open a browser and go to
http://localhost:5000


