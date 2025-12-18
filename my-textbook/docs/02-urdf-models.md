---
title: "Module 2: URDF Models for Humanoid Robots"
sidebar_position: 2
---

# Module 2: URDF Models for Humanoid Robots

Welcome to the URDF Models module! In this module, you'll learn how to create and work with Unified Robot Description Format (URDF) models for humanoid robots. URDF is essential for describing robot geometry, kinematics, and dynamics in ROS-based systems.

## Learning Objectives

By the end of this module, you will be able to:
- Understand the structure and components of URDF files
- Create kinematic chains for humanoid robots
- Define physical properties and inertial parameters
- Visualize and validate URDF models
- Integrate URDF models with simulation environments

## Prerequisites

- Completion of Module 1 (ROS 2 basics)
- Basic understanding of 3D geometry and coordinate systems
- Familiarity with XML syntax

## Table of Contents

1. [Introduction to URDF](#introduction-to-urdf)
2. [URDF Structure and Components](#urdf-structure-and-components)
3. [Links: Robot Body Parts](#links-robot-body-parts)
4. [Joints: Connecting Robot Parts](#joints-connecting-robot-parts)
5. [Materials and Visual Properties](#materials-and-visual-properties)
6. [Inertial Properties](#inertial-properties)
7. [Transmissions and Actuators](#transmissions-and-actuators)
8. [Gazebo-Specific Extensions](#gazebo-specific-extensions)
9. [Validating URDF Models](#validating-urdf-models)

## Introduction to URDF

URDF (Unified Robot Description Format) is an XML-based format used to describe robot models in ROS. It defines the physical and visual properties of a robot, including its links, joints, and kinematic chains.

### Key Concepts

- **Links**: Rigid bodies that make up the robot
- **Joints**: Connections between links that allow motion
- **Kinematic chains**: Sequences of links and joints that form robot limbs
- **Collision models**: Geometric representations for collision detection
- **Visual models**: Geometric representations for visualization

### Why URDF Matters

URDF is crucial for:
- Robot simulation in Gazebo and other environments
- Robot visualization in RViz
- Kinematic analysis and inverse kinematics
- Motion planning and control
- Robot calibration and parameterization

## URDF Structure and Components

A basic URDF file follows this structure:

```xml
<?xml version="1.0"?>
<robot name="my_robot">
  <!-- Links definition -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </visual>
    <collision>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </collision>
  </link>

  <!-- Joint definition -->
  <joint name="base_to_wheel" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_link"/>
    <origin xyz="0 0.25 0" rpy="0 0 0"/>
  </joint>

  <link name="wheel_link">
    <visual>
      <geometry>
        <cylinder radius="0.1" length="0.05"/>
      </geometry>
    </visual>
  </link>
</robot>
```

### Essential Elements

1. **Robot element**: The root element with the robot's name
2. **Link elements**: Define rigid bodies with visual and collision properties
3. **Joint elements**: Define connections between links with specific joint types
4. **Geometry elements**: Define shapes (box, cylinder, sphere, mesh)
5. **Origin elements**: Define positions and orientations using xyz and rpy

## Links: Robot Body Parts

Links represent the rigid bodies of your robot. Each link can have multiple properties:

### Visual Properties

```xml
<link name="torso">
  <visual>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <geometry>
      <capsule length="0.6" radius="0.12"/>
    </geometry>
    <material name="light_grey">
      <color rgba="0.7 0.7 0.7 1.0"/>
    </material>
  </visual>
</link>
```

### Collision Properties

```xml
<link name="torso">
  <collision>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <geometry>
      <capsule length="0.6" radius="0.12"/>
    </geometry>
  </collision>
</link>
```

### Inertial Properties

```xml
<link name="torso">
  <inertial>
    <mass value="8.0"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <inertia ixx="0.3" ixy="0" ixz="0" iyy="0.3" iyz="0" izz="0.1"/>
  </inertial>
</link>
</link>
```

## Joints: Connecting Robot Parts

Joints define how links connect and move relative to each other:

### Joint Types

- **revolute**: Rotational joint with limited range
- **continuous**: Rotational joint without limits
- **prismatic**: Linear sliding joint with limits
- **fixed**: No movement between links
- **floating**: 6-DOF movement (for base links)
- **planar**: Movement on a plane

### Joint Definition Example

```xml
<joint name="left_hip_yaw" type="revolute">
  <parent link="torso"/>
  <child link="left_thigh"/>
  <origin xyz="0 0.1 -0.1" rpy="0 0 0"/>
  <axis xyz="0 0 1"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  <dynamics damping="0.1" friction="0.0"/>
</joint>
```

## Materials and Visual Properties

Materials define the visual appearance of robot parts:

```xml
<material name="red">
  <color rgba="1 0 0 1"/>
</material>

<material name="blue">
  <color rgba="0 0 1 1"/>
</material>

<material name="white">
  <color rgba="1 1 1 1"/>
</material>

<link name="head">
  <visual>
    <geometry>
      <sphere radius="0.1"/>
    </geometry>
    <material name="white"/>
  </visual>
</link>
```

## Inertial Properties

Inertial properties are critical for physics simulation:

```xml
<link name="upper_arm">
  <inertial>
    <mass value="2.0"/>
    <origin xyz="0 0 0.1" rpy="0 0 0"/>
    <inertia ixx="0.01" ixy="0" ixz="0" iyy="0.01" iyz="0" izz="0.005"/>
  </inertial>
</link>
```

### Calculating Inertial Values

For common shapes:
- Box: `ixx = 1/12 * m * (h² + d²)`
- Cylinder: `ixx = 1/12 * m * (3*r² + h²)`
- Sphere: `ixx = 2/5 * m * r²`

## Transmissions and Actuators

Transmissions define how joints connect to actuators:

```xml
<transmission name="left_hip_yaw_trans">
  <type>transmission_interface/SimpleTransmission</type>
  <joint name="left_hip_yaw">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
  </joint>
  <actuator name="left_hip_yaw_motor">
    <hardwareInterface>hardware_interface/PositionJointInterface</hardwareInterface>
    <mechanicalReduction>1</mechanicalReduction>
  </actuator>
</transmission>
```

## Gazebo-Specific Extensions

Gazebo-specific elements for simulation:

```xml
<gazebo reference="head">
  <material>Gazebo/Blue</material>
  <turnGravityOff>false</turnGravityOff>
</gazebo>

<gazebo>
  <plugin name="robot_state_publisher" filename="libgazebo_ros_joint_state_publisher.so">
    <jointName>joint1, joint2</jointName>
  </plugin>
</gazebo>
```

## Validating URDF Models

### Tools for Validation

1. **check_urdf**: Check syntax and structure
   ```bash
   check_urdf /path/to/robot.urdf
   ```

2. **URDF Parser**: Validate with ROS tools
   ```bash
   roslaunch urdf_tutorial display.launch model:='$(find package)/urdf/robot.urdf'
   ```

### Common Validation Steps

1. Check XML syntax
2. Verify all links are connected
3. Ensure joint limits are reasonable
4. Validate inertial properties
5. Test visualization in RViz

## Creating a Humanoid Robot URDF

Let's create a simplified humanoid model:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="10.0"/>
      <origin xyz="0 0 0.25" rpy="0 0 0"/>
      <inertia ixx="0.4" ixy="0" ixz="0" iyy="0.4" iyz="0" izz="0.2"/>
    </inertial>
  </link>

  <!-- Torso -->
  <joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.5" rpy="0 0 0"/>
  </joint>

  <link name="torso">
    <visual>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <geometry>
        <capsule length="0.6" radius="0.12"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <geometry>
        <capsule length="0.6" radius="0.12"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="8.0"/>
      <origin xyz="0 0 0.3" rpy="0 0 0"/>
      <inertia ixx="0.3" ixy="0" ixz="0" iyy="0.3" iyz="0" izz="0.1"/>
    </inertial>
  </link>

  <!-- Head -->
  <joint name="torso_to_head" type="revolute">
    <parent link="torso"/>
    <child link="head"/>
    <origin xyz="0 0 0.6" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="10" velocity="1"/>
  </joint>

  <link name="head">
    <visual>
      <geometry>
        <sphere radius="0.15"/>
      </geometry>
      <material name="white">
        <color rgba="1 1 1 1"/>
      </material>
    </visual>
    <collision>
      <geometry>
        <sphere radius="0.15"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="2.0"/>
      <inertia ixx="0.018" ixy="0" ixz="0" iyy="0.018" iyz="0" izz="0.018"/>
    </inertial>
  </link>

  <!-- Left Arm -->
  <joint name="torso_to_left_shoulder" type="revolute">
    <parent link="torso"/>
    <child link="left_upper_arm"/>
    <origin xyz="0.2 0 0.4" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="50" velocity="1"/>
  </joint>

  <link name="left_upper_arm">
    <visual>
      <origin xyz="0 0 0.15" rpy="0 0 0"/>
      <geometry>
        <capsule length="0.3" radius="0.05"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.15" rpy="0 0 0"/>
      <geometry>
        <capsule length="0.3" radius="0.05"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.5"/>
      <origin xyz="0 0 0.15" rpy="0 0 0"/>
      <inertia ixx="0.005" ixy="0" ixz="0" iyy="0.005" iyz="0" izz="0.001"/>
    </inertial>
  </link>

  <joint name="left_shoulder_to_elbow" type="revolute">
    <parent link="left_upper_arm"/>
    <child link="left_lower_arm"/>
    <origin xyz="0 0 0.3" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="30" velocity="1"/>
  </joint>

  <link name="left_lower_arm">
    <visual>
      <origin xyz="0 0 0.12" rpy="0 0 0"/>
      <geometry>
        <capsule length="0.24" radius="0.04"/>
      </geometry>
      <material name="light_grey">
        <color rgba="0.7 0.7 0.7 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0.12" rpy="0 0 0"/>
      <geometry>
        <capsule length="0.24" radius="0.04"/>
      </geometry>
    </collision>
    <inertial>
      <mass value="1.0"/>
      <origin xyz="0 0 0.12" rpy="0 0 0"/>
      <inertia ixx="0.002" ixy="0" ixz="0" iyy="0.002" iyz="0" izz="0.0005"/>
    </inertial>
  </link>
</robot>
```

## Summary

In this module, you've learned:
- The structure and components of URDF files
- How to define links with visual, collision, and inertial properties
- Different joint types and how to connect robot parts
- How to add materials and visual properties
- How to define transmissions and Gazebo-specific extensions
- How to validate URDF models

These skills are essential for creating realistic humanoid robot models that can be used in simulation and real-world applications.

## Next Steps

In the next module, we'll explore Digital Twins, where you'll learn how to simulate these URDF models in virtual environments.

---

## APA Citations

- Open Robotics. (2023). *URDF Documentation*. https://wiki.ros.org/urdf
- Quigley, M., et al. (2009). ROS: an open-source Robot Operating System. *ICRA Workshop on Open Source Software*, 3(3.2), 5.
- Cousineau, E. A., & Safonova, A. (2012). Design and use paradigms for Gazebo, an open-source multi-robot simulator. *IEEE/RSJ International Conference on Intelligent Robots and Systems*, 1491-1498.