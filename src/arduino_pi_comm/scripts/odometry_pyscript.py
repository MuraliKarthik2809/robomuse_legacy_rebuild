#!/usr/bin/env python3

import rospy
import tf
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32
from tf.transformations import quaternion_from_euler
import math

class OdometryPublisher:
    def __init__(self):
        # Initialize the node
        rospy.init_node('odom_pub', anonymous=True)

        # ROS parameters
        self.ticks_per_meter = rospy.get_param("~ticks_per_meter", 1530)  # Ticks for one meter
        self.base_width = rospy.get_param("~base_width", 0.30)  # 30 cm (distance between wheels)

        # State variables
        self.left_ticks = 0
        self.right_ticks = 0
        self.prev_left_ticks = 0
        self.prev_right_ticks = 0
        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        # ROS publishers and subscribers
        self.odom_pub = rospy.Publisher('odom', Odometry, queue_size=10)
        rospy.Subscriber('left_motor_velocity', Int32, self.left_encoder_callback)
        rospy.Subscriber('right_motor_velocity', Int32, self.right_encoder_callback)
        self.odom_broadcaster = tf.TransformBroadcaster()

        # Control the rate of publishing
        self.rate = rospy.Rate(10)  # 10 Hz

    def left_encoder_callback(self, msg):
        self.left_ticks = self.handle_encoder_overflow(self.left_ticks, msg.data)

    def right_encoder_callback(self, msg):
        self.right_ticks = self.handle_encoder_overflow(self.right_ticks, msg.data)

    def handle_encoder_overflow(self, prev_ticks, current_ticks):
        # Overflow handling logic for encoders
        max_ticks = 2**15 - 1  # Assuming 16-bit encoder
        min_ticks = -2**15

        if current_ticks - prev_ticks > max_ticks:
            return current_ticks - max_ticks
        elif current_ticks - prev_ticks < min_ticks:
            return current_ticks + max_ticks
        else:
            return current_ticks

    def calculate_odometry(self):
        # Calculate the change in ticks
        delta_left = self.left_ticks - self.prev_left_ticks
        delta_right = self.right_ticks - self.prev_right_ticks

        self.prev_left_ticks = self.left_ticks
        self.prev_right_ticks = self.right_ticks

        # Calculate distance traveled
        left_distance = delta_left / self.ticks_per_meter  # Meters
        right_distance = delta_right / self.ticks_per_meter  # Meters

        # Average distance and change in orientation
        distance = (left_distance + right_distance) / 2
        delta_theta = (right_distance - left_distance) / self.base_width

        # Update robot pose
        self.x += distance * math.cos(self.theta)
        self.y += distance * math.sin(self.theta)
        self.theta += delta_theta
        self.theta = math.atan2(math.sin(self.theta), math.cos(self.theta))  # Normalize theta

    def publish_odometry(self):
    	self.odom_broadcaster.sendTransform((self.x, self.y, 0), quat, rospy.Time.now(), "base_link", "odom")
        odom_msg = Odometry()
        odom_msg.header.stamp = rospy.Time.now()
        odom_msg.header.frame_id = 'odom'
        odom_msg.child_frame_id = 'base_link'

        # Fill in the pose information
        odom_msg.pose.pose.position.x = self.x
        odom_msg.pose.pose.position.y = self.y
        odom_msg.pose.pose.position.z = 0

        quat = quaternion_from_euler(0, 0, self.theta)
        odom_msg.pose.pose.orientation.x = quat[0]
        odom_msg.pose.pose.orientation.y = quat[1]
        odom_msg.pose.pose.orientation.z = quat[2]
        odom_msg.pose.pose.orientation.w = quat[3]

        self.odom_pub.publish(odom_msg)

    def run(self):
        while not rospy.is_shutdown():
            self.calculate_odometry()
            self.publish_odometry()
            self.rate.sleep()


if __name__ == '__main__':
    try:
        odom_publisher = OdometryPublisher()
        odom_publisher.run()
    except rospy.ROSInterruptException:
        pass

