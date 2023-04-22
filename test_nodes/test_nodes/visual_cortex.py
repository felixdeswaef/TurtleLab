import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from math import sqrt
from std_msgs.msg import String

class Visual_Cortex(Node):
    def __init__(self):
        super().__init__('Visual_cortex')
        self.publisher_ = self.create_publisher(String, 'enemy_position', 10)
        self.camera = cv2.VideoCapture(0)
        self.cm = np.load( "calibration_matrix.npy")
        self.parameters = cv2.aruco.DetectorParameters_create()
        self.dm = np.load("distortion_coefficients.npy")
        self.hoek=45            #nog te testen 
        self.timer = self.create_timer(0.3, self.timer_callback)  # process the vid every 1 second


    def pose_estimation(self,frame, matrix_coefficients, distortion_coefficients,param,camhoek):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_4X4_50)
        corners, ids, rejected_img_points = cv2.aruco.detectMarkers(gray, cv2.aruco_dict,parameters=self.parameters,
        cameraMatrix=self.cm,
        distCoeff=self.dm)
        enemy=False
        if len(corners) > 0:
            for i in range(0, len(ids)):
                rvec, tvec, markerPoints = cv2.aruco.estimatePoseSingleMarkers(corners[i], 0.02, matrix_coefficients,
                                                                       distortion_coefficients)
                cv2.aruco.drawDetectedMarkers(frame, corners) 
                if len(tvec)!=0:
                    afstand="{:.3f}".format(param*sqrt(tvec[0][0][0]**2+tvec[0][0][2]**2))             
                    h=corners[i][0][1]-corners[i][0][0]*self.hoek
        return len(ids)

    def timer_callback(self):
        ret, frame = self.camera.read()  # read a frame from the camera
        if not ret:
            self.get_logger().warning('Failed to read frame from camera')
            return
        var3=self.pose_estimation()


        msg = msg.data = str(var3)
        self.publisher_.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)
    vc = Visual_Cortex()
    rclpy.spin(vc)
    vc.camera.release()  # release the camera
    rclpy.shutdown()

if __name__ == '__main__':
    main()
