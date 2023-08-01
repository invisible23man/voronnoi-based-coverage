import numpy as np
from shapely.geometry import Point, Polygon

def create_grid(x_range, y_range, grid_resolution):
    x_values = np.arange(x_range[0], x_range[1] + grid_resolution, grid_resolution)
    y_values = np.arange(y_range[0], y_range[1] + grid_resolution, grid_resolution)
    grid_points = np.array([(x, y) for y in y_values for x in x_values])
    return grid_points

def create_circular_grid(center, radius, resolution):
    """Create a grid covering the circular field."""
    x_values = np.arange(-radius, radius + resolution, resolution)
    y_values = np.arange(-radius, radius + resolution, resolution)
    grid_points = np.array([(x, y) for x in x_values for y in y_values if np.sqrt(x**2 + y**2) <= radius])

    return grid_points

def assign_grid_to_regions(grid_points, centers):
    regions = [[] for _ in centers]
    for point in grid_points:
        distances = [np.linalg.norm(point - center) for center in centers]
        region_index = np.argmin(distances)
        regions[region_index].append(point)
    return regions

def generate_lawnmower_path_for_region(region_points, grid_resolution):
    path = []
    sorted_points = sorted(region_points, key=lambda x: (x[1], x[0]))
    current_y = sorted_points[0][1]
    current_path = []
    for point in sorted_points:
        if point[1] == current_y:
            current_path.append(point)
        else:
            if len(current_path) % 2 == 1:  # Reverse every other row
                current_path = current_path[::-1]
            path.extend(current_path)
            current_path = [point]
            current_y = point[1]
    path.extend(current_path)  # Add the last row
    return np.array(path)

def generate_lawnmower_paths(grid_points, centers, grid_resolution):
    regions = assign_grid_to_regions(grid_points, centers)
    paths = [generate_lawnmower_path_for_region(region, grid_resolution) for region in regions]
    return paths

def update_voronoi_centers(paths, weed_density, grid_points, centers):
    new_centers = []
    for path in paths:
        weed_concentration = np.array([weed_density[int(point[0]), int(point[1])] for point in path])
        mv = np.sum(weed_concentration)
        cx = np.sum(path[:, 0] * weed_concentration) / mv
        cy = np.sum(path[:, 1] * weed_concentration) / mv
        new_centers.append([cx, cy])
    return np.array(new_centers)
