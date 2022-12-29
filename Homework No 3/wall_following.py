#!/usr/bin/env python
import rospy # Python library for ROS
from sensor_msgs.msg import LaserScan # LaserScan type message is defined in sensor_msgs
from geometry_msgs.msg import Twist #
from numpy import radians, pi

def callback(dt):
    l=len(dt.ranges)
    
    print('-------------------------------------------')
    print('Range data at 0 deg:   {}'.format(dt.ranges[0]))
    print('Range data at cc deg:  {}'.format(dt.ranges[20]))
    print('Range data at c deg: {}'.format(dt.ranges[-20]))
    print( '-------------------------------------------')
    print(len(dt.ranges))
    print(l)
    thr1 = 0.5 # Laser scan forward range threshold
    thr2 = 0.8
    thr3 = 0.4
    if dt.ranges[0]>thr1 and dt.ranges[20]>thr2 and dt.ranges[l-20]>thr2: # Checks if there are obstacles in front and
                                                                        # 20 degrees left and right 
        move.linear.x = 0.2 # go forward (linear velocity)
        move.angular.z = 0.0 #no angular velocity
    elif dt.ranges[0]<thr1 and dt.ranges[30]>thr2 and dt.ranges[l-30]<thr2: #Checks if the obstacles in front and clockwise direction are closer than threshold limit
        move.linear.x = 0.0 # stop
        move.angular.z = 0.2 # rotate counter clockwise(angular velocity)
        if dt.ranges[0]>thr1 and dt.ranges[20]>thr2 and dt.ranges[l-20]>thr2: # Checks if there are obstacles in front and both sides
            move.linear.x = 0.2 # go forward (linear velocity)
            move.angular.z = 0.0
        
    elif dt.ranges[0]<thr1 and dt.ranges[30]<thr2 and dt.ranges[l-30]>thr2: # Checks if the obstacles in front and counter clockwise direction are closer than threshold limit
        move.linear.x = 0.0 # go forward (linear velocity)
        move.angular.z = -0.2
        if dt.ranges[0]>thr1 and dt.ranges[20]>thr2 and dt.ranges[l-20]>thr2: # Checks if there are obstacles in front and both side
            move.linear.x = 0.2 # go forward (linear velocity)
            move.angular.z = 0.0
    elif dt.ranges[0]<thr1 and dt.ranges[30]<thr2 and dt.ranges[l-30]<thr2: # Checks if the obstacles in front counter clockwise and clockwise direction are closer than threshold limit
        move.linear.x = -0.1 # go backward (linear velocity)
        move.angular.z = 0.3
        if dt.ranges[0]>thr1 and dt.ranges[20]>thr2 and dt.ranges[l-20]>thr2: # Checks if there are obstacles in front and both sides
            move.linear.x = 0.2 # go forward (linear velocity)
            move.angular.z = 0.0
    
    elif dt.ranges[0]>thr1 and dt.ranges[30]>thr3 and dt.ranges[l-30]<thr3: # Checks if the obstacles in  clockwise direction are closer than threshold limit
        move.linear.x = 0.0 # stop
        move.angular.z = 0.1 # rotate counter clockwise(angular velocity)
        if dt.ranges[0]>thr1 and dt.ranges[20]>thr2 and dt.ranges[l-20]>thr2: 
            move.linear.x = 0.2 # go forward (linear velocity)
            move.angular.z = 0.0
        
    elif dt.ranges[0]>thr1 and dt.ranges[30]<thr3 and dt.ranges[l-30]>thr3:
        move.linear.x = 0.0 # stop
        move.angular.z = -0.2 #rotate clockwise
        if dt.ranges[0]>thr1 and dt.ranges[20]>thr2 and dt.ranges[l-20]>thr2: 
            move.linear.x = 0.2 # go forward (linear velocity)
            move.angular.z = 0.0
    elif dt.ranges[0]>thr1 and dt.ranges[30]<thr3 and dt.ranges[l-30]<thr3:
        move.linear.x = 0.0 # stop
        move.angular.z = 0.5 #rotate 
        if dt.ranges[0]>thr1 and dt.ranges[20]>thr2 and dt.ranges[l-20]>thr2: 
            move.linear.x = 0.2 # go forward (linear velocity)
            move.angular.z = 0.0
       
          

        
    pub.publish(move) # publish the move object


move = Twist() # Creates a Twist message type object
rospy.init_node('obstacle_avoidance_node') # Initializes a node
pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)  # Publisher object which will publish "Twist" type messages
                            				 # on the "/cmd_vel" Topic, "queue_size" is the size of the
                                                         # outgoing message queue used for asynchronous publishing

sub = rospy.Subscriber("/scan", LaserScan, callback)  # Subscriber object which will listen "LaserScan" type messages
                                                      # from the "/scan" Topic and call the "callback" function
						      # each time it reads something from the Topic

rospy.spin() # Loops infinitely until someone stops the program execution
