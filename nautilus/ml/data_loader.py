import numpy as np

class DataLoader:
    def __init__(self, weather_condition='clear', data_path='data/'):
        self.data_path = data_path
        self.weather_condition = weather_condition
        if self.weather_condition not in ['clear', 'fog', 'storm']:
            raise ValueError("weather_condition must be 'clear', 'fog', or 'storm'")

    def load_sonar_data(self):
        """
        Simulates sonar data, affected by weather conditions.
        In a 'storm', readings are noisier.
        """
        base_distance = np.random.uniform(10, 100)
        noise = 0
        if self.weather_condition == 'storm':
            noise = np.random.normal(0, 15)  # Add significant noise

        return {"distance": max(0, base_distance + noise), "angle": np.random.uniform(-45, 45)}

    def load_bathymetric_map(self):
        # Simulate a 100x100 map with random depth
        return np.random.rand(100, 100) * 500

    def load_underwater_image(self):
        """
        Simulates a 128x128 grayscale image, affected by weather.
        In 'fog', the image has lower contrast and more noise.
        """
        image = np.random.rand(128, 128)
        if self.weather_condition == 'fog':
            # Lower contrast and add noise
            image = image * 0.5 + np.random.normal(0.2, 0.1, image.shape)
        return np.clip(image, 0, 1)

    def load_lidar_data(self, num_points=100):
        """
        Simulates a 3D point cloud, affected by weather.
        - 'fog': More scattered points.
        - 'storm': Fewer points returned.
        """
        scale = 2.0
        if self.weather_condition == 'fog':
            scale = 4.0  # More scattered
        if self.weather_condition == 'storm':
            num_points = int(num_points * 0.7)  # 30% data loss

        cluster_center = np.random.uniform(-5, 5, size=3)
        return cluster_center + np.random.normal(scale=scale, size=(num_points, 3))

    def load_chemical_data(self):
        """
        Simulates chemical sensor readings, affected by weather.
        In a 'storm', readings are more variable.
        """
        variability_multiplier = 1.0
        if self.weather_condition == 'storm':
            variability_multiplier = 2.5 # Higher variability

        is_anomaly = np.random.rand() < 0.05
        if is_anomaly:
            return {
                "ph": round(np.random.uniform(5, 6) + np.random.normal(0, 0.2 * variability_multiplier), 2),
                "salinity": round(np.random.uniform(40, 45) + np.random.normal(0, 1 * variability_multiplier), 2),
                "temperature": round(np.random.uniform(25, 30) + np.random.normal(0, 2 * variability_multiplier), 1),
            }
        else:
            return {
                "ph": round(np.random.uniform(7.8, 8.2) + np.random.normal(0, 0.1 * variability_multiplier), 2),
                "salinity": round(np.random.uniform(34, 36) + np.random.normal(0, 0.5 * variability_multiplier), 2),
                "temperature": round(np.random.uniform(10, 15) + np.random.normal(0, 1 * variability_multiplier), 1),
            }
