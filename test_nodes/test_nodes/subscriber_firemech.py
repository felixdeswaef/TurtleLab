import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

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
    	if(msg.data == 'activeren'):
           GPIO.output(Motoren, 1)

        else if(msg.data == 'deactiveren'):
           GPIO.output(Motoren, 0)
           
        else: #voor als er iets zou misgaan met de messages
           GPIO.output(Motoren, 0)
        self.get_logger().info('I heard: "%s"' % msg.data)


def main(args=None):
    rclpy.init(args=args)

    Motor_subscriber = MinimalSubscriber()

    rclpy.spin(Motor_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    Motor_subscriber.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
