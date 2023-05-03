# Import necessary modules and packages
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time
import board
import neopixel

# Set up GPIO pin for blue LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

# Set initial state of bot to 0
botstate = 0

# Define a class for the pixel node
class pixelNode(Node):

    # Constructor
    def __init__(self):
        super().__init__('pixel_node')
        
        #(pin, n, brightness, auto_write, pixel_order)
        self.pixels = neopixel.NeoPixel(pin=board.D10, n=34, brightness=0.5, auto_write=True, pixel_order=neopixel.GRB)

        # Subscribe to the topic '/bot_state' and set the callback function
        self.subscription = self.create_subscription(String,
                '/bot_state', self.listener_callback, 1)
        self.subscription  # prevent unused variable warning

        # Set up a timer that runs the timer_callback() function every 0.05 seconds
        timer_period = 0.05  # 20Hz
        self.timer = self.create_timer(timer_period,self.timer_callback)

        # blue LED off - LED strip BLUE
        GPIO.output(25, GPIO.LOW)
        self.pixels.fill((0, 0, 255))
        self.get_logger().info('LEDS: READY')

    # Callback function for the subscription to '/bot_state'

    def listener_callback(self, msg):
        global botstate

        if msg.data == 'driving':
            botstate = 0
        elif msg.data == 'detected':
            botstate = 1
        elif msg.data == 'shoot':
            botstate = 2
        else:
            botstate = 3

    # Timer callback function
    def timer_callback(self):
        global botstate

        if botstate == 0:
            # blue LED on - LED strip GREEN
            GPIO.output(25, GPIO.HIGH)
            self.pixels.fill((0, 255, 0))
            #self.get_logger().info('LEDS: DRIVING')
        elif botstate == 1:
            # blue LED off - LED strip ORANGE
            GPIO.output(25, GPIO.LOW)
            self.pixels.fill((255, 127, 0))
            #self.get_logger().info('LEDS: DETECTED')
        elif botstate == 2:
            # blue LED off - LED strip MAGENTA
            GPIO.output(25, GPIO.LOW)
            self.pixels.fill((255, 0, 255))
            #self.get_logger().info('LEDS: SHOOT')
        else:
            # blue LED off - LED strip RED
            GPIO.output(25, GPIO.LOW)
            self.pixels.fill((255, 0, 0))
            #self.get_logger().info('LEDS: UNKNOWN')
         
# Main function
def main(args=None):

    # Initialize ROS
    rclpy.init(args=args)

    # Create an instance of the pixelNode class
    pixel_node = pixelNode()

    # Spin the node
    rclpy.spin(pixel_node)

    # Destroy the node and shutdown ROS when done
    pixel_node.destroy_node()
    rclpy.shutdown()

# Call the main function if this file is run directly
if __name__ == '__main__':
    main()
