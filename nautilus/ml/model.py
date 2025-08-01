import numpy as np

class AIModel:
    def __init__(self, image_threshold=0.9, lidar_threshold=5, chemical_thresholds=None):
        self.image_threshold = image_threshold
        self.lidar_threshold = lidar_threshold
        # Set default chemical thresholds if not provided
        if chemical_thresholds is None:
            self.chemical_thresholds = {
                'ph': (6.5, 8.5),      # Normal pH range
                'salinity': (32, 37),  # Normal salinity range
                'temperature': (5, 20) # Normal temperature range
            }
        else:
            self.chemical_thresholds = chemical_thresholds

    def analyze_lidar_data(self, lidar_data):
        """
        Analyzes LIDAR data to detect dense point clusters.
        Returns True if a dense object is detected.
        """
        if not isinstance(lidar_data, np.ndarray):
            raise TypeError("lidar_data must be a numpy array.")

        # Simple density check: if the standard deviation of points is small,
        # it implies they are tightly clustered.
        if np.std(lidar_data) < self.lidar_threshold:
            return True
        return False

    def analyze_chemical_data(self, chemical_data):
        """
        Analyzes chemical data for values outside normal ranges.
        Returns a list of anomalies found.
        """
        anomalies = []
        for key, (min_val, max_val) in self.chemical_thresholds.items():
            if not (min_val <= chemical_data[key] <= max_val):
                anomalies.append(key)
        return anomalies

    def identify_interesting_locations(self, image_data, lidar_data, chemical_data):
        """
        Simulates identification of interesting locations by fusing sensor data.
        An interesting location is identified if any of the sensors detect something significant.
        Returns a dictionary with findings.
        """
        if not isinstance(image_data, np.ndarray):
            raise TypeError("image_data must be a numpy array.")

        findings = {
            "image_features": [],
            "lidar_object_detected": False,
            "chemical_anomalies": []
        }

        # 1. Analyze Image Data
        interesting_points = np.where(image_data > self.image_threshold)
        findings["image_features"] = list(zip(interesting_points[0], interesting_points[1]))

        # 2. Analyze LIDAR Data
        if self.analyze_lidar_data(lidar_data):
            findings["lidar_object_detected"] = True

        # 3. Analyze Chemical Data
        findings["chemical_anomalies"] = self.analyze_chemical_data(chemical_data)

        return findings
