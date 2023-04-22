# Subscriber dependencies
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

# LED dependencies
import time
import board
import neopixel

num_pixels = 34

pixel_pin = board.D18
ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER
)

def colorwheel(pos):
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            pixels[i] = colorwheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)
        
# TODO: add multiple subscribers in this node to reflect status on LED's
# http://docs.ros.org/en/foxy/The-ROS2-Project/Contributing/Migration-Guide-Python.html

class MinimalSubscriber(Node):

    def __init__(self):
        super().__init__('minimal_subscriber')

        self.subscription = self.create_subscription(
            String,
            'leds',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('leds: "%s"' % msg.data)
        
        if(msg.data == 'driving'):
            anim = 0
            
        elif(msg.data == 'detected'):
            anim = 1
            
        elif(msg.data == 'spooling'):
            anim = 2
            
        elif(msg.data == 'firing'):
            anim = 3

def anim0():
    rainbow_cycle(0.005)

def anim1():
    pixels.fill((255, 127, 0))
    pixels.show()
            
def anim2():
    pixels.fill((255, 0, 255))
    pixels.show()

def anim3():
    pixels.fill((255, 255, 255))
    pixels.show()
            
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