import unittest
import numpy as np
from nautilus.ml.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):

    def setUp(self):
        self.data_loader = DataLoader()

    def test_load_sonar_data(self):
        sonar_data = self.data_loader.load_sonar_data()
        self.assertIsInstance(sonar_data, dict)
        self.assertIn('distance', sonar_data)
        self.assertIn('angle', sonar_data)
        self.assertIsInstance(sonar_data['distance'], float)
        self.assertIsInstance(sonar_data['angle'], float)

    def test_load_bathymetric_map(self):
        b_map = self.data_loader.load_bathymetric_map()
        self.assertIsInstance(b_map, np.ndarray)
        self.assertEqual(b_map.shape, (100, 100))

    def test_load_underwater_image(self):
        image = self.data_loader.load_underwater_image()
        self.assertIsInstance(image, np.ndarray)
        self.assertEqual(image.shape, (128, 128))

    def test_load_lidar_data(self):
        lidar_data = self.data_loader.load_lidar_data(num_points=50)
        self.assertIsInstance(lidar_data, np.ndarray)
        self.assertEqual(lidar_data.shape, (50, 3))

    def test_load_chemical_data(self):
        chemical_data = self.data_loader.load_chemical_data()
        self.assertIsInstance(chemical_data, dict)
        self.assertIn('ph', chemical_data)
        self.assertIn('salinity', chemical_data)
        self.assertIn('temperature', chemical_data)
        self.assertIsInstance(chemical_data['ph'], float)
        self.assertIsInstance(chemical_data['salinity'], float)
        self.assertIsInstance(chemical_data['temperature'], float)

if __name__ == '__main__':
    unittest.main()
