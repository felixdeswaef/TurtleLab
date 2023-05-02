import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist #msg type of /cmd_vel
from std_msgs.msg import String #msg type of /camera_info
from std_msgs.msg import Float64 #msg type of /enemy_distance

class MovementPublisher(Node):

    #values for the twist message for /cmd_vel topic
    linear_x:float
    linear_y:float
    linear_z:float
    angular_x:float
    angular_y:float
    angular_z:float
    enemy_distance:float
    
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
        #for rotation in short intervals:
        self.stop_counter = 0
        timer_period_cmd_vel = 0.5  # seconds
        #send command every timer_period seconds
        self.timer_cmd_vel = self.create_timer(timer_period_cmd_vel, self.publish_velocity)
        
        ### publishing to /bot_state ###
        self.state_publisher = self.create_publisher(
            String,             #msg type
            '/bot_state',       #topic name 
             1                 #qos
        )
        #attribute to configure state
        self.bot_state = "driving"
        timer_period_bot_state = 0.5  # seconds
        #send command every timer_period seconds
        self.timer_bot_state = self.create_timer(timer_period_bot_state, self.publish_bot_state)
        
        ###publishing to /enemy_distance###
        self.enemy_distance = 1.5
        self.enemy_distance_publisher = self.create_publisher(
            Float64,
            '/enemy_distance',
            10
        )
        timer_period_enemy_distance = 0.5  # seconds
        self.timer_enemy_distance = self.create_timer(timer_period_enemy_distance, self.publish_enemy_distance)
        
        ### subcribition to /camera_info ###
        self.camera_subscriber = self.create_subscription(
            String,                 #msg type
            '/camera_info',         #topic name
            self.camera_processor,  #subscriber callback function
            10                      #qos
        )

    def publish_velocity(self):
        """
        Callback function to publish to the /cmd_vel topic
        Output format: type Twist, msg.linear and msg.angular contains floats to change velocity of turtlebot 
        """
        #create msg
        msg = Twist()
        msg.linear.x = self.linear_x
        msg.linear.y = self.linear_y
        msg.linear.z = self.linear_z
        msg.angular.x = self.angular_x
        msg.angular.y = self.angular_y
        msg.angular.z = self.angular_z
        #publish msg
        self.move_publisher.publish(msg)
        self.get_logger().info(f"Publishing a msg with msg:\nlinear:\n  x={msg.linear.x}\n  y={msg.linear.y}\n  z={msg.linear.z}\nangular:\n  x={msg.angular.x}\n  y={msg.angular.y}\n  z={msg.angular.z}\n", throttle_duration_sec=1.0)
    
    def publish_enemy_distance(self):
        """
        Callback function to publish to the /enemy_distance topic
        Ouput format: type Float64, msg.data="<state>"
        """
        msg = Float64()
        msg.data = self.enemy_distance
        self.enemy_distance_publisher.publish(msg)
      
    def publish_bot_state(self):
        """
        Callback function to publish to the /bot_state topic
        Ouput format: type String, msg.data="<state>"
        <state> is a String with possible values "driving", "detected", "shoot"
        """
        msg = String()
        msg.data = self.bot_state
        self.state_publisher.publish(msg)
        
        
    def camera_processor(self, msg:String):
        """
        Callback function to process the information sent from the /camera_info topic
        Input format : type String, msg.data="<distance>;<angle>;<detected>"
        <angle> is a float that represents the angle in radians (positive is right, negative is left)
        <distance> is a float that represents the distance to the other bot in m
        <detected> is an int 0->False, 1->True
        """
        self.get_logger().info(f"Camera_processor received msg = {msg.data}", throttle_duration_sec=1.0)
        try:
            #parse msg
            distance, angle, detected = str(msg.data).split(";") 
            distance = float(distance)
            angle = float(angle)
            detected = float(detected)
            #update info to publish to /enemy_distance
            self.enemy_distance = distance
        except Exception:
            self.get_logger().warning(f"Camera_processor received illegal msg = {msg.data}")
        
        if(detected == 1):
            #update msgs to /bot_state topic
            self.bot_state = "detected"
            #reset movement
            self.angular_x = 0.0
            self.angular_y = 0.0
            self.angular_z = 0.0 
            #aiming 
            if(angle > 0.10):
                #try to aim at the other bot
                self.angular_x = 0.0
                self.angular_y = 0.0
                self.angular_z = -0.1 
            elif(angle < -0.10):
                #try to aim at the other bot
                self.angular_x = 0.0
                self.angular_y = 0.0
                self.angular_z = 0.1
            else:
                if(distance > 1.0):
                    #get closer to enemy bot, charge forward!
                    self.linear_x = -0.5 #go forward
                    self.linear_y = 0.0
                    self.linear_z = 0.0
                else:
                    #close enough, stand still
                    self.linear_x = 0.0 
                    self.linear_y = 0.0
                    self.linear_z = 0.0
                    self.bot_state = "shoot" #fire!
        else:
            self.bot_state = "driving"
            #search enemy bot, start rotating by changing msgs to /cmd_vel topic
            self.linear_x = 0.0 
            self.linear_y = 0.0
            self.linear_z = 0.0
            self.angular_x = 0.0
            self.angular_y = 0.0
            if(self.stop_counter < 10):
                self.angular_z = 0.10 #rotate left    
            else:
                self.angular_z = 0.0 #stop and scan aruco 
            self.stop_counter+=1
            if(self.stop_counter > 20):
                self.stop_counter = 0

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