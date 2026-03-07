import numpy as np

def get_rainfall_intensity(t, duration=60, peak_intensity=10.0, profile_type='gaussian'):
    """
    Returns rainfall intensity (m^3/s per node) at time t.
    """
    if t < 0 or t > duration:
        return 0.0
    
    if profile_type == 'constant':
        return peak_intensity
    
    if profile_type == 'gaussian':
        # Simple bell curve centered at duration/2
        mu = duration / 2
        sigma = duration / 6
        intensity = peak_intensity * np.exp(-((t - mu)**2) / (2 * sigma**2))
        return intensity
    
    return 0.0

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    times = np.linspace(0, 100, 100)
    intensities = [get_rainfall_intensity(t) for t in times]
    plt.plot(times, intensities)
    plt.show()
