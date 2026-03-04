#!/usr/bin/env python3

# cmd_vel_to_motor.py
import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

def cmd_vel_callback(msg):
    linear_x = msg.linear.x  # Forward/Backward velocity
    angular_z = msg.angular.z  # Rotational velocity

    # Robot-specific parameters (adjust based on your setup)
    wheel_base = 0.3  # Distance between wheels in meters
    wheel_radius = 0.125  # Radius of wheels in meters

    # Compute individual wheel velocities
    left_velocity = (linear_x - (angular_z * wheel_base / 2)) / wheel_radius
    right_velocity = (linear_x + (angular_z * wheel_base / 2)) / wheel_radius

    # Scale to your motor range
    left_motor = int(left_velocity * 100)  # Assuming motor accepts 0-100 range
    right_motor = int(right_velocity * 100)

    # Publish motor velocities
    left_pub.publish(left_motor)
    right_pub.publish(right_motor)

rospy.init_node('cmd_vel_to_motor', anonymous=True)

left_pub = rospy.Publisher('left_motor_velocity', Int32, queue_size=5)
right_pub = rospy.Publisher('right_motor_velocity', Int32, queue_size=5)

rospy.Subscriber('cmd_vel', Twist, cmd_vel_callback)

rospy.spin()

