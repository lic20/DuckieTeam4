#!/usr/bin/env python
import cv2
import rospy
import apriltag
import numpy
from cv_bridge import CvBridge, CvBridgeError

from duckietown.dtros import DTROS, NodeType, TopicType, DTParam, ParamType
from sensor_msgs.msg import CompressedImage
from duckietown_msgs.msg import Twist2DStamped

class TagDetectionNode():
    def __init__(self):
        self.node_name = "TagDetectorNode"

        #intialize a publisher and subscriber
        self.sub_image = rospy.Subscriber("~corrected_image/compressed", CompressedImage, self.processImage, queue_size=1)

        self.pub = rospy.Publisher("~apriltag_img", Image, queue_size=1)
        self.pub_car_cmd = rospy.Publisher("~car_cmd", Twist2DStamped, queue_size=1, dt_topic_type=TopicType.CONTROL)

        self.tag_list = []
        self.duckie = False
       

    def processImage(self, image_msg):
        self.stats.received()

        if not self.active:
            return
        
        try:
            self.processImage_(image_msg)
        finally:
            return

    def processImage_(self, image_msg):

        # Decode from compressed image with OpenCV
        try:
            image_cv = bgr_from_jpg(image_msg.data)
        except ValueError as e:
            self.loginfo('Could not decode image: %s' % e)
            return


        print('Image is decoded')
        
        #yellow duckie detection
        self.duckie = False
        ratio = duckie_detection(image_cv)
        if ratio >= 1.0:
            self.duckie = True
            print('Duckie in sight')

        #perform apriltag detection
        img_gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        detector = apriltag.Detector()
        result = detector.detect(img)

        color = (0, 0, 255)
        thickness = 2
        self.tag_list = []

        for det in result:
            start_point = (int(det.corners[1][0]), int(det.corners[1][1]))
            end_point = (int(det.corners[3][0]),int(det.corners[3][1]))
            rect_size = abs((start_point[0] - end_point[0])*(start_point[1] - end_point[1]))
            tag = {'size': rect_size, 'center': det.center}
            self.tag_list.append(tag)

            image_cv = cv2.rectangle(image_cv, start_point, end_point, color, thickness)
        
        
        #print(self.tag_list)
        self.tag_list = sorted(self.tag_list, key= lambda i: i['size'])
        self.pub.publish(image_cv)
    

    def duckie_detection(img):
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        '''yellow'''
        # Range for upper range
        yellow_lower = numpy.array([20, 100, 100])
        yellow_upper = numpy.array([30, 255, 255])
        mask_yellow = cv2.inRange(hsv, yellow_lower, yellow_upper)

        yellow_output = cv2.bitwise_and(img, img, mask=mask_yellow)

        yellow_ratio =(cv2.countNonZero(mask_yellow))/(img.size/3)

        result = numpy.round(yellow_ratio*100, 2)
        print("Duckie in image ratio", result)
        return result


    def speed_cmd(self)
        car_control_msg = Twist2DStamped()

        v = 1
        omega = 0


        if len(self.tag_list) == 0:
            go_forward = False
        else:
            closest_tag = self.tag_list[-1]
            print(closest_tag['size'])
            if closest_tag['size'] >= 10000:
                go_forward = False
            elif self.duckie: 
                go_forward = False
            else:
                go_forward = True
                
        if go_forward:
            v = 1
            print('forward')
        else:
            print('no movement')

        car_control_msg.v = v
        car_control_msg.omega = omega
        self.pub_car_cmd.publish(car_control_msg)


if __name__ == '__main__':
    rospy.init_node('apriltag_detector',anonymous=False)
    apriltag_detector_node = TagDetectionNode()
    rospy.on_shutdown(apriltag_detector_node.onShutdown)
    rospy.spin()
