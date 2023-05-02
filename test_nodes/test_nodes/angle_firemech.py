import rclpy
from rclpy.node import Node

from std_msgs.msg import Float64
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Tilt = 13 #GPIO pin 13 voor de tilt servo
GPIO.setup(Tilt, GPIO.OUT) #Als output zetten
servoTilt_pwm = GPIO.PWM(Tilt, 50) #servo frequency van 50Hz
servoTilt_pwm.start(7.5) #start positie van servo in het midden bij het opstarten

class SubscriberAngle(Node):

    def __init__(self):
        super().__init__('anglemech_subscriber')
        self.subscription = self.create_subscription(Float64, '/enemy_distance',
                self.listener_callback, 10)
        self.subscription  #prevent unused variable warning

    def listener_callback(self, msg):
        angle = 7.5 + float(msg.data)/10
        servoTilt_pwm.ChangeDutyCycle(angle)
        time.sleep(0.5)
            
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    anglemech_subscriber = SubscriberAngle()

    rclpy.spin(anglemech_subscriber)

    anglemech_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
