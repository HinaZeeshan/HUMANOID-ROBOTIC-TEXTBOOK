  # Chapter 1: Introduction to ROS 2
     
     ## 1.1 What is ROS 2?
     
     ROS 2 (Robot Operating System 2) is an open-source framework for developing robot applications. It provides a structure      communication layer, tools, and libraries to help build complex robot systems.
     
     ## 1.2 Core Concepts
     
     ### Nodes
    
    Nodes are executable processes that perform computation. They communicate with other nodes using various communication 
      mechanisms.
    
    ### Topics
    
    Topics are named buses over which nodes exchange messages. Messages are data structures containing information (e.g.,  
      sensor readings, motor commands).
    
    ### Services
    
    Services are a request/reply communication mechanism. A service server node provides a service, and a client node sends      request and receives a reply.
    
    ### Actions
    
    Actions are used for long-running tasks with feedback. An action client sends a goal, receives continuous feedback, and      eventually a result.
    
    ## 1.3 Setting up ROS 2
    
    [Diagram: ROS 2 Architecture Overview]
    
   
    [Diagram: ROS 2 Architecture Overview]
   
    ## 1.4 Basic ROS 2 Commands
  Example: List active ROS 2 nodes
  ros2 node list

  Example: List available topics
  ros2 topic list

   1
  Example: List active ROS 2 nodes
  ros2 node list

  Example: List available topics
  ros2 topic list

   1
  Example: List available topics
  ros2 topic list

   

   
    ## 1.5 Your First ROS 2 Node (Placeholder for Code Example)
   
   1 # Minimal Publisher Node (Python)
    2 import rclpy
    3 from rclpy.node import Node
    4 from std_msgs.msg import String
    5 
    6 class MinimalPublisher(Node):
    7 
    8     def __init__(self):
    9         super().__init__('minimal_publisher')
   10         self.publisher_ = self.create_publisher(String, 'topic', 10)     
   11         timer_period = 0.5  # seconds
   12         self.timer = self.create_timer(timer_period, self.timer_callback)
   13         self.i = 0
   14 
   15     def timer_callback(self):
   16         msg = String()
   17         msg.data = 'Hello ROS 2: %d' % self.i
   18         self.publisher_.publish(msg)
   19         self.get_logger().info('Publishing: "%s"' % msg.data)
   20         self.i += 1
   21 
   22 def main(args=None):
   23     rclpy.init(args=args)
   24     minimal_publisher = MinimalPublisher()
   25     rclpy.spin(minimal_publisher)
   26     minimal_publisher.destroy_node()
   27     rclpy.shutdown()
   28 
   29 if __name__ == '__main__':
   30     main()

    1 # Minimal Subscriber Node (Python)
    2 import rclpy
    3 from rclpy.node import Node
    4 from std_msgs.msg import String
    5 
    6 class MinimalSubscriber(Node):
    7 
    8     def __init__(self):
    9         super().__init__('minimal_subscriber')
   10         self.subscription = self.create_subscription(       
   11             String,
   12             'topic',
   13             self.listener_callback,
   14             10)
   11             String,
   12             'topic',
   13             self.listener_callback,
   14             10)
   14             10)
   15         self.subscription  # prevent unused variable warning
   16
   17     def listener_callback(self, msg):
   18         self.get_logger().info('I heard: "%s"' % msg.data)
   19
   20 def main(args=None):
   21     rclpy.init(args=args)
   22     minimal_subscriber = MinimalSubscriber()
   16
   17     def listener_callback(self, msg):
   18         self.get_logger().info('I heard: "%s"' % msg.data)
   19
   20 def main(args=None):
   21     rclpy.init(args=args)
   22     minimal_subscriber = MinimalSubscriber()
   18         self.get_logger().info('I heard: "%s"' % msg.data)
   19
   20 def main(args=None):
   21     rclpy.init(args=args)
   22     minimal_subscriber = MinimalSubscriber()
   21     rclpy.init(args=args)
   22     minimal_subscriber = MinimalSubscriber()
   22     minimal_subscriber = MinimalSubscriber()
   23     rclpy.spin(minimal_subscriber)
   24     minimal_subscriber.destroy_node()
   25     rclpy.shutdown()
   26
   27 if __name__ == '__main__':
   28     main()
   
    ## 1.6 Further Reading
   
    *   [ROS 2 Documentation](https://docs.ros.org/en/galactic/index.html)
    *   [ROS 2 Tutorials](https://docs.ros.org/en/galactic/Tutorials.html)
