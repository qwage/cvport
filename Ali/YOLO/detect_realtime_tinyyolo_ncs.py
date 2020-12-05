# USAGE
# python detect_realtime_tinyyolo_ncs.py --conf config/config.json \
# 	--input videos/test_video.mp4

# import the necessary packages
from openvino.inference_engine import IENetwork
from openvino.inference_engine import IEPlugin
from intel.yoloparams import TinyYOLOV3Params
from intel.tinyyolo import TinyYOLOv3
from imutils.video import VideoStream
from pyimagesearch.utils import Conf
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import time
import cv2
import os

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--conf", required=True,
	help="Path to the input configuration file")
ap.add_argument("-i", "--input", help="path to the input video file")
args = vars(ap.parse_args())

# load the configuration file
conf = Conf(args["conf"])

# load the COCO class labels our YOLO model was trained on and
# initialize a list of colors to represent each possible class
# label
LABELS = open(conf["labels_path"]).read().strip().split("\n")
np.random.seed(42)
COLORS = np.random.uniform(0, 255, size=(len(LABELS), 3))

# initialize the plugin in for specified device
plugin = IEPlugin(device="MYRIAD")

# read the IR generated by the Model Optimizer (.xml and .bin files)
print("[INFO] loading models...")
net = IENetwork(model=conf["xml_path"], weights=conf["bin_path"])

# prepare inputs
print("[INFO] preparing inputs...")
inputBlob = next(iter(net.inputs))

# set the default batch size as 1 and get the number of input blobs,
# number of channels, the height, and width of the input blob
net.batch_size = 1
(n, c, h, w) = net.inputs[inputBlob].shape

# if a video path was not supplied, grab a reference to the webcam
if args["input"] is None:
	print("[INFO] starting video stream...")
	# vs = VideoStream(src=0).start()
	vs = VideoStream(usePiCamera=True).start()
	time.sleep(2.0)

# otherwise, grab a reference to the video file
else:
	print("[INFO] opening video file...")
	vs = cv2.VideoCapture(os.path.abspath(args["input"]))

# loading model to the plugin and start the frames per second
# throughput estimator
print("[INFO] loading model to the plugin...")
execNet = plugin.load(network=net, num_requests=1)
fps = FPS().start()

# loop over the frames from the video stream
while True:
	# grab the next frame and handle if we are reading from either
	# VideoCapture or VideoStream
	orig = vs.read()
	orig = orig[1] if args["input"] is not None else orig

	# if we are viewing a video and we did not grab a frame then we
	# have reached the end of the video
	if args["input"] is not None and orig is None:
		break

	# resize original frame to have a maximum width of 500 pixel and
	# input_frame to network size
	orig = imutils.resize(orig, width=500)
	frame = cv2.resize(orig, (w, h))

	# change data layout from HxWxC to CxHxW
	frame = frame.transpose((2, 0, 1))
	frame = frame.reshape((n, c, h, w))

	# start inference and initialize list to collect object detection
	# results
	output = execNet.infer({inputBlob: frame})
	objects = []

	# loop over the output items
	for (layerName, outBlob) in output.items():
		# create a new object which contains the required tinyYOLOv3
		# parameters
		layerParams = TinyYOLOV3Params(net.layers[layerName].params,
			outBlob.shape[2])

		# parse the output region
		objects += TinyYOLOv3.parse_yolo_region(outBlob,
			frame.shape[2:], orig.shape[:-1], layerParams,
			conf["prob_threshold"])

	# loop over each of the objects
	for i in range(len(objects)):
		# check if the confidence of the detected object is zero, if
		# it is, then skip this iteration, indicating that the object
		# should be ignored
		if objects[i]["confidence"] == 0:
			continue

		# loop over remaining objects
		for j in range(i + 1, len(objects)):
			# check if the IoU of both the objects exceeds a
			# threshold, if it does, then set the confidence of that
			# object to zero
			if TinyYOLOv3.intersection_over_union(objects[i],
				objects[j]) > conf["iou_threshold"]:
				objects[j]["confidence"] = 0

	# filter objects by using the probability threshold -- if a an
	# object is below the threshold, ignore it
	objects = [obj for obj in objects if obj['confidence'] >= \
		conf["prob_threshold"]]

	# store the height and width of the original frame
	(endY, endX) = orig.shape[:-1]

	# loop through all the remaining objects
	for obj in objects:
		# validate the bounding box of the detected object, ensuring
		# we don't have any invalid bounding boxes
		if obj["xmax"] > endX or obj["ymax"] > endY or obj["xmin"] \
			< 0 or obj["ymin"] < 0:
			continue

		# build a label consisting of the predicted class and
		# associated probability
		label = "{}: {:.2f}%".format(LABELS[obj["class_id"]],
			obj["confidence"] * 100)

		# calculate the y-coordinate used to write the label on the
		# frame depending on the bounding box coordinate
		y = obj["ymin"] - 15 if obj["ymin"] - 15 > 15 else \
			obj["ymin"] + 15
		
		#Coordinate boxes starting from the bottom left coordinate and going anti-clockwise around
		Coordinates = [[obj["xmin"],obj["ymin"]], [obj["xmax"],obj["ymin"]], [obj["xmax"],obj["ymax"]], [obj["xmin"],obj["ymax"]]]
        
		# draw a bounding box rectangle and label on the frame
		cv2.rectangle(orig, (obj["xmin"], obj["ymin"]), (obj["xmax"],
			obj["ymax"]), COLORS[obj["class_id"]], 2)
		cv2.putText(orig, label, (obj["xmin"], y),
			cv2.FONT_HERSHEY_SIMPLEX, 1, COLORS[obj["class_id"]], 3)

	# display the current frame to the screen and record if a user
	# presses a key
	cv2.imshow("TinyYOLOv3", orig)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

	# update the FPS counter
	fps.update()
	
# stop the timer and display FPS information
fps.stop()
print("[INFO] elapsed time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# stop the video stream and close any open windows1
vs.stop() if args["input"] is None else vs.release()
cv2.destroyAllWindows()
