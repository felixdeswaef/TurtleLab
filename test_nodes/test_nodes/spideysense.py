import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Motoren = 23 #GPIO pin 23 voor de motoren
Lader = 12 #GPIO pin 12 voor de laad servo
GPIO.setup(Motoren, GPIO.OUT) #pin als output zetten
GPIO.setup(Lader, GPIO.OUT)
servoLader_pwm = GPIO.PWM(Lader, 50) #servo frequency van 50Hz
servoLader_pwm.start(7.5) #dit eventueel al op 10.5 zetten zodat dit niet meer in de lus hoeft gedaan te worden

class Subscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(String, '/camera_info',
                self.listener_callback, 10)
        self.subscription  # prevent unused variable warning
    
    def shoot():
        GPIO.output(Motoren, GPIO.HIGH)
        time.sleep(2) #timer van 2 seconden zodat de motoren op snelheid geraken
        servoLader_pwm.ChangeDutyCycle(10.5) #servo van de lader eerst naar achter trekken zodat een pijlje in de loop kan vallen
        time.sleep(0.5)
        servoLader_pwm.ChangeDutyCycle(2) #servo naar voor duwen zodat het pijltje afgeschoten wordt
        time.sleep(0.5)
        GPIO.output(Motoren, GPIO.LOW)
        servoLader_pwm.ChangeDutyCycle(10.5) #servo terug naar achter trekken zodat een volgend pijltje geladen wordt
            

    def listener_callback(self, msg):
        data=str(msg.data)
        data.split(";")
        hoek=float(data[1])
        if data[2]=="1" and 0.12>hoek>-0.12:
            self.shoot()

        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)

    FireMech_subscriber = Subscriber()

    rclpy.spin(FireMech_subscriber)

    FireMech_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
