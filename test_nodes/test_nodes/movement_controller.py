import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist #msg type of /cmd_vel
from std_msgs.msg import String #msg type of /camera_info

class MovementPublisher(Node):

    #values for the twist message for /cmd_vel topic
    linear_x:float
    linear_y:float
    linear_z:float
    angular_x:float
    angular_y:float
    angular_z:float
    
    #value for str message for /bot_state topic
    bot_state:str
    
    def __init__(self):
        super().__init__(type(self).__name__) #give this node the name of the class
        
        ### publishing to /cmd_vel ###
        self.move_publisher = self.create_publisher(
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
        timer_period_cmd_vel = 0.1  # seconds
        #send command every timer_period seconds
        self.timer_cmd_vel = self.create_timer(timer_period_cmd_vel, self.publish_velocity)
        
        ### publishing to /bot_state ###
        self.state_publisher = self.create_publisher(
            String,             #msg type
            '/bot_state',       #topic name 
             10                 #qos
        )
        #attribute to configure state
        self.bot_state = "driving"
        timer_period_bot_state = 0.1  # seconds
        #send command every timer_period seconds
        self.timer_bot_state = self.create_timer(timer_period_bot_state, self.publish_bot_state)
        
        ### subcribition to /camera_info ###
        self.camera_subscriber = self.create_subscription(
            String,                 #msg type
            '/camera_info',         #topic name
            self.camera_processor,  #subscriber callback function
            10                      #qos
        )

    def publish_velocity(self):
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
        
    def publish_bot_state(self):
        """
        Callback function to publish to the /bot_state topic
        Ouput format: msg.data="<state>"
        <state> is a String with possible values "driving", "detected", "shoot"
        """
        msg = String()
        msg.data = self.bot_state
        self.state_publisher.publish(msg)
        
        
    def camera_processor(self, msg:String):
        """
        Callback function to process the information sent from the /camera_info topic
        Input format : msg.data="<angle>;<distance>;<detected>"
        <angle> is a float that represents the angle in degrees (positive is right, negative is left)
        <distance> is a float that represents the distance to the other bot in cm
        <detected> is ann int 0->False, 1->True
        """
        self.get_logger().info(f"Camera_processor received msg = {msg.data}")
        #parse msg
        angle, distance, detected = msg.data.split() 
        angle = float(angle)
        distance = float(distance)
        detected = float(detected)
        
        if(detected == 1):
            #update msgs to /bot_state topic
            self.bot_state = "detected"
        else:
            #search enemy bot, start rotating by changing msgs to /cmd_vel topic
            self.linear_x = 0.0 #forward-backward control
            self.linear_y = 0.0
            self.linear_z = 0.0
            self.angular_x = 0.0
            self.angular_y = 0.0
            self.angular_z = 1.0 #left-right control
            
        if(angle > 1):
            #try to aim at the other bot
            self.angular_x = 0.0
            self.angular_y = 0.0
            self.angular_z = 0.5 #left-right control
        elif(angle < -1):
            #try to aim at the other bot
            self.angular_x = 0.0
            self.angular_y = 0.0
            self.angular_z = -0.5 #left-right control
        else:
            if(distance > 100):
                #get closer to enemy bot, charge forward!
                self.linear_x = -1.0 #forward-backward control
                self.linear_y = 0.0
                self.linear_z = 0.0
            else:
                #close enough, stand still
                self.linear_x = 0.0 #forward-backward control
                self.linear_y = 0.0
                self.linear_z = 0.0
        

def main(args=None):
    rclpy.init(args=args)
    #make new publisher object
    node = MovementPublisher()
    #keep node alive
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()