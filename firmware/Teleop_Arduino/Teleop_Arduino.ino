#include <Cytron_SmartDriveDuo.h>
#include <ros.h>
#include <std_msgs/Int32.h>
#include <geometry_msgs/Twist.h>

// Encoder pins
int encoder_left_A = 2;
int encoder_left_B = 3;
int encoder_right_A = 18;
int encoder_right_B = 19;

// Motor control pins
#define IN1 4
#define AN1 5
#define AN2 6
#define IN2 7

// Robot parameters
const float wheel_radius = 0.125;  // 12.5 cm radius
const float wheel_base = 0.3;    // 30 cm distance between wheels
const float encoder_ticks_per_rev = 1200;

// Global variables
volatile long totalPulsesLeft = 0;
volatile long totalPulsesRight = 0;

float leftMotorVelocity = 0;
float rightMotorVelocity = 0;

// Motor driver
Cytron_SmartDriveDuo smartDriveDuo30(PWM_INDEPENDENT, IN1, IN2, AN1, AN2);

// ROS node handle
ros::NodeHandle nh;

// ROS message objects
geometry_msgs::Twist cmd_vel_msg;
std_msgs::Int32 leftEncoderROS;
std_msgs::Int32 rightEncoderROS;

// ROS publishers and subscribers
ros::Publisher leftEncoderPublisher("left_encoder_pulses", &leftEncoderROS);
ros::Publisher rightEncoderPublisher("right_encoder_pulses", &rightEncoderROS);

// Function to handle velocity commands
void cmdVelCallback(const geometry_msgs::Twist& cmd_vel_msg) {
  // Extract linear and angular velocity from the Twist message
  float linear_velocity = cmd_vel_msg.linear.x;  // m/s
  float angular_velocity = cmd_vel_msg.angular.z; // rad/s

  // Calculate wheel velocities in rad/s
  float leftMotorVelocity = (linear_velocity + angular_velocity * wheel_base / 2.0) / wheel_radius; // Adjusted for inverted forward
  float rightMotorVelocity = (linear_velocity - angular_velocity * wheel_base / 2.0) / wheel_radius; // Adjusted for inverted forward

  // Correct motor direction
  int pwmLeft = constrain(leftMotorVelocity, -100, 100);    // Removed inversion for the left motor
  int pwmRight = constrain(rightMotorVelocity * -1, -100, 100); // Inverted for the right motor

  // Send PWM values to motor driver
  smartDriveDuo30.control(pwmLeft, pwmRight);
}

ros::Subscriber<geometry_msgs::Twist> cmdVelSubscriber("cmd_vel", &cmdVelCallback);

void setup() {
  // Initialize encoder pins
  pinMode(encoder_left_A, INPUT_PULLUP);
  pinMode(encoder_left_B, INPUT_PULLUP);
  pinMode(encoder_right_A, INPUT_PULLUP);
  pinMode(encoder_right_B, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(encoder_left_A), encoder_left_A_Int, RISING);
  attachInterrupt(digitalPinToInterrupt(encoder_left_B), encoder_left_B_Int, RISING);
  attachInterrupt(digitalPinToInterrupt(encoder_right_A), encoder_right_A_Int, RISING);
  attachInterrupt(digitalPinToInterrupt(encoder_right_B), encoder_right_B_Int, RISING);

  // Initialize ROS
  nh.initNode();
  nh.advertise(leftEncoderPublisher);
  nh.advertise(rightEncoderPublisher);
  nh.subscribe(cmdVelSubscriber);
}

void loop() {
  nh.spinOnce();

  // Publish encoder pulses
  leftEncoderROS.data = totalPulsesLeft;
  rightEncoderROS.data = totalPulsesRight;
  leftEncoderPublisher.publish(&leftEncoderROS);
  rightEncoderPublisher.publish(&rightEncoderROS);

  delay(10);  // Small delay to avoid overloading
}


void encoder_left_A_Int() {
  // Check direction using encoder B pin
  if(digitalRead(encoder_left_B) == LOW) {
    totalPulsesLeft--; // Decrement if left B is low
  }  
}

void encoder_left_B_Int() {
  // Check direction using encoder A pin
  if(digitalRead(encoder_left_A) == LOW) {
    totalPulsesLeft++; // Increment if left A is low
  }  
}

void encoder_right_A_Int() {
  // Reverse the direction for the right encoder
  if(digitalRead(encoder_right_B) == LOW) {
    totalPulsesRight++; // Decrement if right B is low (reversed logic)
  }  
}

void encoder_right_B_Int() {
  // Reverse the direction for the right encoder
  if(digitalRead(encoder_right_A) == LOW) {
    totalPulsesRight--; // Increment if right A is low (reversed logic)
  }
}
