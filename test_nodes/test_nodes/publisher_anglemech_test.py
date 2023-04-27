#publisher om het vuur mechanisme te al te kunnen testen

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
i = 0.2

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        
        msg.data += i;
        
        if (msg.data > 5):
            msg.data = 0
            
        self.publisher_.publish(msg)
          
        self.get_logger().info('Publishing: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
