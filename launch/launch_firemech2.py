"""
Launchfile containing the 3 main nodes and a varition of the firemech node
-visual_cortex: Detection of aruco codes and calulating distance, angle and detection
-movement_controller: Driving of wheels based on camera info and publishing bot_state to communicate with ledSub and firemech
-ledSub: Driving leds based on bot_state.
-firemech_2: Driving firing mechanism based on bot_state without safety measure for the motors (if it keeps receiving shoot, the motors keep spinning)
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlebot3_nodes',
            executable='visual_cortex',
            name='visual_cortex'
        ),
        Node(
            package='turtlebot3_nodes',
            executable='movement_controller',
            name='movement_controller'
        ),
        Node(
            package='turtlebot3_nodes',
            executable='ledSub',
            name='ledSub'
        ),
        Node(
            package='turtlebot3_nodes',
            executable='firemech_2',
            name='firemech_2'
        )
    ])