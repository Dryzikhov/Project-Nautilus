import unittest
import numpy as np
from nautilus.ml.model import AIModel

class TestAIModel(unittest.TestCase):

    def setUp(self):
        self.model = AIModel(threshold=0.8)

    def test_identify_interesting_locations(self):
        # Create a sample image where some pixels are above the threshold
        image = np.array([
            [0.1, 0.2, 0.9],
            [0.95, 0.3, 0.4],
            [0.5, 0.98, 0.6]
        ])
        expected_locations = [(0, 2), (1, 0), (2, 1)]
        locations = self.model.identify_interesting_locations(image)

        # Sort both lists to ensure comparison is correct regardless of order
        self.assertCountEqual(locations, expected_locations)

    def test_identify_no_interesting_locations(self):
        image = np.zeros((5, 5))
        locations = self.model.identify_interesting_locations(image)
        self.assertEqual(len(locations), 0)

    def test_identify_all_interesting_locations(self):
        image = np.ones((2, 2)) * 0.9
        expected_locations = [(0, 0), (0, 1), (1, 0), (1, 1)]
        locations = self.model.identify_interesting_locations(image)
        self.assertCountEqual(locations, expected_locations)

    def test_input_type_error(self):
        with self.assertRaises(TypeError):
            self.model.identify_interesting_locations("not a numpy array")

if __name__ == '__main__':
    unittest.main()
