import cv2
import apriltag
import pyautogui
import numpy
import time

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
    print("Duckie in image ratio:", result)
    return result


screenWidth, screenHeight = pyautogui.size()
screen_size = (screenWidth, screenHeight)
print(screen_size)

started = False
end = True

while True: #keep generating new image from Duckiebot's camera until shutdown
    im1 = pyautogui.screenshot(region=(50,600, 1000, 500))
    image_cv = cv2.cvtColor(numpy.array(im1), cv2.COLOR_RGB2BGR)
    #cv2.imshow('test',image_cv)

    #yellow object duckie detection
    duckie_here = False
    det_ratio = duckie_detection(image_cv)
    if det_ratio >= 1.0:
        duckie_here = True
        print('Duckie in sight')
    #apriltag detection:
    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    detector = apriltag.Detector()
    result = detector.detect(gray)

    color = (0, 0, 255)
    thickness = 2
    tag_list = []
    for det in result:
        start_point = (int(det.corners[1][0]), int(det.corners[1][1]))
        end_point = (int(det.corners[3][0]),int(det.corners[3][1]))
        rect_size = abs((start_point[0] - end_point[0])*(start_point[1] - end_point[1]))
        tag = {'size': rect_size, 'center': det.center}
        tag_list.append(tag)
        
        image = cv2.rectangle(image_cv, start_point, end_point, color, thickness)

    tag_list = sorted(tag_list, key= lambda i: i['size'])
    #print(len(tag_list))
    

    if len(tag_list) == 0:
        go_forward = False
    else:
        started = True
        closest_tag = tag_list[-1]
        print(closest_tag['size'])
        if closest_tag['size'] >= 6000:
            go_forward = False
        elif duckie_here:
            go_forward = False
        else:
            go_forward = True
            print(tag_list[-1])

    if go_forward:
        pyautogui.click(1746,50) 
        pyautogui.keyDown('up') 
        time.sleep(0.1)
        pyautogui.keyUp('up')
        print('forward')
        #for performing lane following:
        # if not started:
        #     pyautogui.click(1746,50) 
        #     pyautogui.keyDown('up') 
        #     time.sleep(0.1)
        #     pyautogui.keyUp('up')
        #     print('start lane following')
        started = True
        end = False
    else:
        #lane following 
        # if not end:
        #     pyautogui.click(1746,50) 
        #     pyautogui.keyDown('s') 
        #     time.sleep(0.1)
        #     pyautogui.keyUp('s') #stop lane following
        #     print('stop lane following')

        print('no movement')
        started = False
        end = True

    cv2.imshow('color', image) 

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()