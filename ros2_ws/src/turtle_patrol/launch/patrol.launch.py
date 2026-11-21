"""Turtlesim ile devriye düğümünü birlikte başlatır."""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    side = LaunchConfiguration('side_length')
    laps = LaunchConfiguration('laps')
    sides = LaunchConfiguration('sides')
    return LaunchDescription([
        DeclareLaunchArgument('side_length', default_value='3.0',
                              description='Çokgenin kenar uzunluğu (m)'),
        DeclareLaunchArgument('sides', default_value='4',
                              description='Kenar sayısı: 3 üçgen, 4 kare, 6 altıgen'),
        DeclareLaunchArgument('laps', default_value='1',
                              description='Kaç tur atılacağı'),
        Node(package='turtlesim', executable='turtlesim_node', name='sim'),
        Node(package='turtle_patrol', executable='patrol', name='patrol',
             output='screen',
             parameters=[{'side_length': side, 'laps': laps,
                          'sides': ParameterValue(sides, value_type=int)}]),
    ])
