import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    config = os.path.join(
        get_package_share_directory('pid_controller'),
        'config',
        'parameters.yaml'
    )

    kp = LaunchConfiguration('kp')
    ki = LaunchConfiguration('ki')
    kd = LaunchConfiguration('kd')

    return LaunchDescription([
        DeclareLaunchArgument('kp', default_value='0.1'),
        DeclareLaunchArgument('ki', default_value='0.01'),
        DeclareLaunchArgument('kd', default_value='0.001'),

        Node(
            package='pid_controller',
            executable='pid_controller_node',
            name='pid_controller_node',
            output='screen',
            arguments=['--ros-args', '--log-level', 'info'],
            parameters=[{
                'p': kp,
                'i': ki,
                'd': kd,
            }],
        ),

        Node(
            package='joint_simulator',
            executable='joint_simulator_node',
            name='joint_simulator_node',
            output='screen',
            arguments=['--ros-args', '--log-level', 'warn'],
            parameters=[config],
        ),

        Node(
            package='reference_input_node',
            executable='reference_input_node',
            name='reference_input_node',
            output='screen',
            arguments=['--ros-args', '--log-level', 'info'],
        ),
    ])
