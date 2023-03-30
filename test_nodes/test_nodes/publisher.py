import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

from std_msgs.msg import String


class VelocityPublisher(Node):

    def __init__(self):
        super().__init__('set_velocity')
        #create publisher
        self.publisher = self.create_publisher(
            Twist,      #type
            '/cmd_vel', #topic
             10         #quality
        )
        timer_period = 0.1  # seconds
        #send command every timer_period seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = Twist()
        msg.linear.x=0.1
        self.publisher.publish(msg)
        self.get_logger().info('Publishing')


def main(args=None):
    rclpy.init(args=args)
    #make new publisher object
    vel_publisher = VelocityPublisher()
    #keep node alive
    rclpy.spin(vel_publisher)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    vel_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()