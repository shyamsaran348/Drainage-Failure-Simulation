import numpy as np

class ElevationProvider:
    """
    Simulates or fetches elevation data for geographical coordinates.
    For this research, we use a synthetic gradient based on Chennai's topography
    (High in the west/south, low towards the Bay of Bengal in the east).
    """
    def __init__(self, baseline_elevation=10.0, gradient_x=-0.001, gradient_y=-0.0005, noise_scale=0.1):
        """
        baseline_elevation: Elevation at the reference point (m)
        gradient_x: change in elevation per degree longitude
        gradient_y: change in elevation per degree latitude
        """
        self.baseline = baseline_elevation
        self.grad_x = gradient_x
        self.grad_y = gradient_y
        self.noise = noise_scale
        # Reference point (roughly Velachery, Chennai)
        self.ref_lon = 80.22 
        self.ref_lat = 12.98

    def get_elevation(self, lon, lat):
        """
        Returns estimated elevation (meters).
        """
        dx = lon - self.ref_lon
        dy = lat - self.ref_lat
        
        # Base elevation based on gradient
        elev = self.baseline + (dx * self.grad_x * 111000) + (dy * self.grad_y * 111000)
        
        # Add a bit of local noise for realism
        elev += np.random.normal(0, self.noise)
        
        return max(0.5, elev) # Min elevation 0.5m

if __name__ == "__main__":
    provider = ElevationProvider()
    print(f"Elevation at ref: {provider.get_elevation(80.22, 12.98):.2f}m")
    print(f"Elevation 1km East: {provider.get_elevation(80.23, 12.98):.2f}m")
