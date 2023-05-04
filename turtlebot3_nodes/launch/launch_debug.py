"""
Launchfile for debug
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
        )
    ])