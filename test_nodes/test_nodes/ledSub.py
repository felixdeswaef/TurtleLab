# Subscriber dependencies
import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time

# LED dependencies
import time
import board
import neopixel

GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.OUT)

#from adafruit_led_animation.color import *
#from adafruit_led_animation.animation.rainbow import Rainbow
#from adafruit_led_animation.animation.chase import Chase
#from adafruit_led_animation.animation.comet import Comet
#from adafruit_led_animation.animation.solid import Solid
#from adafruit_led_animation.color import *



bluestate = 0
#rainbow = Rainbow(pixels, speed=0.1, period=3, step=5)
#comet = Comet(pixels, speed=0.1, color=PURPLE, tail_length=17, bounce=True)
#chase = Chase(pixels, speed=0.1, size=4, spacing=6, color=AMBER)
#solid = Solid(pixels, color=RED)

class pixelNode(Node):

    def __init__(self, pixel_pin = board.D18, num_pixels = 34, ORDER = neopixel.GRB):       
        super().__init__('pixel_node')

        self.subscription = self.create_subscription(
            String,
            'bot_state',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        self.pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)       self.pixels.fill((255, 0, 0))
        self.pixels.show()
        
        # blue led blinker
        timer_period = 0.5  # 2Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def listener_callback(self, msg):        
        if msg.data == 'driving':
            self.pixels.fill((255, 255, 255))
            self.get_logger().info('LEDS: DRIVING')
            
        elif msg.data == 'detected':
            self.pixels.fill((255, 127, 0))
            self.get_logger().info('LEDS: DETECTED')
            
        elif msg.data == 'shoot':
            self.pixels.fill((255, 0, 255))
            self.get_logger().info('LEDS: SHOOT')

        else:
            self.pixels.fill((255, 0, 0))
            self.get_logger().info('LEDS: UNKNOWN')
        
        self.pixels.show()
        
    def timer_callback(self):
        global bluestate
        
        if bluestate == 0:
            GPIO.output(25, GPIO.HIGH)
            bluestate = 1
        else:
            GPIO.output(25, GPIO.LOW)
            bluestate = 0       
            
def main(args=None):
    rclpy.init(args=args)

    pixel_node = pixelNode()

    rclpy.spin(pixel_node)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    pixel_node.destroy_node()
    rclpy.shutdown()
   
if __name__ == '__main__':
    main()