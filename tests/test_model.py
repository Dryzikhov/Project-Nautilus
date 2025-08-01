import unittest
import numpy as np
from nautilus.ml.model import AIModel

class TestAIModel(unittest.TestCase):

    def setUp(self):
        self.model = AIModel(image_threshold=0.8, lidar_threshold=2.0)
        # Dummy data for tests
        self.normal_image = np.zeros((5, 5))
        self.interesting_image = np.zeros((5, 5))
        self.interesting_image[2, 2] = 0.9

        self.sparse_lidar = np.array([[10, 20, 30], [-10, -20, -30], [5, -15, 25]]) # High std dev
        self.dense_lidar = np.random.rand(10, 3) # Low std dev

        self.normal_chemical = {'ph': 8.0, 'salinity': 35, 'temperature': 15}
        self.anomalous_chemical = {'ph': 6.0, 'salinity': 45, 'temperature': 25}

    def test_analyze_lidar_data_dense(self):
        self.assertTrue(self.model.analyze_lidar_data(self.dense_lidar))

    def test_analyze_lidar_data_sparse(self):
        self.assertFalse(self.model.analyze_lidar_data(self.sparse_lidar))

    def test_analyze_chemical_data_normal(self):
        anomalies = self.model.analyze_chemical_data(self.normal_chemical)
        self.assertEqual(len(anomalies), 0)

    def test_analyze_chemical_data_anomalous(self):
        anomalies = self.model.analyze_chemical_data(self.anomalous_chemical)
        self.assertCountEqual(anomalies, ['ph', 'salinity', 'temperature'])

    def test_identify_interesting_locations_fusion(self):
        # Test case 1: Only image has interesting features
        findings = self.model.identify_interesting_locations(
            self.interesting_image, self.sparse_lidar, self.normal_chemical
        )
        self.assertEqual(len(findings["image_features"]), 1)
        self.assertFalse(findings["lidar_object_detected"])
        self.assertEqual(len(findings["chemical_anomalies"]), 0)

        # Test case 2: Only LIDAR detects an object
        findings = self.model.identify_interesting_locations(
            self.normal_image, self.dense_lidar, self.normal_chemical
        )
        self.assertEqual(len(findings["image_features"]), 0)
        self.assertTrue(findings["lidar_object_detected"])
        self.assertEqual(len(findings["chemical_anomalies"]), 0)

        # Test case 3: Only chemical anomalies are found
        findings = self.model.identify_interesting_locations(
            self.normal_image, self.sparse_lidar, self.anomalous_chemical
        )
        self.assertEqual(len(findings["image_features"]), 0)
        self.assertFalse(findings["lidar_object_detected"])
        self.assertEqual(len(findings["chemical_anomalies"]), 3)

        # Test case 4: All sensors detect something
        findings = self.model.identify_interesting_locations(
            self.interesting_image, self.dense_lidar, self.anomalous_chemical
        )
        self.assertEqual(len(findings["image_features"]), 1)
        self.assertTrue(findings["lidar_object_detected"])
        self.assertEqual(len(findings["chemical_anomalies"]), 3)

    def test_input_type_error(self):
        with self.assertRaises(TypeError):
            self.model.identify_interesting_locations("not an array", self.dense_lidar, self.normal_chemical)
        with self.assertRaises(TypeError):
            self.model.analyze_lidar_data("not an array")

if __name__ == '__main__':
    unittest.main()
