from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='test_nodes',
            executable='test_visual_cortex',
            name='test_visual_cortex'
        ),
        Node(
            package='test_nodes',
            executable='movement_controller',
            name='movement_controller'
        ),
    ])