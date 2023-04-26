import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Tilt = 13 #GPIO pin 13 voor de tilt servo
GPIO.setup(Tilt, GPIO.OUT) #Als output zetten
servoTilt_pwm = GPIO.PWM(Tilt, 50) #servo frequency van 50Hz
servoTilt_pwm.start(7.5) #start positie van servo in het midden bij het opstarten

class Subscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(String, 'topic',
                self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        if msg.data == 'Distance':
            
            servoTilt_pwm.ChangeDutyCycle(10.5)
            time.sleep(0.5)
            servoTilt_pwm.ChangeDutyCycle(2)
            time.sleep(0.5)
            servoTilt_pwm.ChangeDutyCycle(10.5)
            
        else: #als er even niet geschoten moet worden dan mag de servo terug in zijn midden positie komen
            servoLader_pwm.ChangeDutyCycle(7.5)
            
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    AngleMech_subscriber = Subscriber()

    rclpy.spin(AngleMech_subscriber)

    AngleMech_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
