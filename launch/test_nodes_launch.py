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
            executable='firemech',
            name='firemech'
        )
    ])