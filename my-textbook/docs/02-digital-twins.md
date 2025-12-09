---
title: "Module 2: Digital Twin (Gazebo & Unity)"
sidebar_position: 2
---

# Module 2: Digital Twin (Gazebo & Unity)

Welcome to the Digital Twin module! In this module, you'll learn how to create high-fidelity simulations for humanoid robots using Gazebo and Unity. Digital twins are virtual replicas of physical systems that allow us to test robot behaviors in a safe environment before deployment.

## Learning Objectives

By the end of this module, you will be able to:
- Understand the principles of digital twin technology for robotics
- Set up physics simulation with gravity, collisions, and realistic environments
- Create high-fidelity simulations in Unity for humanoid robots
- Implement sensor simulation for LiDAR, Depth, and IMU sensors
- Connect your simulated robot to ROS 2 for testing

## Prerequisites

- Completion of Module 1 (ROS 2 basics)
- Basic understanding of 3D modeling concepts
- Familiarity with physics principles (gravity, collisions)

## Table of Contents

1. [Introduction to Digital Twins](#introduction-to-digital-twins)
2. [Physics Simulation Fundamentals](#physics-simulation-fundamentals)
3. [Gazebo Simulation Environment](#gazebo-simulation-environment)
4. [Unity Robotics Setup](#unity-robotics-setup)
5. [Sensor Simulation](#sensor-simulation)
6. [Connecting to ROS 2](#connecting-to-ros-2)
7. [Testing Robot Behaviors](#testing-robot-behaviors)

## Introduction to Digital Twins

A digital twin is a virtual representation of a physical system that mirrors its characteristics, behaviors, and performance in real-time. In robotics, digital twins allow us to:

- Test algorithms safely without risk to hardware
- Validate control systems before deployment
- Train AI models on synthetic data
- Optimize robot designs virtually

### Benefits of Digital Twins

- **Safety**: Test dangerous maneuvers without physical risk
- **Cost-Effective**: Reduce hardware wear and tear
- **Repeatability**: Conduct identical experiments multiple times
- **Speed**: Accelerate development cycles

## Physics Simulation Fundamentals

Realistic physics simulation is crucial for accurate digital twins. The simulation must account for:

- Gravity and its effects on robot stability
- Collision detection and response
- Friction and surface interactions
- Mass distribution and inertial properties

### Key Physics Parameters

```yaml
physics_engine: "ODE"  # Open Dynamics Engine
gravity: [0, 0, -9.81]  # Standard Earth gravity in m/s^2
collision_detection: "Bullet"  # Algorithm for collision detection
solver_iterations: 50  # Higher values = more accurate but slower
```

## Gazebo Simulation Environment

Gazebo is a powerful 3D simulation environment that provides realistic physics, high-quality graphics, and convenient programmatic interfaces.

### Setting Up a Basic World

```xml
<?xml version="1.0"?>
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Set gravity -->
    <gravity>0 0 -9.81</gravity>

    <!-- Include default plugins -->
    <plugin filename="libgazebo_ros_init.so" name="gazebo_ros_init">
      <ros>
        <namespace>/gazebo</namespace>
      </ros>
    </plugin>

    <!-- Ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Lighting -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Your humanoid robot model -->
    <include>
      <name>my_humanoid</name>
      <uri>model://my_humanoid_robot</uri>
      <pose>0 0 1 0 0 0</pose>
    </include>
  </world>
</sdf>
```

### Creating a Robot Model

A robot model in Gazebo consists of links (rigid bodies) connected by joints:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base link -->
  <link name="base_link">
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0"/>
      <inertia ixx="0.4" ixy="0" ixz="0" iyy="0.4" iyz="0" izz="0.2"/>
    </inertial>

    <visual>
      <origin xyz="0 0 0"/>
      <geometry>
        <capsule length="0.5" radius="0.15"/>
      </geometry>
    </visual>

    <collision>
      <origin xyz="0 0 0"/>
      <geometry>
        <capsule length="0.5" radius="0.15"/>
      </geometry>
    </collision>
  </link>

  <!-- Hip joint connecting to torso -->
  <joint name="hip_joint" type="revolute">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.3"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  </joint>

  <!-- Torso link -->
  <link name="torso">
    <inertial>
      <mass value="8.0"/>
      <origin xyz="0 0 0.3"/>
      <inertia ixx="0.3" ixy="0" ixz="0" iyy="0.3" iyz="0" izz="0.1"/>
    </inertial>

    <visual>
      <origin xyz="0 0 0.3"/>
      <geometry>
        <capsule length="0.6" radius="0.12"/>
      </geometry>
    </visual>

    <collision>
      <origin xyz="0 0 0.3"/>
      <geometry>
        <capsule length="0.6" radius="0.12"/>
      </geometry>
    </collision>
  </link>
</robot>
```

## Unity Robotics Setup

Unity provides a high-fidelity 3D environment with realistic rendering capabilities, making it ideal for creating photorealistic simulations.

### Installing Unity Robotics

1. Download and install Unity Hub
2. Install Unity version 2021.3 LTS or later
3. Create a new 3D project
4. Install the Unity Robotics Hub package
5. Install ML-Agents for AI training

### Basic Robot Setup in Unity

```csharp
using UnityEngine;
using Unity.Robotics.Core;
using Unity.Robotics.ROSTCPConnector;

public class HumanoidController : MonoBehaviour
{
    public ArticulationBody[] joints;
    public float torqueLimit = 100f;

    void Start()
    {
        // Initialize ROS connection
        var ros = ROSConnection.GetOrCreateInstance();
        ros.RegisterPublisher<Float32MultiArrayMsg>("joint_commands");
    }

    void FixedUpdate()
    {
        // Send joint positions to ROS
        var jointPositions = new float[joints.Length];
        for(int i = 0; i < joints.Length; i++)
        {
            jointPositions[i] = joints[i].jointPosition.x;
        }

        var msg = new Float32MultiArrayMsg();
        msg.data = jointPositions.ToList();

        ROSConnection.GetOrCreateInstance().Publish("joint_states", msg);
    }
}
```

## Sensor Simulation

Digital twins must accurately simulate the robot's sensory capabilities to be useful for testing perception algorithms.

### LiDAR Simulation

LiDAR sensors provide 360-degree distance measurements:

```xml
<sensor name="lidar_front" type="ray">
  <ray>
    <scan>
      <horizontal>
        <samples>720</samples>
        <resolution>1</resolution>
        <min_angle>-3.14159</min_angle>
        <max_angle>3.14159</max_angle>
      </horizontal>
    </scan>
    <range>
      <min>0.1</min>
      <max>30.0</max>
      <resolution>0.01</resolution>
    </range>
  </ray>
  <always_on>true</always_on>
  <update_rate>10</update_rate>
  <visualize>true</visualize>
  <plugin name="lidar_controller" filename="libgazebo_ros_ray_sensor.so">
    <ros>
      <namespace>/lidar</namespace>
      <remapping>~/out:=scan</remapping>
    </ros>
    <output_type>sensor_msgs/LaserScan</output_type>
  </plugin>
</sensor>
```

### Depth Camera Simulation

Depth cameras provide 3D point cloud data:

```xml
<sensor name="depth_camera" type="depth">
  <camera>
    <horizontal_fov>1.047</horizontal_fov>
    <image>
      <width>640</width>
      <height>480</height>
      <format>R8G8B8</format>
    </image>
    <clip>
      <near>0.1</near>
      <far>10</far>
    </clip>
  </camera>
  <always_on>true</always_on>
  <update_rate>30</update_rate>
  <visualize>true</visualize>
  <plugin name="camera_controller" filename="libgazebo_ros_openni_kinect.so">
    <baseline>0.2</baseline>
    <distortion_k1>0.0</distortion_k1>
    <distortion_k2>0.0</distortion_k2>
    <distortion_k3>0.0</distortion_k3>
    <distortion_t1>0.0</distortion_t1>
    <distortion_t2>0.0</distortion_t2>
    <point_cloud_cutoff>0.1</point_cloud_cutoff>
    <frame_name>camera_depth_optical_frame</frame_name>
  </plugin>
</sensor>
```

### IMU Simulation

IMU sensors provide orientation and acceleration data:

```xml
<sensor name="imu_sensor" type="imu">
  <always_on>true</always_on>
  <update_rate>100</update_rate>
  <visualize>false</visualize>
  <imu>
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
        </noise>
      </z>
    </angular_velocity>
    <linear_acceleration>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>1.7e-2</stddev>
        </noise>
      </z>
    </linear_acceleration>
  </imu>
</sensor>
```

## Connecting to ROS 2

The simulation must communicate with ROS 2 nodes to be useful for testing:

### Gazebo-ROS 2 Bridge

```bash
# Launch the robot in Gazebo with ROS 2 bridge
ros2 launch my_robot_gazebo my_robot_world.launch.py
```

### Unity-ROS 2 Connection

Unity can connect to ROS 2 using the TCP connector:

```python
# Python script to connect Unity to ROS 2
import rospy
from sensor_msgs.msg import LaserScan, Image, Imu
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist

def lidar_callback(data):
    # Process LiDAR data from Unity simulation
    print(f"Lidar ranges: {len(data.ranges)} points")

def camera_callback(data):
    # Process camera data from Unity simulation
    print(f"Received image: {data.width}x{data.height}")

def imu_callback(data):
    # Process IMU data from Unity simulation
    print(f"Orientation: {data.orientation}")

# Subscribe to sensor data
rospy.Subscriber('/unity/lidar_scan', LaserScan, lidar_callback)
rospy.Subscriber('/unity/camera/image_raw', Image, camera_callback)
rospy.Subscriber('/unity/imu', Imu, imu_callback)
```

## Testing Robot Behaviors

Once your digital twin is set up, you can test various robot behaviors:

1. **Locomotion**: Walking, running, climbing stairs
2. **Manipulation**: Grasping objects, opening doors
3. **Navigation**: Path planning, obstacle avoidance
4. **Interaction**: Human-robot interaction scenarios

### Example: Testing Balance Control

```python
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu
from geometry_msgs.msg import Twist

class BalanceTester(Node):
    def __init__(self):
        super().__init__('balance_tester')
        self.imu_sub = self.create_subscription(Imu, '/robot/imu', self.imu_callback, 10)
        self.cmd_pub = self.create_publisher(Twist, '/robot/cmd_vel', 10)

        self.balance_threshold = 0.1  # Radians

    def imu_callback(self, msg):
        roll, pitch, yaw = self.quaternion_to_euler(msg.orientation)

        if abs(pitch) > self.balance_threshold:
            # Send corrective command
            cmd = Twist()
            cmd.angular.y = -pitch * 2.0  # Proportional control
            self.cmd_pub.publish(cmd)

def main():
    rclpy.init()
    tester = BalanceTester()
    rclpy.spin(tester)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Summary

In this module, you've learned:
- How to create realistic digital twins using Gazebo and Unity
- Essential physics simulation concepts for robotics
- How to simulate various sensors (LiDAR, camera, IMU)
- How to connect simulations to ROS 2 for testing

Digital twins are invaluable tools that accelerate robot development while reducing risks and costs.

## Next Steps

In the next module, we'll explore AI-powered perception and navigation systems using NVIDIA Isaac, building on the simulation foundation established here.

---

## APA Citations

- Quigley, M., et al. (2009). ROS: an open-source Robot Operating System. *ICRA Workshop on Open Source Software*, 3(3.2), 5.
- NVIDIA Corporation. (2023). *NVIDIA Isaac Sim User Guide*. https://docs.omniverse.nvidia.com/isaacsim/latest/isaacsim.html
- Open Robotics. (2023). *Gazebo Documentation*. https://gazebosim.org/docs/