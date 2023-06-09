import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
Motoren = 23  # GPIO pin 23 voor de motoren
Lader = 12  # GPIO pin 12 voor de laad servo
GPIO.setup(Motoren, GPIO.OUT)  # pin als output zetten
GPIO.setup(Lader, GPIO.OUT)
servoLader_pwm = GPIO.PWM(Lader, 50)  # servo frequency van 50Hz
servoLader_pwm.start(7.5)  # dit eventueel al op 10.5 zetten zodat dit niet meer in de lus hoeft gedaan te worden

class SubscriberFiremech(Node):

    def __init__(self):
        super().__init__('firemech_subscriber')
        self.teller = 4 #max 4 consecutive shots
        self.subscription = self.create_subscription(
            String,                 #msg type
            '/bot_state',           #topic name
            self.listener_callback, #callback function when receiving a message
            1                       #qos (buffer length of msgs)
        )

    def listener_callback(self, msg):
        if msg.data == "shoot":
            GPIO.output(Motoren, GPIO.HIGH)
            time.sleep(2)  # timer van 2 seconden zodat de motoren op snelheid geraken
            servoLader_pwm.ChangeDutyCycle(10.5)  # servo van de lader eerst naar achter trekken zodat een pijlje in de loop kan vallen
            time.sleep(0.5)
            servoLader_pwm.ChangeDutyCycle(2)  # servo naar voor duwen zodat het pijltje afgeschoten wordt
            time.sleep(0.5)
            GPIO.output(Motoren, GPIO.LOW)
            servoLader_pwm.ChangeDutyCycle(10.5)  # servo terug naar achter trekken zodat een volgend pijltje geladen wordt
            time.sleep(0.5)

            self.teller -= 1
            if (self.teller <= 0):  # Voor beveiliging dat de motoren niet te lang aan zijn
                GPIO.output(Motoren, GPIO.LOW)
                servoLader_pwm.ChangeDutyCycle(10.5)
                time.sleep(0.5)
        else:  # motoren uit
            self.teller = 4  # reset teller, terug max 4 keer schieten
            GPIO.output(Motoren, GPIO.LOW)
            servoLader_pwm.ChangeDutyCycle(10.5)
            time.sleep(0.5)

        self.get_logger().info(f"I heard: {msg.data}")

def main(args=None):
    rclpy.init(args=args)

    firemech_subscriber = SubscriberFiremech()

    rclpy.spin(firemech_subscriber)

    firemech_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
