# Team 4: Uber For Duckies
Students: Cynthia Li, Shinny Sun

This is the Github repository for team 4's Robotics 1 final project. Our project
is related to automouns driving and Uber. We explore the idea of object detection,
lane following, and the mechanical/electrical for a duckie grabber. 

Scripts:
--------
- Robotics1_Duckie_Picker.ino: This is the script for remote controlling the duckie grabber. 
  - Execution: Upload this code to an Arduino Uno and run it from there
- apriltag_detection.py: This is the script for running object detectin for apriltag and duckie
  - Execution: 
  - Make sure the dts keyboard control GUI is up and being place on the top right corner of your screen, and rqt_image_view is up from the Duckiebot's ROS container.
  - Don't block the camera image with any application
  - Then run python apriltag_detection.py 

Special Note:
--------------
The tag_detector_node.py script is the ROS node we implemented for object detection. However, we are
not able to further develop and test it out due to our limited time constraint on the project. We uploaded here to help other understand what we try to achieve with ROS for our project. 
