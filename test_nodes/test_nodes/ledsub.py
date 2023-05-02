# Import necessary modules and packages

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time
import board
import neopixel
from adafruit_led_animation.color import *
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import *

# Set up GPIO pin for blue LED

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

# Set initial state of bot to 0

botstate = 0

# Set up NeoPixels

pixel_pin = board.D10
num_pixels = 34
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5,
                           auto_write=False, pixel_order=ORDER)

# define animations

rainbow = Rainbow(pixels, speed=0.1, period=3, step=5)
comet = Comet(pixels, speed=0.1, color=(255, 0, 255), tail_length=17,
              bounce=True)
chase = Chase(pixels, speed=0.1, size=4, spacing=6, color=(255, 127, 0))
solid = Solid(pixels, color=(255, 0, 0))


# Define a class for the pixel node

class pixelNode(Node):

    # Constructor

    def __init__(self):
        super().__init__('pixel_node')

        # Subscribe to the topic '/bot_state' and set the callback function

        self.subscription = self.create_subscription(String,
                '/bot_state', self.listener_callback, 1)
        self.subscription  # prevent unused variable warning

        # Set up a timer that runs the timer_callback() function every 0.05 seconds

        timer_period = 0.05  # 20Hz
        self.timer = self.create_timer(timer_period,
                self.timer_callback)

        # Set all NeoPixels to blue and display them

        pixels.fill((0, 0, 255))
        self.get_logger().info('LEDS: READY')
        pixels.show()

    # Callback function for the subscription to '/bot_state'

    def listener_callback(self, msg):
        global botstate

        # Set botstate based on the message received

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

        # Display blue LED and rainbow animation if botstate is 0

        if botstate == 0:
            GPIO.output(25, GPIO.HIGH)
            rainbow.animate()
        elif botstate == 1:

        # Display orange LED and chase animation if botstate is 1

            GPIO.output(25, GPIO.LOW)
            chase.animate()
        elif botstate == 2:

        # Display purple LED and comet animation if botstate is 2

            GPIO.output(25, GPIO.LOW)
            comet.animate()
        else:

        # Display red LED and solid animation if botstate is not 0, 1, or 2

            GPIO.output(25, GPIO.LOW)
            solid.animate()


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
