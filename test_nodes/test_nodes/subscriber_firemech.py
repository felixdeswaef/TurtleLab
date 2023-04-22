import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Motoren = 23
Lader = 12
GPIO.setup(Motoren, GPIO.OUT)
GPIO.setup(Lader, GPIO.OUT)
servoLader_pwm = GPIO.PWM(Lader,50)
servoLader_pwm.start(2.5)

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(String, 'topic',
                self.listener_callback, 10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        if msg.data == 'activeren':
            #GPIO.output(Motoren, GPIO.HIGH)
            time.sleep(2)
            servoLader_pwm.ChangeDutyCycle(5)
            time.sleep(0.5)
            servoLader_pwm.ChangeDutyCycle(2.5)
        
        elif msg.data == 'deactiveren':
            GPIO.output(Motoren, GPIO.LOW)
            
        else: # voor als er iets zou misgaan met de messages
            GPIO.output(Motoren, GPIO.LOW)
            
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
