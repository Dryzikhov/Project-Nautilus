import unittest
import numpy as np
from nautilus.navigation.navigator import Navigator

class TestNavigator(unittest.TestCase):

    def setUp(self):
        self.navigator = Navigator(grid_size=(10, 10))

    def test_avoid_obstacle_low_risk(self):
        """Test 'Proceed' action for low obstacle risk."""
        self.assertEqual(self.navigator.avoid_obstacle(0.2, 30), "Proceed")

    def test_avoid_obstacle_moderate_risk_left(self):
        """Test 'Turn Left' action for moderate risk."""
        self.assertEqual(self.navigator.avoid_obstacle(0.5, 30), "Turn Left")

    def test_avoid_obstacle_moderate_risk_right(self):
        """Test 'Turn Right' action for moderate risk."""
        self.assertEqual(self.navigator.avoid_obstacle(0.5, -30), "Turn Right")

    def test_avoid_obstacle_high_risk_left(self):
        """Test 'Hard Turn Left' action for high risk."""
        self.assertEqual(self.navigator.avoid_obstacle(0.8, 30), "Hard Turn Left")

    def test_avoid_obstacle_high_risk_right(self):
        """Test 'Hard Turn Right' action for high risk."""
        self.assertEqual(self.navigator.avoid_obstacle(0.8, -30), "Hard Turn Right")

    def test_optimize_route_simple(self):
        start, end, obstacles = (0, 0), (2, 2), []
        path = self.navigator.optimize_route(start, end, obstacles)
        self.assertIsNotNone(path)
        self.assertEqual(path[0], start)
        self.assertEqual(path[-1], end)
        self.assertEqual(len(path), 5)

    def test_optimize_route_with_obstacles(self):
        start, end = (0, 0), (3, 3)
        obstacles = [(1, 1), (1, 2), (1, 3)]
        path = self.navigator.optimize_route(start, end, obstacles)
        self.assertIsNotNone(path)
        for obs in obstacles:
            self.assertNotIn(obs, path)

    def test_optimize_route_no_path(self):
        start, end = (1, 1), (8, 8)
        obstacles = [(5, i) for i in range(0, 10)] # Vertical wall
        path = self.navigator.optimize_route(start, end, obstacles)
        self.assertIsNone(path)

    def test_optimize_route_out_of_bounds(self):
        with self.assertRaises(ValueError):
            self.navigator.optimize_route((0, 0), (11, 11), [])

if __name__ == '__main__':
    unittest.main()
