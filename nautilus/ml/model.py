import numpy as np

class AIModel:
    def __init__(self, threshold=0.9):
        self.threshold = threshold

    def identify_interesting_locations(self, image_data):
        """
        Simulates identification of interesting locations from image data.
        Returns a list of coordinates (y, x) where pixel intensity is above a threshold.
        """
        if not isinstance(image_data, np.ndarray):
            raise TypeError("image_data must be a numpy array.")

        # Find pixels with intensity > threshold
        interesting_points = np.where(image_data > self.threshold)
        # Return as a list of (y, x) coordinates
        return list(zip(interesting_points[0], interesting_points[1]))
