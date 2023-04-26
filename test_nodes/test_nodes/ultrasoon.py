import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import RPi.GPIO as GPIO
import time
from hcsr04sensor.sensor import Measurement

GPIO_MODE = GPIO.BCM
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG_PIN = 20
ECHO_PIN = 21

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.OUT)

class MinimalPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'Wall_Detect', 10)
        timer_period = 1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self):
        msg = String()
        distance =  Measurement(TRIG_PIN, ECHO_PIN, 20, "metric", GPIO_MODE) #in cm
        
        if (distace < 30):        
          msg.data = 'Muur'
          self.publisher_.publish(msg)
        else:
          msg.data = 'Dictance_ok'
          self.publisher_.publish(msg)
          
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.state = not self.state


def main(args=None):
    rclpy.init(args=args)

    minimal_publisher = MinimalPublisher()

    rclpy.spin(minimal_publisher)

    minimal_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
