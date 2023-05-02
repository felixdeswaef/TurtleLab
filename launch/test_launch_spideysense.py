"""
Launchfile containing the 3 main nodes and a varition of the firemech node (spideysense)
-visual_cortex: Detection of aruco codes and calulating distance, angle and detection
-movement_controller: Driving of wheels based on camera info and publishing bot_state to communicate with ledSub and firemech
-ledSub: Driving leds based on bot_state.
-spideysense: Driving firing mechanism based on camera_info
"""
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='test_nodes',
            executable='visual_cortex',
            name='visual_cortex'
        ),
        Node(
            package='test_nodes',
            executable='movement_controller',
            name='movement_controller'
        ),
        Node(
            package='test_nodes',
            executable='ledSub',
            name='ledSub'
        ),
        Node(
            package='test_nodes',
            executable='spideysense',
            name='spideysense'
        )
    ])