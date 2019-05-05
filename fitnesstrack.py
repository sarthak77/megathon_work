"""
DECIDING THRESHHOLD VALUE::
Basically what we’re doing is taking different “pictures” and
comparing the difference between them. Before comparing this difference
however, we also convert these pictures to grayscale (black and white)
to make this easier. This way, after comparing these pictures, we will
have a black background where all pixels are the same and the
difference will be the white pixels. So let’s say we have about 10,000
white pixels on the screen, we can set a ‘threshold’ to classify that
as motion. We have to account for trees and clouds moving on the
screen so this ‘threshold’ value can vary from 10,000 to maybe 100,000.
It depends on many factors like daytime or nighttime, resolution, how
close the motion to detect is and so on…
"""

#importing packages
import numpy as np		      
import cv2                            
from datetime import datetime         

#function for calculating difference
def diffImg(t0, t1, t2):              
  d1 = cv2.absdiff(t2, t1)
  #print("d1::",d1)
  d2 = cv2.absdiff(t1, t0)
  #print("d2::",d2)
  #print("d1&d2::",cv2.bitwise_and(d1,d2))
  return cv2.bitwise_and(d1, d2)#and outputs only common pixels 

#threshhold is basically difference in pixel values
"""
push ups:130000 
crunches:140000 and comment second condition in if statement
"""
threshold = 130000#test for push ups                    

# Lets initialize capture on webcam
cam = cv2.VideoCapture(0)             

#naming window
winName = "Movement Indicator"	     
cv2.namedWindow(winName)              

# Read three images first:
t_minus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)

# Lets use a time check so we only take 1 pic per sec
timeCheck = datetime.now().strftime('%Ss')
#remove this condition for sudden movement changes

while True:
  # read from camera
  ret, frame = cam.read()	      

  # this is total difference number
  totalDiff = cv2.countNonZero(diffImg(t_minus, t, t_plus))

  #display text on window
  text = "threshold: " + str(totalDiff)				
  cv2.putText(frame, text, (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)  
  
  
  #if totalDiff > threshold:#for crunches
  if totalDiff > threshold and timeCheck != datetime.now().strftime('%Ss'):
    dimg= cam.read()[1]
    cv2.imwrite(datetime.now().strftime('%Y%m%d_%Hh%Mm%Ss%f') + '.jpg', dimg)
  timeCheck = datetime.now().strftime('%Ss')
  

  # Read next image
  t_minus = t
  t = t_plus
  t_plus = cv2.cvtColor(cam.read()[1], cv2.COLOR_RGB2GRAY)
  cv2.imshow(winName, frame)
  
  #comment to hide camera window
  key = cv2.waitKey(10)#-1
  if key == 27:			 
    cv2.destroyWindow(winName)
    break
