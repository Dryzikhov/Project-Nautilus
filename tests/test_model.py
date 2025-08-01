import unittest
import numpy as np
from nautilus.ml.model import AIModel

class TestAIModel(unittest.TestCase):

    def setUp(self):
        """Set up mock data for testing."""
        self.clear_model = AIModel(weather_condition='clear')
        self.fog_model = AIModel(weather_condition='fog')
        self.storm_model = AIModel(weather_condition='storm')

        # Mock sensor data
        self.high_risk_sonar = {'distance': 10, 'angle': 20}
        self.low_risk_sonar = {'distance': 80, 'angle': 10}
        self.dense_lidar = np.random.normal(loc=0, scale=1.0, size=(50, 3)) # Low std -> high risk/confidence
        self.sparse_lidar = np.random.normal(loc=0, scale=5.0, size=(50, 3)) # High std -> low risk/confidence
        self.interesting_image = np.array([[0.1, 0.9], [0.2, 0.3]])
        self.boring_image = np.zeros((2, 2))
        self.anomalous_chemical = {'ph': 6.0, 'salinity': 45, 'temperature': 25}
        self.normal_chemical = {'ph': 8.0, 'salinity': 35, 'temperature': 15}

    def test_weight_adjustment(self):
        """Test if sensor weights are adjusted correctly for weather."""
        # In fog, lidar and image weights for discovery should be lower
        self.assertLess(self.fog_model.discovery_sensor_weights['lidar'], self.clear_model.discovery_sensor_weights['lidar'])
        self.assertLess(self.fog_model.discovery_sensor_weights['image'], self.clear_model.discovery_sensor_weights['image'])

        # In a storm, chemical weights for discovery should be lower
        self.assertLess(self.storm_model.discovery_sensor_weights['chemical'], self.clear_model.discovery_sensor_weights['chemical'])

        # In fog, lidar weight for obstacles should be lower and sonar higher
        self.assertLess(self.fog_model.obstacle_sensor_weights['lidar'], self.clear_model.obstacle_sensor_weights['lidar'])
        self.assertGreater(self.fog_model.obstacle_sensor_weights['sonar'], self.clear_model.obstacle_sensor_weights['sonar'])

    def test_assess_obstacle_risk(self):
        """Test the obstacle risk assessment logic."""
        # High risk scenario
        high_risk = self.clear_model.assess_obstacle_risk(self.high_risk_sonar, self.dense_lidar)
        self.assertGreater(high_risk, 0.7)

        # Low risk scenario
        low_risk = self.clear_model.assess_obstacle_risk(self.low_risk_sonar, self.sparse_lidar)
        self.assertLess(low_risk, 0.3)

        # Test risk assessment in fog (LIDAR is less trusted)
        risk_in_fog = self.fog_model.assess_obstacle_risk(self.low_risk_sonar, self.dense_lidar)
        risk_in_clear = self.clear_model.assess_obstacle_risk(self.low_risk_sonar, self.dense_lidar)
        # Since dense_lidar indicates high risk, but is less trusted in fog, the overall risk should be lower in fog.
        self.assertLess(risk_in_fog, risk_in_clear)

    def test_identify_interesting_locations(self):
        """Test the interesting location identification logic."""
        # Scenario with strong signals from all sensors
        findings = self.clear_model.identify_interesting_locations(
            self.interesting_image, self.dense_lidar, self.anomalous_chemical
        )
        self.assertTrue(findings['is_interesting'])
        self.assertGreater(findings['fused_confidence'], 0.6)

        # Scenario with weak signals
        findings = self.clear_model.identify_interesting_locations(
            self.boring_image, self.sparse_lidar, self.normal_chemical
        )
        self.assertFalse(findings['is_interesting'])
        self.assertLess(findings['fused_confidence'], 0.5)

        # Test fusion in fog (image is less trusted)
        confidence_in_clear = self.clear_model.identify_interesting_locations(
            self.interesting_image, self.sparse_lidar, self.normal_chemical
        )['fused_confidence']

        confidence_in_fog = self.fog_model.identify_interesting_locations(
            self.interesting_image, self.sparse_lidar, self.normal_chemical
        )['fused_confidence']
        # Since the interesting_image is a strong signal, but less trusted in fog, the overall confidence should be lower.
        self.assertLess(confidence_in_fog, confidence_in_clear)

if __name__ == '__main__':
    unittest.main()
