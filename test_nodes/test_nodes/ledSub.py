# Subscriber dependencies
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# LED dependencies
import time
import board
import neopixel

from adafruit_led_animation.color import *
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.solid import Solid
from adafruit_led_animation.color import *

num_pixels = 34

pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)

anim = 0
rainbow = Rainbow(pixels, speed=0.1, period=3, step=5)
comet = Comet(pixels, speed=0.1, color=PURPLE, tail_length=17, bounce=True)
chase = Chase(pixels, speed=0.1, size=4, spacing=6, color=AMBER)
solid = Solid(pixels, color=RED)

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')

        self.subscription = self.create_subscription(
            String,
            'bot_state',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning
        
        timer_period = 0.02  # 50Hz
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def listener_callback(self, msg):
        #self.get_logger().info('bot_state: "%s"' % msg.data)
        
        if msg.data == 'driving':
            anim = 1
            self.get_logger().info('LEDS: DRIVING')
            
        elif msg.data == 'detected':
            anim = 2
            self.get_logger().info('LEDS: DETECTED')
            
        elif msg.data == 'shoot':
            anim = 3
            self.get_logger().info('LEDS: SHOOT')
        # Unknown data -> solid red
        else:
            anim = 0
            self.get_logger().info('LEDS: UNKNOWN')
    
    def timer_callback(self):
        if anim == 1:
            rainbow.animate()
        elif anim == 2:
            comet.animate()
        elif anim == 3:
            chase.animate()
        else:
            solid.animate()
            
def main(args=None):
    rclpy.init(args=args)

    minimal_subscriber = MinimalSubscriber()

    rclpy.spin(minimal_subscriber)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
   
if __name__ == '__main__':
    main()