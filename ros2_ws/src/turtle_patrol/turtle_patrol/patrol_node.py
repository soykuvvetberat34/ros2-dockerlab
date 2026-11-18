"""Kaplumbağayı konum geri beslemesiyle kare çizerek devriye gezdiren düğüm."""

from geometry_msgs.msg import Twist
import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose

from turtle_patrol.geometry import compute_command, square_waypoints


class PatrolNode(Node):
    """/turtle1/pose dinler, /turtle1/cmd_vel yayınlar."""

    def __init__(self):
        super().__init__('patrol')
        self.side = self.declare_parameter('side_length', 3.0).value
        self.linear_speed = self.declare_parameter('linear_speed', 1.5).value
        self.angular_speed = self.declare_parameter('angular_speed', 1.5).value
        self.laps = self.declare_parameter('laps', 1).value

        self.cmd_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.create_subscription(Pose, '/turtle1/pose', self.on_pose, 10)
        self.timer = self.create_timer(0.05, self.on_timer)

        self.pose = None
        self.waypoints = []
        self.index = 0
        self.done = False
        self.get_logger().info(
            f'Devriye: kenar={self.side} m, tur={self.laps}, '
            f'hız={self.linear_speed} m/s')

    def on_pose(self, msg):
        self.pose = msg
        if not self.waypoints:
            corners = square_waypoints(msg.x, msg.y, msg.theta, self.side)
            self.waypoints = corners * self.laps
            self.get_logger().info(f'Başlangıç: ({msg.x:.2f}, {msg.y:.2f})')

    def on_timer(self):
        if self.pose is None or self.done:
            return
        target = self.waypoints[self.index]
        linear, angular, reached = compute_command(
            self.pose.x, self.pose.y, self.pose.theta, target,
            self.linear_speed, self.angular_speed)

        if reached:
            self.index += 1
            self.get_logger().info(f'Köşe {self.index}/{len(self.waypoints)} tamam')
            if self.index >= len(self.waypoints):
                self.done = True
                self.cmd_pub.publish(Twist())
                self.get_logger().info('Devriye tamamlandı.')
            return

        cmd = Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        self.cmd_pub.publish(cmd)


def main(args=None):
    rclpy.init(args=args)
    node = PatrolNode()
    try:
        while rclpy.ok() and not node.done:
            rclpy.spin_once(node, timeout_sec=0.1)
    except KeyboardInterrupt:
        pass
    finally:
        node.cmd_pub.publish(Twist())
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
