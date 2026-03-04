#!/usr/bin/env python3

# odometry_publisher.py
import rospy
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32
from tf.transformations import quaternion_from_euler
import math

def left_encoder_callback(msg):
    global left_ticks
    left_ticks = msg.data

def right_encoder_callback(msg):
    global right_ticks
    right_ticks = msg.data

rospy.init_node('odometry_publisher')

rospy.Subscriber('left_encoder_pulses', Int32, left_encoder_callback)
rospy.Subscriber('right_encoder_pulses', Int32, right_encoder_callback)

odom_pub = rospy.Publisher('odom', Odometry, queue_size=10)

rate = rospy.Rate(10)  # 10 Hz

wheel_radius = 0.125  # 5 cm
ticks_per_revolution = 1200
base_width = 0.3  # 30 cm

left_ticks = 0
right_ticks = 0

x = 0.0
y = 0.0
theta = 0.0

prev_left_ticks = 0
prev_right_ticks = 0

while not rospy.is_shutdown():
    delta_left = left_ticks - prev_left_ticks
    delta_right = right_ticks - prev_right_ticks

    prev_left_ticks = left_ticks
    prev_right_ticks = right_ticks

    left_distance = (2 * math.pi * wheel_radius * delta_left) / ticks_per_revolution
    right_distance = (2 * math.pi * wheel_radius * delta_right) / ticks_per_revolution

    distance = (left_distance + right_distance) / 2
    delta_theta = (right_distance - left_distance) / base_width

    x += distance * math.cos(theta)
    y += distance * math.sin(theta)
    theta += delta_theta

    # Publish odometry message
    odom_msg = Odometry()
    odom_msg.header.stamp = rospy.Time.now()
    odom_msg.header.frame_id = 'odom'
    odom_msg.child_frame_id = 'base_link'

    odom_msg.pose.pose.position.x = x
    odom_msg.pose.pose.position.y = y
    odom_msg.pose.pose.position.z = 0

    quat = quaternion_from_euler(0, 0, theta)
    odom_msg.pose.pose.orientation.x = quat[0]
    odom_msg.pose.pose.orientation.y = quat[1]
    odom_msg.pose.pose.orientation.z = quat[2]
    odom_msg.pose.pose.orientation.w = quat[3]

    odom_pub.publish(odom_msg)

    rate.sleep()

