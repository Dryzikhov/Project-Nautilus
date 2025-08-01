import unittest
import numpy as np
from nautilus.navigation.navigator import Navigator

class TestNavigator(unittest.TestCase):

    def setUp(self):
        self.navigator = Navigator(grid_size=(10, 10))
        self.sparse_lidar = np.array([[10, 20, 30], [-10, -20, -30], [5, -15, 25]]) # High std dev
        self.dense_lidar = np.random.rand(10, 3) # Low std dev

    def test_avoid_obstacle_safe(self):
        sonar_data = {'distance': 50, 'angle': 30}
        self.assertEqual(self.navigator.avoid_obstacle(sonar_data, self.sparse_lidar), "Proceed")

    def test_avoid_obstacle_sonar_only_left(self):
        sonar_data = {'distance': 15, 'angle': 30}
        self.assertEqual(self.navigator.avoid_obstacle(sonar_data, self.sparse_lidar), "Turn Left")

    def test_avoid_obstacle_sonar_only_right(self):
        sonar_data = {'distance': 15, 'angle': -30}
        self.assertEqual(self.navigator.avoid_obstacle(sonar_data, self.sparse_lidar), "Turn Right")

    def test_avoid_obstacle_sonar_and_lidar_left(self):
        sonar_data = {'distance': 15, 'angle': 30}
        self.assertEqual(self.navigator.avoid_obstacle(sonar_data, self.dense_lidar), "Hard Turn Left")

    def test_avoid_obstacle_sonar_and_lidar_right(self):
        sonar_data = {'distance': 15, 'angle': -30}
        self.assertEqual(self.navigator.avoid_obstacle(sonar_data, self.dense_lidar), "Hard Turn Right")

    def test_optimize_route_simple(self):
        start = (0, 0)
        end = (2, 2)
        obstacles = []
        path = self.navigator.optimize_route(start, end, obstacles)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)
        self.assertEqual(len(path), 5) # (0,0)->(0,1)->(0,2)->(1,2)->(2,2) or similar

    def test_optimize_route_with_obstacles(self):
        start = (0, 0)
        end = (3, 3)
        obstacles = [(1, 1), (1, 2), (1, 3)]
        path = self.navigator.optimize_route(start, end, obstacles)
        self.assertIsNotNone(path)
        self.assertNotIn((1, 1), path)
        self.assertNotIn((1, 2), path)
        self.assertNotIn((1, 3), path)

    def test_optimize_route_no_path(self):
        start = (1, 1)
        end = (8, 8)
        # Create a vertical wall of obstacles
        obstacles = [(5, i) for i in range(0, 10)]
        path = self.navigator.optimize_route(start, end, obstacles)
        self.assertIsNone(path)

    def test_optimize_route_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.navigator.optimize_route((0, 0), (11, 11), [])

if __name__ == '__main__':
    unittest.main()
