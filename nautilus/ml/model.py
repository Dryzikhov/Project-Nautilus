import numpy as np

class AIModel:
    def __init__(self, weather_condition='clear', chemical_thresholds=None):
        self.weather_condition = weather_condition

        # --- Weights for Interesting Location Identification ---
        self.discovery_sensor_weights = {'image': 0.4, 'lidar': 0.4, 'chemical': 0.2}
        if self.weather_condition == 'fog':
            self.discovery_sensor_weights['image'] *= 0.3
            self.discovery_sensor_weights['lidar'] *= 0.5
        elif self.weather_condition == 'storm':
            self.discovery_sensor_weights['chemical'] *= 0.5

        total_discovery_weight = sum(self.discovery_sensor_weights.values())
        for sensor in self.discovery_sensor_weights:
            self.discovery_sensor_weights[sensor] /= total_discovery_weight

        # --- Weights for Obstacle Avoidance ---
        self.obstacle_sensor_weights = {'sonar': 0.6, 'lidar': 0.4}
        if self.weather_condition == 'fog':
            self.obstacle_sensor_weights['lidar'] *= 0.4 # LIDAR is less reliable
            self.obstacle_sensor_weights['sonar'] *= 1.2 # Sonar is more reliable
        elif self.weather_condition == 'storm':
            self.obstacle_sensor_weights['sonar'] *= 0.6 # Sonar is less reliable

        total_obstacle_weight = sum(self.obstacle_sensor_weights.values())
        for sensor in self.obstacle_sensor_weights:
            self.obstacle_sensor_weights[sensor] /= total_obstacle_weight

        if chemical_thresholds is None:
            self.chemical_thresholds = {'ph': (6.5, 8.5), 'salinity': (32, 37), 'temperature': (5, 20)}
        else:
            self.chemical_thresholds = chemical_thresholds

    # --- Methods for Interesting Location Identification ---
    def _analyze_image_for_discovery(self, image_data):
        return np.max(image_data)

    def _analyze_lidar_for_discovery(self, lidar_data):
        if not isinstance(lidar_data, np.ndarray) or lidar_data.size == 0: return 0.0
        std_dev = np.std(lidar_data)
        return max(0, 1 - (std_dev / 5.0))

    def _analyze_chemicals(self, chemical_data):
        anomalies = sum(1 for key, (min_val, max_val) in self.chemical_thresholds.items() if not (min_val <= chemical_data[key] <= max_val))
        return anomalies / len(self.chemical_thresholds)

    def fuse_discovery_data(self, image_data, lidar_data, chemical_data):
        if not isinstance(image_data, np.ndarray): raise TypeError("image_data must be a numpy array.")
        scores = {
            'image': self._analyze_image_for_discovery(image_data),
            'lidar': self._analyze_lidar_for_discovery(lidar_data),
            'chemical': self._analyze_chemicals(chemical_data)
        }
        fused_score = sum(scores[s] * self.discovery_sensor_weights[s] for s in scores)
        return fused_score, scores

    def identify_interesting_locations(self, image_data, lidar_data, chemical_data):
        fused_confidence, individual_scores = self.fuse_discovery_data(image_data, lidar_data, chemical_data)
        return {"is_interesting": fused_confidence > 0.6, "fused_confidence": fused_confidence, "individual_scores": individual_scores}

    # --- Methods for Obstacle Avoidance ---
    def _analyze_sonar_for_obstacle(self, sonar_data):
        """Returns a risk score (0-1) based on distance. Closer is riskier."""
        distance = sonar_data['distance']
        # Risk increases exponentially as distance decreases
        return max(0, 1 - (distance / 50.0)) # 50m is the 'safe' distance

    def _analyze_lidar_for_obstacle(self, lidar_data):
        """Returns a risk score (0-1) based on object density."""
        if not isinstance(lidar_data, np.ndarray) or lidar_data.size == 0: return 0.0
        std_dev = np.std(lidar_data)
        # Lower std dev -> denser object -> higher risk
        return max(0, 1 - (std_dev / 3.0)) # Lower threshold for obstacles

    def assess_obstacle_risk(self, sonar_data, lidar_data):
        """
        Fuses Sonar and LIDAR data to assess the risk of an obstacle.
        Returns a single, fused risk score (0-1).
        """
        risk_scores = {
            'sonar': self._analyze_sonar_for_obstacle(sonar_data),
            'lidar': self._analyze_lidar_for_obstacle(lidar_data)
        }

        fused_risk = sum(risk_scores[s] * self.obstacle_sensor_weights[s] for s in risk_scores)
        return min(fused_risk, 1.0) # Cap risk at 1.0
