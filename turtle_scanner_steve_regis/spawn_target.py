import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn
import random

class SpawnTarget(Node):
    def __init__(self):
        super().__init__('spawn_target')
        self.client = self.create_client(Spawn, '/spawn')
        self.get_logger().info('Nœud spawn_target démarré')

    def spawn(self):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('En attente du service /spawn...')

        request = Spawn.Request()
        request.name = 'turtle_target'
        request.x = random.uniform(1.0, 10.0)
        request.y = random.uniform(1.0, 10.0)
        request.theta = 0.0

        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info(f'Turtle cible spawnée à ({request.x:.2f}, {request.y:.2f})')
        else:
            self.get_logger().error('Échec du spawn')

def main(args=None):
    rclpy.init(args=args)
    node = SpawnTarget()
    node.spawn()
    node.destroy_node()
    rclpy.shutdown()
if __name__ == '__main__':
    main()
