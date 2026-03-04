import rospy
from std_msgs.msg import Int32

def encoder_callback(msg):
    rospy.loginfo("Received Encoder Value: %d", msg.data)

def encoder_listener():
    rospy.init_node('encoder_listener', anonymous=True)
    rospy.Subscriber("encoder", Int32, encoder_callback)
    rospy.spin()

if __name__ == '__main__':
    encoder_listener()
