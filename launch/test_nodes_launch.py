from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='test_nodes',
            executable='vel_publisher',
            name='vel_publisher'
        ),
        Node(
            package='test_nodes',
            executable='keyboard_reader',
            name='keyboard_reader'
        ),
    ])