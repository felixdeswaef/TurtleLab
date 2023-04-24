import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class test_visual_cortex(Node):
    
    #value's for anlge, distance and detected
    angle = [3.7, 0.0, 0.0, 0.0, -4.3, -4.2]
    distance = [1.1, 123.0, 123.0, 123.0, 2.2, 3.3]
    detected = [0, 1, 1, 1, 1, 1]
    idx = 0
    
    def __init__(self):
        super().__init__(type(self).__name__) #give this node the name of the class
        
        #create test publisher
        self.test_publisher = self.create_publisher(
            String,      #msg type
            '/camera_info', #topic name 
             10         #qos
        )
        #send command every timer_period seconds
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.publish_camera_info)
        

    def publish_camera_info(self):
        #create msg
        msg = String()
        msg.data += str(self.angle[self.idx])
        msg.data += ";" 
        msg.data += str(self.distance[self.idx])
        msg.data += ";"
        msg.data += str(self.detected[self.idx])
        #publish msg
        self.test_publisher.publish(msg)
        self.get_logger().info(f"Publishing a msg: {msg.data}")
        self.idx += 1
        if(self.idx == len(self.angle)):
            self.idx = 0

        
def main(args=None):
    rclpy.init(args=args)
    #make new publisher object
    test_publisher = test_visual_cortex()
    #keep node alive
    rclpy.spin(test_publisher)

    test_publisher.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()