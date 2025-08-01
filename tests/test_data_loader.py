import unittest
import numpy as np
from nautilus.ml.data_loader import DataLoader

class TestDataLoader(unittest.TestCase):

    def test_initialization(self):
        """Tests if the DataLoader initializes correctly."""
        loader = DataLoader(weather_condition='clear')
        self.assertEqual(loader.weather_condition, 'clear')
        with self.assertRaises(ValueError):
            DataLoader(weather_condition='sunny')

    def test_load_data_clear(self):
        """Tests data loading in 'clear' weather."""
        # In clear weather, data should be relatively 'clean'.
        # We can't test random output, but we can test the expected types and shapes.
        loader = DataLoader(weather_condition='clear')

        sonar_data = loader.load_sonar_data()
        self.assertIsInstance(sonar_data, dict)

        image_data = loader.load_underwater_image()
        self.assertEqual(image_data.shape, (128, 128))

        lidar_data = loader.load_lidar_data(num_points=100)
        self.assertEqual(lidar_data.shape, (100, 3))

    def test_load_data_in_fog(self):
        """Tests the effect of 'fog' on sensor data."""
        # In fog, LIDAR should be more scattered (higher std dev) and images less clear.
        np.random.seed(42) # for reproducibility
        clear_loader = DataLoader(weather_condition='clear')
        fog_loader = DataLoader(weather_condition='fog')

        clear_lidar = clear_loader.load_lidar_data()
        fog_lidar = fog_loader.load_lidar_data()
        # Higher std dev indicates more scatter
        self.assertGreater(np.std(fog_lidar), np.std(clear_lidar))

        clear_image = clear_loader.load_underwater_image()
        fog_image = fog_loader.load_underwater_image()
        # Lower contrast (variance) in fog
        self.assertLess(np.var(fog_image), np.var(clear_image))

    def test_load_data_in_storm(self):
        """Tests the effect of 'storm' on sensor data."""
        # In a storm, Sonar should be noisier and LIDAR may lose points.
        np.random.seed(42)
        storm_loader = DataLoader(weather_condition='storm')

        # Test for LIDAR data loss
        lidar_data = storm_loader.load_lidar_data(num_points=100)
        self.assertEqual(lidar_data.shape[0], 70) # Expecting 30% data loss

        # Test for Sonar noise (hard to test precisely, but we can check if it runs)
        sonar_data = storm_loader.load_sonar_data()
        self.assertIn('distance', sonar_data)

        # Test for chemical data variability (hard to test precisely)
        chem_data = storm_loader.load_chemical_data()
        self.assertIn('ph', chem_data)

if __name__ == '__main__':
    unittest.main()
