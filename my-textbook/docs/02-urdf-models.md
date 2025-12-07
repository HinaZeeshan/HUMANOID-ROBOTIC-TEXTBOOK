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
    
     1 <?xml version="1.0"?>
    2 <robot name="simple_arm">        
    3 
    4   <link name="base_link">        
    5     <visual>
    6       <geometry>
    7         <box size="0.1 0.1 0.1"/>
    8       </geometry>
    9       <material name="blue">     
   10         <color rgba="0 0 1 1"/>  
   11       </material>
   12     </visual>
   13   </link>
   14 
   15   <link name="link1">
   16     <visual>
   17       <geometry>
   18         <cylinder length="0.5" radius="0.05"/>
   19       </geometry>
   20       <material name="red">
   21         <color rgba="1 0 0 1"/>
   22       </material>
   23     </visual>
   24   </link>
   25 
   26   <joint name="joint1" type="revolute">
   27     <parent link="base_link"/>
   28     <child link="link1"/>
   29     <origin xyz="0 0 0.05" rpy="0 0 0"/>
   30     <axis xyz="0 0 1"/>
   31     <limit lower="-1.57" upper="1.57" effort="100" velocity="100"/>
   32   </joint>
   33 
   34 </robot>
  
    
    ## 2.4 Visualizing URDF Models
    
    [Diagram: URDF Structure and Visualization]
  Example: Check URDF file for errors
  check_urdf my_robot.urdf

  Example: Display URDF model in RViz
  ros2 launch urdf_tutorial display.launch model:=my_robot.urdf

    
    ## 2.5 Further Reading
    
    *   [ROS URDF Tutorials](https://wiki.ros.org/urdf/Tutorials)
    *   [URDF XML Schema](http://wiki.ros.org/urdf/XML)