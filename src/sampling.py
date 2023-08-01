import numpy as np
from scipy.stats import multivariate_normal

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

def update_voronoi_centers(paths, weed_distribution, grid_points, grid_resolution):
    new_centers = []
    for path in paths:
        weed_densities = sample_weed_density(weed_distribution, path, grid_points, grid_resolution)
        mv = np.sum(weed_densities)
        if mv == 0:  # If there are no weeds in the path, the center does not change
            new_center = np.mean(path, axis=0)
        else:
            cx = np.sum(path[:, 0] * weed_densities) / mv
            cy = np.sum(path[:, 1] * weed_densities) / mv
            new_center = np.array([cx, cy])
        new_centers.append(new_center)
    return np.array(new_centers)
