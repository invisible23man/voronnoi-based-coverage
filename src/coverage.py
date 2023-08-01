import numpy as np
from shapely.geometry import Point, Polygon
from drone import Drone

from sampling import estimated_measurements, true_measurements

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

def generate_lawnmower_path_for_region(region_points, grid_resolution, time_budget):
    """Generate a lawnmower path for a single Voronoi region using assigned grid points."""
    path = []
    sorted_points = sorted(region_points, key=lambda x: (x[1], x[0]))
    current_y = sorted_points[0][1]
    current_path = []
    for point in sorted_points:
        if len(path) + len(current_path) + 1 > time_budget:  # Stop if adding another point would exceed the time budget
            break
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

def generate_lawnmower_paths(grid_points, centers, grid_resolution, total_time_budget):
    """Generate lawnmower paths for all Voronoi regions."""
    time_budget_per_drone = total_time_budget / len(centers)
    regions = assign_grid_to_regions(grid_points, centers)
    paths = [generate_lawnmower_path_for_region(region, grid_resolution, time_budget_per_drone) for region in regions]
    return paths, regions

def update_voronoi_centers(paths, regions, true_weed_density, drones:Drone, grid_points, centers, method='kde', estimation=True):
    new_centers = []
    for path, region, drone in zip(paths, regions, drones):
        # Sample the true weed density using the sensor model
        sampled_weed_concentration = true_measurements(true_weed_density, path)

        if estimation:
            # Update sensor model using the samppled measurements
            drone.sensor_estimation_model.fit(path,sampled_weed_concentration)
            
            # Generate remaining path in the region
            remaining_path_points = remaining_path(region, path)

            if len(remaining_path_points)>0:
                # Estimate the weed density using the selected method
                estimated_weed_concentration= estimated_measurements(remaining_path_points, drone.sensor_estimation_model, method='kde')
            else:
                remaining_path_points = np.empty_like(path)
                estimated_weed_concentration = np.empty_like(sampled_weed_concentration)
                print("Partiiton Already Covered in Sampling Time")

            # Get Complete Picture
            path = np.concatenate((path, remaining_path_points))
            estimated_weed_density = np.concatenate((sampled_weed_concentration, estimated_weed_concentration))
        else:
            estimated_weed_density = sampled_weed_concentration

        # Compute mean coordinates weighted by the estimated weed concentration
        mv = np.sum(estimated_weed_density)
        cx = np.sum(path[:, 0] * estimated_weed_density) / mv
        cy = np.sum(path[:, 1] * estimated_weed_density) / mv

        # Check if new center is NaN
        if np.isnan(cx) or np.isnan(cy):
            if len(remaining_path_points) > 0:
                new_center = remaining_path_points[0]
            else:
                print("No remaining path points available. Drone position will not be updated.")
                new_center = drone.get_position()  # Set new center as current position if no remaining path points
        else:
            new_center = [cx, cy]

        # Append new center to the list
        new_centers.append(new_center)

    return np.array(new_centers)

def remaining_path(region, sampled_path):
    """Generate the remaining path in the region after subtracting the sampled path."""
    return np.array([point for point in region if point not in sampled_path])

def calculate_repulsion_forces(drone_positions):
    repulsion_forces = np.zeros_like(drone_positions)
    for i in range(len(drone_positions)):
        for j in range(i):
            # Calculate the vector from drone j to drone i
            diff_vector = drone_positions[i] - drone_positions[j]
            # Calculate the distance between the drones
            distance = np.linalg.norm(diff_vector)
            # Calculate the repulsion force
            repulsion_force = diff_vector / distance**3
            # Add the repulsion force to the forces on both drones
            repulsion_forces[i] += repulsion_force
            repulsion_forces[j] -= repulsion_force
    return repulsion_forces
