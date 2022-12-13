import rospy
import numpy as np
from sensor_msgs.msg import LaserScan
import matplotlib.pyplot as plt
import matplotlib as mplt
from nav_msgs.msg import Odometry
import tf.transformations as tf
#from math import sin, cos, pi, radians, arctan2, sqrt, matrix, degrees
from numpy import radians, arctan2, sqrt, matrix, degrees, sin, cos, pi
import threading

class motion:
    def __init__(self):
        self.lock = threading.Lock() 
        self.cur_pos=0
        sub = rospy.Subscriber('/scan', LaserScan, self.callback)
        subl = rospy.Subscriber ("/odom", Odometry, self.getAngle)
        self.once = True
        self.x =[]
        self.y =[]
        self.fx=[]
        self.fy=[]

    def callback(self, msg):
        self.lock.acquire()
        ranges = msg.ranges
        self.x =[]
        self.y =[] 
        self.fx=[] 
        self.fy=[] 
        if self.once:
            for i in range(len(ranges)):
                thetha_rad = radians(i)
                if ranges [i] == 'inf':
                    pass 
                else:
                    X = -ranges [i] * sin(thetha_rad)
                    Y = ranges [i] * cos(thetha_rad)
                    self.x.append(X)
                    self.y.append(Y)

            for j in range(len(ranges)):
                xr = ((self.x[j] * cos(self.cur_pos)) - (self.y[j] * sin(self.cur_pos)))
                yr = (self.x[j] * sin(self.cur_pos)) + (self.y[j] * cos(self.cur_pos))
                self.fx.append(xr)
                self.fy.append(yr)

        plt.clf()
        print(self.cur_pos)
        plt.scatter(0,0, marker = 'X', s=40,color='k')
        plt.scatter (self.fx, self.fy) 
        plt.pause (.1) 
        plt.show
        self.lock.release()

    def rotate_matrix (x, y, angle, x_shift=0, y_shift=0, units="DEGREES"):
        if units == "DEGREES":
            angle = radians(angle)
        xr = (x*cos(angle))-(y*sin(angle))
        yr = (x*sin(angle))+(y*cos(angle))

        return xr, yr

    def getAngle(self,msg):
        self.lock.acquire()
        cur_r = msg.pose.pose.orientation
        cur_pos1 = tf.euler_from_quaternion((cur_r.x, cur_r.y, cur_r.z, cur_r.w))
        self.cur_pos =cur_pos1[2]
        self.lock.release()

  
if __name__ == "__main__":
    rospy.init_node ('scan_values1')
    motion()
    rospy.spin()
