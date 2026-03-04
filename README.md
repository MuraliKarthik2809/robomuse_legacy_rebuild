# robomuse_legacy_rebuild

# Robomuse Legacy Rebuild (ROS1 Noetic)

Robomuse is a differential-drive mobile robot platform designed for SLAM and autonomous navigation using ROS.

This repository contains a rebuilt modular ROS1 stack for the Robomuse robot.

## Features

- Differential drive mobile robot
- RPLidar A2 integration
- SLAM (GMapping / Cartographer)
- Autonomous navigation (AMCL + move_base)
- Gazebo simulation
- Arduino motor control using rosserial
- Modular ROS architecture

## Repository Structure

firmware/  
Arduino motor control firmware.

robomuse_ws/src/  
ROS workspace containing robot packages.

docker/  
Docker environment for running ROS Noetic on newer operating systems.

docs/  
Project diagrams and documentation.

## System Architecture

Robot Hardware
- Arduino Mega
- Cytron SmartDriveDuo-30
- RPLidar A2

ROS Architecture
- arduino_pi_comm → hardware communication
- robomuse_bringup → robot bringup
- robomuse_description → URDF robot model
- robomuse_slam → SLAM
- robomuse_navigation → navigation stack
- robomuse_gazebo → simulation

## Installation

Install ROS Noetic.

Install dependencies:
sudo apt install ros-noetic-rplidar-ros
sudo apt install ros-noetic-rosserial
sudo apt install ros-noetic-rosserial-python
sudo apt install ros-noetic-navigation
sudo apt install ros-noetic-slam-gmapping
sudo apt install ros-noetic-cartographer


Clone repository:
git clone 
