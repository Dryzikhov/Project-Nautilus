import numpy as np

class DataLoader:
    def __init__(self, data_path='data/'):
        self.data_path = data_path

    def load_sonar_data(self):
        # Simulate sonar data
        return {"distance": np.random.uniform(10, 100), "angle": np.random.uniform(-45, 45)}

    def load_bathymetric_map(self):
        # Simulate a 100x100 map with random depth
        return np.random.rand(100, 100) * 500

    def load_underwater_image(self):
        # Simulate a 128x128 grayscale image
        return np.random.rand(128, 128)

    def load_lidar_data(self, num_points=100):
        # Simulate a 3D point cloud: num_points x [x, y, z]
        # Points are clustered around a potential object for realism
        cluster_center = np.random.uniform(-5, 5, size=3)
        return cluster_center + np.random.normal(scale=2.0, size=(num_points, 3))

    def load_chemical_data(self):
        # Simulate chemical sensor readings with occasional anomalies
        is_anomaly = np.random.rand() < 0.05  # 5% chance of an anomaly
        if is_anomaly:
            return {
                "ph": round(np.random.uniform(5, 6), 2),          # Anomalous pH
                "salinity": round(np.random.uniform(40, 45), 2),  # Anomalous salinity
                "temperature": round(np.random.uniform(25, 30), 1), # Anomalous temperature
            }
        else:
            return {
                "ph": round(np.random.uniform(7.8, 8.2), 2),     # Normal sea water pH
                "salinity": round(np.random.uniform(34, 36), 2), # Normal salinity (PSU)
                "temperature": round(np.random.uniform(10, 15), 1),# Normal temperature (Celsius)
            }
