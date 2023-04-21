import rclpy
import sys
from rclpy.node import Node
from std_msgs.msg import String

#for reading keyboard input
import sys, select, termios, tty
settings = termios.tcgetattr(sys.stdin)

class KeyboardReader(Node):
    
    def __init__(self):
        super().__init__(type(self).__name__) #give this node the name of the class
        #create publisher
        self.key_publisher = self.create_publisher(
            String,         #msg type
            '/cmd_key',     #topic name
             10             #qos
        )
        
        # timer_period = 0.1
        # self.timer = self.create_timer(timer_period, self.read_keyboard_input)
        
    def read_keyboard_input(self):
        msg_controls = "Reading keyboard input to adjust speed\n"
        msg_controls += "press w to move forward (increase linear velocity)\n"
        msg_controls += "press s to move backward (decrease linear velocity)\n"    
        msg_controls += "press a to move right (increase angular velocity)\n"
        msg_controls += "press d to move left (decrease angular velocity)\n"
        msg_controls += "press e stop the bot from moving \n"
        msg_controls += "press q to quit"
        print(msg_controls)
        while(True):
            tty.setraw(sys.stdin.fileno(), when=termios.TCSAFLUSH) #set terminal to hide entered characters
            a = select.select([sys.stdin], [], [], 0) #try to read from stdin with timeout 0 seconds
            key = sys.stdin.read(1) #read 1 byte
            if(key=='q'):
                tty.setcbreak(sys.stdin.fileno(), when=termios.TCSAFLUSH) #set terminal to display entered characters
                termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, settings) #apply settings
                exit()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings) #apply settings
            #print(f"received key {key}")
            msg = String()
            msg.data = key[0]
            self.key_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    #make new publisher object
    node = KeyboardReader()
    node.read_keyboard_input()
    #keep node alive
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()