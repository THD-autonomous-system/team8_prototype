import rospy
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt
from math import sin, cos, pi

def lidar_callback(msg):
    global ranges, dis_forward
    ranges=msg.ranges
    map (ranges)
	
def map(ranges):
    x=[]
    y=[]
    for theta in range (len(ranges)):
        if ranges [theta] == "inf":
            pass
        else:
            rad = theta *pi/180
            x_new = -ranges [theta]*sin(rad)
            y_new = ranges [theta]*cos(rad)
            x.append(x_new)
            y.append(y_new)
    plt.clf()
    plt.scatter(x,y)
    plt.scatter(0,0, marker = 'X', s=40,color='k')
    plt.pause(.05)
    plt.show
    
	
rospy.init_node('map_detection')
sub = rospy.Subscriber('/scan', LaserScan, lidar_callback)
rospy.spin()
