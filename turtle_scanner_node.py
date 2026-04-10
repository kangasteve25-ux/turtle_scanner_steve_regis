import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
import math

class TurtleScanner(Node):
    def __init__(self):
        super().__init__('turtle_scanner')

        # Souscriptions
        self.sub_turtle1 = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback_turtle1,
            10
        )

        self.sub_target = self.create_subscription(
            Pose,
            '/turtle_target/pose',
            self.pose_callback_target,
            10
        )

        self.pose_turtle1 = None
        self.pose_target = None

        self.get_logger().info('Nœud Scanner démarré - En attente des données...')

    def pose_callback_turtle1(self, msg):
        self.pose_turtle1 = msg
        self.compute_distance()

    def pose_callback_target(self, msg):
        self.pose_target = msg
        self.compute_distance()

    def compute_distance(self):
        if self.pose_turtle1 and self.pose_target:
            dist = math.sqrt(
                (self.pose_target.x - self.pose_turtle1.x) ** 2 +
                (self.pose_target.y - self.pose_turtle1.y) ** 2
            )

            self.get_logger().info(f'Distance cible : {dist:.2f} m')


def main(args=None):
    rclpy.init(args=args)
    node = TurtleScanner()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()