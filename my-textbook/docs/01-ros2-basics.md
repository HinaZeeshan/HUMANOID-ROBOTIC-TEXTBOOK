---
title: "Module 1: Robotic Nervous System (ROS 2)"
sidebar_position: 1
---

# Module 1: Robotic Nervous System (ROS 2)

Welcome to the foundational module of our Humanoid Robotics Textbook! In this module, you'll learn about ROS 2 (Robot Operating System 2), which serves as the "nervous system" for robots, enabling different components to communicate and work together seamlessly.

## Learning Objectives

By the end of this module, you will be able to:
- Understand the core concepts of ROS 2 and its architecture
- Create and manage ROS 2 nodes for different robot components
- Implement communication between nodes using topics, services, and actions
- Bridge Python applications with ROS 2 using rclpy
- Explain URDF (Unified Robot Description Format) for humanoid robots

## Prerequisites

- Basic Python programming knowledge
- Understanding of object-oriented programming concepts
- Familiarity with command-line interfaces

## Table of Contents

1. [Introduction to ROS 2](#introduction-to-ros-2)
2. [Nodes: The Building Blocks](#nodes-the-building-blocks)
3. [Topics: Publish-Subscribe Communication](#topics-publish-subscribe-communication)
4. [Services: Request-Response Communication](#services-request-response-communication)
5. [Actions: Goal-Based Communication](#actions-goal-based-communication)
6. [Python-ROS Bridge with rclpy](#python-ros-bridge-with-rclpy)
7. [URDF for Humanoid Robots](#urdf-for-humanoid-robots)
8. [Putting It All Together](#putting-it-all-together)

## Introduction to ROS 2

ROS 2 (Robot Operating System 2) is not an actual operating system, but rather a flexible framework for writing robot software. It provides libraries, tools, and conventions that facilitate the creation of complex and robust robot behavior across a wide variety of robot platforms.

### Key Concepts

- **Nodes**: Processes that perform computation
- **Topics**: Named buses over which nodes exchange messages
- **Services**: Synchronous request/response communication
- **Actions**: Asynchronous goal-based communication with feedback
- **Messages**: Data structures used inside ROS for communication
- **Parameters**: Configuration values that nodes can access

### Why ROS 2?

ROS 2 improves upon the original ROS with:
- Real-time support
- Multi-robot systems
- Security features
- Better cross-platform support
- Improved middleware (DDS-based)

## Nodes: The Building Blocks

A node is an executable that uses ROS 2 to communicate with other nodes. Nodes are the fundamental building blocks of a ROS 2 system.

### Creating a Simple Node

Here's a basic ROS 2 node in Python:

```python
import rclpy
from rclpy.node import Node

class MinimalNode(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.get_logger().info('Minimal node created')

def main(args=None):
    rclpy.init(args=args)
    minimal_node = MinimalNode()

    try:
        rclpy.spin(minimal_node)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Node Lifecycle

1. **Initialization**: Node is created and registered with the ROS 2 master
2. **Execution**: Node runs and performs its tasks
3. **Shutdown**: Node is properly destroyed and unregistered

## Topics: Publish-Subscribe Communication

Topics enable asynchronous communication between nodes using a publish-subscribe pattern. Publishers send messages to topics, and subscribers receive messages from topics.

### Publisher Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = f'Hello World: {self.i}'
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()

    try:
        rclpy.spin(minimal_publisher)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_publisher.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Subscriber Example

```python
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info(f'I heard: "{msg.data}"')

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()

    try:
        rclpy.spin(minimal_subscriber)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_subscriber.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Services: Request-Response Communication

Services provide synchronous request-response communication between nodes. A service client sends a request to a service server, which processes the request and sends back a response.

### Service Server Example

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f'Incoming request\na={request.a}, b={request.b}')
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()

    try:
        rclpy.spin(minimal_service)
    except KeyboardInterrupt:
        pass
    finally:
        minimal_service.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

### Service Client Example

```python
from example_interfaces.srv import AddTwoInts
import rclpy
from rclpy.node import Node

class MinimalClient(Node):
    def __init__(self):
        super().__init__('minimal_client')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        self.future = self.cli.call_async(self.req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()

def main(args=None):
    rclpy.init(args=args)
    minimal_client = MinimalClient()
    response = minimal_client.send_request(1, 2)
    minimal_client.get_logger().info(f'Result of add_two_ints: {response.sum}')

    minimal_client.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

## Actions: Goal-Based Communication

Actions provide asynchronous communication for long-running tasks with feedback and status updates. They're ideal for navigation, manipulation, and other tasks that take time to complete.

## Python-ROS Bridge with rclpy

rclpy is the Python client library for ROS 2, providing Python APIs to interact with ROS 2 concepts.

### Installation and Setup

```bash
pip install rclpy
```

### Basic rclpy Usage

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node')
        self.get_logger().info('Node initialized')

def main():
    rclpy.init()
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
```

## URDF for Humanoid Robots

URDF (Unified Robot Description Format) is an XML format for representing a robot model. For humanoid robots, URDF describes the physical structure, joints, and kinematic properties.

### Basic URDF Structure

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base link -->
  <link name="base_link">
    <visual>
      <geometry>
        <box size="0.5 0.5 0.5"/>
      </geometry>
    </visual>
  </link>

  <!-- Torso -->
  <link name="torso">
    <visual>
      <geometry>
        <box size="0.3 0.3 0.6"/>
      </geometry>
    </visual>
  </link>

  <!-- Joint connecting base to torso -->
  <joint name="base_to_torso" type="fixed">
    <parent link="base_link"/>
    <child link="torso"/>
    <origin xyz="0 0 0.4"/>
  </joint>
</robot>
```

### Key URDF Elements for Humanoids

- **Links**: Rigid parts of the robot (head, torso, limbs)
- **Joints**: Connections between links (revolute, prismatic, fixed)
- **Materials**: Visual appearance properties
- **Transmissions**: How joints connect to actuators
- **Gazebo**: Simulation-specific extensions

## Putting It All Together

Now that you understand the core concepts of ROS 2, let's create a simple humanoid robot controller that demonstrates all these concepts working together:

1. A node that publishes sensor data (topics)
2. A node that responds to movement commands (services)
3. A node that performs complex movements (actions)
4. A URDF description of the humanoid robot

This foundational knowledge will serve as the basis for all subsequent modules in this textbook.

## Summary

In this module, you've learned:
- The core concepts of ROS 2 architecture
- How to create and manage nodes
- Different communication patterns (topics, services, actions)
- How to bridge Python with ROS 2 using rclpy
- How to describe humanoid robots using URDF

These concepts form the "nervous system" of a robot, enabling different components to communicate and work together effectively.

## Next Steps

In the next module, we'll explore Digital Twins, where you'll learn how to simulate these ROS 2 concepts in a virtual environment before deploying them on real robots.

---

## APA Citations

- Open Robotics. (2023). *ROS 2 Documentation*. https://docs.ros.org/en/humble/
- Quigley, M., Gerkey, B., & Smart, W. D. (2009). ROS: an open-source Robot Operating System. *ICRA Workshop on Open Source Software*, 3(3.2), 5.
- Macenski, S. (2022). *Professional ROS 2 Development*. Apress.