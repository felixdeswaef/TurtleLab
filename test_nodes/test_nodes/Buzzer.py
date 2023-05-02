import rclpy
from rclpy.node import Node

from std_msgs.msg import String
import RPi.GPIO as GPIO
from microbit import *
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
    	if(msg.data == 'muziek'):
    	i = 200
    	    while (i >= 0):
                BuzzerStarWars(pin0)
                 i -= 1
           
        else: #voor als er iets zou misgaan met de messages
           GPIO.output(Motoren, 0)
        self.get_logger().info('I heard: "%s"' % msg.data)
        
    def beep (pin, noteFrequency, noteDuration, sleepDuration = 100):
  	microsecondsPerWave = 1e6/noteFrequency
  	millisecondsPerCycle = 1000/(microsecondsPerWave * 2)
  	loopTime = noteDuration * millisecondsPerCycle
  	for x in range(loopTime):
    	    pin.write_digital(1)
    	    time.sleep_us(int(microsecondsPerWave))
    	    pin.write_digital(0)
    	    time.sleep_us(int(microsecondsPerWave))
  	sleep(sleepDuration)

    def BuzzerStarWars(pin):
  	SW_NOTES = [293.66, 293.66, 293.66, 392.0, 622.25, 554.37, 523.25, 454, 932.32, 622.25, 554.37, 523.25, 454, 932.32, 622.25, 554.37, 523.25, 554.37, 454]
  	SW_DURATION = [180, 180, 180, 800, 800, 180, 180, 180, 800, 400, 180, 180, 180, 800, 400, 180, 180, 180, 1000]
  	SW_SLEEP = [40, 40, 40, 100, 100, 40, 40, 40, 100, 50, 40, 40, 40, 100, 50, 40, 40, 40, 100]
  	for i in range(len(SW_NOTES)):
    	    beep(pin, SW_NOTES[i], SW_DURATION[i], SW_SLEEP[i])


def main(args=None):
    rclpy.init(args=args)

    Motor_subscriber = MinimalSubscriber()

    rclpy.spin(Motor_subscriber)

    Motor_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
    
    

