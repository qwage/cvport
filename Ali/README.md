————————————————————————————————————————————————————————————————————————
1. Haarcascade: READ this section if you are particularly interested on running the Haarcascade program

Running the Haarcascade program on your machine does not require much configuratoin. haar.py is the main file that will run the Haarcascade. It has three main for loops, each one concerns a different Haarcascade for a different feature to be detected. In my program, the Haarcascades are for the eyes, the full human body, and the upper part of the human body. The xml files in the same directory define the features of those things we want to look for. Just make sure you have all the libraries required and the xml file(s) on the same directory. And make sure to comment/uncomment what for loop(s) (Haarcascade) and lines you would like to be performed. 

Note: Running multiple Haarcascades is a computationally expensive operation and could slow down your camera (FPS).


————————————————————————————————————————————————————————————————————————
2. Tiny-YOLO: READ this section if you are particularly interested on running the Tiny-YOLO program on your raspberry pi, which we will refer to as YOLO during the
   explanation process.

There are few assumptions I am making about your raspberry pi that you will have to take care of before continuing:

a. You have a raspberry pi 4 that has at least one 3.0 USB connector (the blue USB connector)

b. You have the Neural Compute Stick 2 by Intel and a camera connected to your pi

c. You have a virtual environment called “cv” that has opencv and python configured on it. If not, I suggest you stop and go do that. An excellent source would be:
   https://www.pyimagesearch.com/2019/09/16/install-opencv-4-on-raspberry-pi-4-and-raspbian-buster/ 
   
d. You have a virtual environment called “openvino” that has opencv, python, and the Neural Compute Stick 2 packages on it. If not, I suggest you stop and go do 
   that. An excellent source would be: https://www.pyimagesearch.com/2019/04/08/openvino-opencv-and-movidius-ncs-on-the-raspberry-pi/
   

After having those four things done and having your essentials with you (raspberry pi 4, camera, the Neural Compute Stick 2, etc), now we can continue. Note: The 
YOLO code does not need configuration with the raspberry pi, its the Neural Compute Stick 2 that needs configuration with the raspberry pi. And to do it:

I. On your openvino virtual environment run the below command to install the JSON-Minify package needed for this, and after, plug your Neural Compute Stick 2
   in the 3.0 USB Connector on the Pi.

        pip install json_minify

II. Execute those two command lines below

        workon openvino
        source ~/openvino/bin/setupvars.sh

III. Navigate to your YOLO file which you downloaded from GitHub, and run this command to start YOLO

	python detect_realtime_tinyyolo_ncs.py --conf config/config.json


Now YOLO should work on your pi with no issues (you can press q on your keyboard to stop YOLO). Note that you can change the threshold detection probability (percentage) by navigating to the config folder and changing the “prob_threshold” variable to something else in the config.json file. The variable should be something between 0 and 1 to set the minimum threshold of detection probability. Also, note that this YOLO code has been trained to detect 80 different objects only. The list of those objects can be found in the coco.names file inside the yolo folder. In addition, if you are interested in the coordinates of the objects detetcted, there is a variable called "Coordinates" in the detect_realtime_tinyyolo_ncs.py file that saves all the objects coordinates.


I created a collab google sheet which will demonstrate YOLO or/and Tiny-YOLO on any YouTube video or a video from your computer without any coding needed. It can be used to determine whether YOLO is the object detection algorithm you want on your pi or not.
      https://colab.research.google.com/drive/13PYrnmTp5Q48vR_GRMnEN4T_6R5xorNm?usp=sharing


————————————————————————————————————————————————————————————————————————
For Any inquiries/issues, please contact me at: aalmakhm@purdue.edu or alialmakhmari99@hotmail.com
 
