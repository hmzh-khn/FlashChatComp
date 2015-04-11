import cv2
import numpy as np
import sys
import io
import matplotlib.pyplot as plt

if __name__ == "__main__":
	print "Using OpenCV v" + cv2.__version__

	import cv2

	cap = cv2.VideoCapture(0)
	hist = []
	hist1 = []
	while(True):
		# Capture frame-by-frame
		ret, frame = cap.read()
		cv2.imshow('frame',frame)
		hist = cv2.calcHist([frame],[0],None,[256],[0,256])
		plt.plot(hist)
		plt.plot(hist1)
		print hist
		hist1 = hist
		hist = [h for [h] in hist]

		plt.hist(frame.ravel(),256,[0,256]); plt.show()
		
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()

	# cv2.NamedWindow("w1", cv2.CV_WINDOW_AUTOSIZE)
	# # capture = cv2.CaptureFromCAM(0)

	# def repeat():
	# 	# capture = cv2.CaptureFromCAM(0)
	# 	# cv2.SetCaptureProperty(capture, cv2.CV_CAP_PROP_FRAME_HEIGHT, 400)
	# 	# cv2.SetCaptureProperty(capture, cv2.CV_CAP_PROP_FRAME_WIDTH, 600)
	# 	# cv2.SetCaptureProperty(capture, cv2.CV_CAP_PROP_FORMAT, cv2.IPL_DEPTH_32F)
	# 	# img = cv2.QueryFrame(capture)

	# 	# frame = cv2.QueryFrame(capture)
	# 	# # img1 = cv2.CaptureFromCAM(0)
	# 	# cv2.ShowImage("w1", frame)
	# 	# # img = cv2.imread(img1);
	# 	# print "Histogram: "+cv2.calcHist([img],[0],None,[256],[0,256])

	# 	# stream = io.BytesIO()

	# 	# camera.capture(stream)
 #  #       # Construct a numpy array from the stream
 #  #       data = np.fromstring(stream.getvalue(), dtype=np.uint8)
 #  #       # "Decode" the image from the array, preserving colour
 #  #       image = cv2.imdecode(data, 1)
 #  #       cv2.imshow('frame', image)

 #        #import numpy as np


	# while True:
	# 	repeat()
	# 	key = cv2.waitKey(20)
	# 	if key == 27: # exit on ESC
	# 		break

