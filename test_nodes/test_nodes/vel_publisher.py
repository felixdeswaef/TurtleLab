import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import String

class VelocityPublisher(Node):

    #values for the twist message
    linear_x:float
    linear_y:float
    linear_z:float
    angular_x:float
    angular_y:float
    angular_z:float
    
    def get_linear_x(self):
        return self.linear_x
    
    def get_angular_z(self):
        return self.angular_z
    
    def __init__(self):
        super().__init__(type(self).__name__) #give this node the name of the class
        
        #create velocity publisher
        self.vel_publisher = self.create_publisher(
            Twist,      #msg type
            '/cmd_vel', #topic name 
             10         #qos
        )
        #attributes to control speed
        self.linear_x = 0.0 #forward-backward control
        self.linear_y = 0.0
        self.linear_z = 0.0
        self.angular_x = 0.0
        self.angular_y = 0.0
        self.angular_z = 0.0 #left-right control
        timer_period = 0.1  # seconds
        #send command every timer_period seconds
        self.timer = self.create_timer(timer_period, self.publish_vel)
        
        #create subscibtion to the /cmd_key topic to adjust the speed we are sending
        self.key_subscriber = self.create_subscription(
            String,             #msg type
            '/cmd_key',         #topic name
            self.adjust_speed,  #subscriber callback function
            10                  #qos
        )

    def publish_vel(self):
        #create msg
        msg = Twist()
        msg.linear.x = self.linear_x
        msg.linear.y = self.linear_y
        msg.linear.z = self.linear_z
        msg.angular.x = self.angular_x
        msg.angular.y = self.angular_y
        msg.angular.z = self.angular_z
        #publish msg
        self.vel_publisher.publish(msg)
        self.get_logger().info(f"Publishing a msg with msg:\nlinear:\n  x={msg.linear.x}\n  y={msg.linear.y}\n  z={msg.linear.z}\nangular:\n  x={msg.angular.x}\n  y={msg.angular.y}\n  z={msg.angular.z}\n")

    def adjust_speed(self, msg:String):
        key = msg.data[0]
        self.get_logger().info(f"Received message with key {msg}")
        
        if(key == 'w'):
            self.linear_x += 0.125
        elif(key == 's'):
            self.linear_x -= 0.125
        elif(key == 'a'):
            self.angular_z += 0.125
        elif(key == 'd'):
            self.angular_z -= 0.125
        elif(key == "e"):
            self.linear_x = 0.0
            self.linear_y = 0.0
            self.linear_z = 0.0
            self.angular_x = 0.0
            self.angular_y = 0.0
            self.angular_z = 0.0
        

def main(args=None):
    rclpy.init(args=args)
    #make new publisher object
    vel_publisher = VelocityPublisher()
    #keep node alive
    rclpy.spin(vel_publisher)

    vel_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()