# Sources:
# https://github.com/DamAnirban/WS2812B_ros/blob/master/light_ros.py
# https://github.com/machinekoder/neopixel_ring/blob/master/neopixel_ring/neopixel_node.py
# https://answers.ros.org/question/414293/how-to-use-ws2812b-led-lights-with-ros-2-node/

# Dependencies
# pip install rpi-ws281x

import rclpy
from std_msgs.msg import ColorRGBA
from rpi_ws281x import Adafruit_NeoPixel, Color

# Define the number of WS2812B LED lights and the pin they are connected to
NUM_LEDS = 34  # Number of LED
LED_PIN = 18  # 0- number will form a color

# Initialize the WS2812B LED lights
strip = Adafruit_NeoPixel(NUM_LEDS, LED_PIN)
strip.begin()
strip.show()

# Callback function for the color message
def color_callback(msg):
    # Set the color of all the WS2812B LED lights
    for i in range(NUM_LEDS):
        strip.setPixelColor(i, Color(int(msg.r * 255), int(msg.g * 255), int(msg.b * 255)))
    strip.show()

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('minimal_subscriber')
    subscription = node.create_subscription(ColorRGBA, 'color', color_callback, 10)
    subscription  # prevent unused variable warning
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()