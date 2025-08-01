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
