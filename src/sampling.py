from scipy.spatial.distance import cdist
from scipy.linalg import det, inv
from math import sqrt, pi
import numpy as np

def sample_weed_density(weed_distribution, path_points, grid_points, grid_resolution):
    """Sample the weed density at each point in the path."""
    sampled_values = []
    for point in path_points:
        distances = np.linalg.norm(grid_points - point, axis=1)
        closest_point_index = np.argmin(distances)
        if distances[closest_point_index] <= grid_resolution:
            sampled_values.append(weed_distribution[closest_point_index])
        else:
            sampled_values.append(0)  # No weed detected if the point is not within the grid resolution
    return np.array(sampled_values)

def true_measurements(true_weed_density, sampled_points):
    """
    This function represents the sensor model. It should take in the true weed density and the sampled points and return an estimate of the weed density at the sampled points.
    """
    # Here we simply return the true weed density at the sampled points.
    # This is a placeholder and should be replaced with an actual sensor model.
    return np.array([true_weed_density[int(point[0]), int(point[1])] for point in sampled_points])

def estimated_measurements(sampled_points, sensor, method='kde'):
    if method == 'kde':
        log_density = sensor.score_samples(sampled_points)
        estimated_density = np.exp(log_density)
    elif method == 'dpmm':
        estimated_density = sensor.predict(sampled_points)
    else:
        raise ValueError(f"Unknown method: {method}")

    return estimated_density