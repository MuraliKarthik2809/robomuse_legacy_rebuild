#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
from math import copysign

class CmdVelPub:
    def __init__(self):
        # Initialize the node
        rospy.init_node('cmd_vel_pub', anonymous=True)

        # Robot-specific parameters
        self.BASE_WIDTH = 0.30  # Distance between wheels in meters
        self.WHEEL_RADIUS = 0.125  # Radius of wheels in meters
        self.TICKS_PER_METER = 1530  # Ticks per meter traveled 

        # Max speed limits 
        self.MAX_ABS_LINEAR_SPEED = 1.0  # m/s
        self.MAX_ABS_ANGULAR_SPEED = 1.0  # rad/s

        # ROS publishers
        self.left_pub = rospy.Publisher('left_motor_velocity', Int32, queue_size=5)
        self.right_pub = rospy.Publisher('right_motor_velocity', Int32, queue_size=5)

        # ROS subscriber
        rospy.Subscriber('cmd_vel', Twist, self.cmd_vel_callback)

        # Lock to synchronize callback
        #self.lock = rospy.Lock()

    def cmd_vel_callback(self, twist):
        #with self.lock:
            linear_x = twist.linear.x  # Forward/Backward velocity
            angular_z = twist.angular.z  # Rotational velocity

            # Apply maximum speed limits
            if abs(linear_x) > self.MAX_ABS_LINEAR_SPEED:
                linear_x = copysign(self.MAX_ABS_LINEAR_SPEED, linear_x)
            if abs(angular_z) > self.MAX_ABS_ANGULAR_SPEED:
                angular_z = copysign(self.MAX_ABS_ANGULAR_SPEED, angular_z)

            # Compute wheel velocities (linear velocity and angular velocity)
            vr = linear_x - angular_z * self.BASE_WIDTH / 2.0  # Right wheel velocity in m/s
            vl = linear_x + angular_z * self.BASE_WIDTH / 2.0  # Left wheel velocity in m/s

            # Convert to ticks per second (for motor control)
            vr_ticks = int(vr * self.TICKS_PER_METER)  # Right wheel ticks/s
            vl_ticks = int(vl * self.TICKS_PER_METER)  # Left wheel ticks/s

            # Publish wheel speeds
            self.left_pub.publish(vl_ticks)
            self.right_pub.publish(vr_ticks)

            rospy.logdebug("vr_ticks: %d, vl_ticks: %d", vr_ticks, vl_ticks)

    def run(self):
        rospy.spin()

if __name__ == '__main__':
    try:
        cmd_vel_pub = CmdVelPub()
        cmd_vel_pub.run()
    except rospy.ROSInterruptException:
        pass

