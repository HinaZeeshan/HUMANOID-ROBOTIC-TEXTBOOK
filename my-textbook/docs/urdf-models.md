 # Chapter 2: URDF Models for Humanoids
     
     ## 2.1 What is URDF?
     
     URDF (Unified Robot Description Format) is an XML format for representing a robot model. It specifies the robot's     
      kinematic and dynamic properties, visual appearance, and collision properties.
     
     ## 2.2 Core Concepts
    
 ### Links
    
   Links are the rigid bodies that make up the robot (e.g., torso, upper arm, forearm). Each link has mass, inertia, and 
      visual/collision properties.
    
    ### Joints
    
    Joints connect links and specify their relative motion (e.g., revolute, prismatic, fixed). Joints can have limits and 
      dynamics properties.
    
    ## 2.3 Creating a Simple URDF Model (Placeholder for Code Example)
    
    ```xml
 <?xml version="1.0"?>
<robot name="simple_arm">        

  <link name="base_link">        
    <visual>
      <geometry>
        <box size="0.1 0.1 0.1"/>
      </geometry>
      <material name="blue">     
        <color rgba="0 0 1 1"/>  
      </material>
    </visual>
  </link>

  <link name="link1">
    <visual>
      <geometry>
        <cylinder length="0.5" radius="0.05"/>
      </geometry>
      <material name="red">
        <color rgba="1 0 0 1"/>
      </material>
    </visual>
  </link>

  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0.05" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="-1.57" upper="1.57" effort="100" velocity="100"/>
  </joint>

</robot>
```
  
    
    ## 2.4 Visualizing URDF Models
    
    [Diagram: URDF Structure and Visualization]
  Example: Check URDF file for errors
  check_urdf my_robot.urdf

  Example: Display URDF model in RViz
  ros2 launch urdf_tutorial display.launch model:=my_robot.urdf

    
    ## 2.5 Further Reading
    
    *   [ROS URDF Tutorials](https://wiki.ros.org/urdf/Tutorials)
    *   [URDF XML Schema](http://wiki.ros.org/urdf/XML)