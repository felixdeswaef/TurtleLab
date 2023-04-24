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
        self.dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        self.cm = [[823.93985557  , 0.      ,   322.76228491],[  0.    ,     825.11141958 ,279.6240493 ],[  0.    ,       0.      ,     1.        ]]
        self.parameters = cv2.aruco.DetectorParameters()
        self.ms=0.05
        self.detector = cv2.aruco.ArucoDetector(self.dictionary, self.parameters)
        self.dm = [[ 6.29137073e-02 ,-7.33484417e-01  ,6.53444356e-03 , 3.83894903e-03, 1.16325776e+01]]
        self.hoek=45            #nog te testen 
        self.timer = self.create_timer(0.3, self.timer_callback)  # process the vid every 1 second
    def my_estimatePoseSingleMarkers(self,corners):
        marker_size=self.ms
        marker_points = np.array([[-marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, marker_size / 2, 0],
                              [marker_size / 2, -marker_size / 2, 0],
                              [-marker_size / 2, -marker_size / 2, 0]], dtype=np.float32)
        trash = []
        rvecs = []
        tvecs = []
        i = 0
        for c in corners:
            nada, R, t = cv2.solvePnP(marker_points, corners[i], self.cm, self.dm, False, cv2.SOLVEPNP_IPPE_SQUARE)
            rvecs.append(R)
            tvecs.append(t)
            trash.append(nada)

        return rvecs, tvecs, trash

    def pose_estimation(self,frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, rejected_img_points = self.detector.detectMarkers(gray)
        param=2.4
        enemy=False
        if len(corners) > 0:    
            for i in range(0, len(ids)):
                rvec, tvec, rejimp= self.my_estimatePoseSingleMarkers(corners[i])
                if len(tvec)!=0:
                    afstand="{:.3f}".format(param*sqrt(tvec[0][0]**2+tvec[0][2]**2))             
                    h=corners[i][0][1]-corners[i][0][0]*self.hoek
                    return afstand,h
        return 0,0

    def timer_callback(self):
        ret, frame = self.camera.read()  # read a frame from the camera
        if not ret:
            self.get_logger().warning('Failed to read frame from camera')
            return
        var3=self.pose_estimation(frame)
        msg=String()
        msg.data = str(var3)
        self.publisher_.publish(msg)
        

def main(args=None):
    rclpy.init(args=args)
    vc = Visual_Cortex()
    rclpy.spin(vc)
    vc.camera.release()  # release the camera
    rclpy.shutdown()

if __name__ == '__main__':
    main()
