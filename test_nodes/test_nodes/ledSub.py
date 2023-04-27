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

bluestate = 0

# Callback function for the color message
def led_callback(msg):
    if msg.data == 'driving':
        for i in range(NUM_LEDS):
            strip.setPixelColor(i, Color(0, 255, 0))
    elif msg.data == 'detected':
        for i in range(NUM_LEDS):
            strip.setPixelColor(i, Color(255, 255, 0))
    elif msg.data == 'shoot':
        for i in range(NUM_LEDS):
            strip.setPixelColor(i, Color(255, 0, 0))
    else:
        for i in range(NUM_LEDS):
            strip.setPixelColor(i, Color(255, 0, 255))
    
    strip.show()
    
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
    node = rclpy.create_node('minimal_subscriber')
    subscription = node.create_subscription(String, 'bot_state', led_callback, 10)
    subscription  # prevent unused variable warning
    
    # blue led blinker
    timer_period = 0.5  # 2Hz
    timer = create_timer(timer_period, timer_callback)

    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()