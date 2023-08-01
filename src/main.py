import pickle
from tqdm import tqdm
from field import Field
from coverage import (create_circular_grid, 
                      generate_lawnmower_paths, update_voronoi_centers)
from plotting import (plot_field, plot_voronoi, plot_voronoi_iterations_3d,
                      plot_weed_distribution_with_voronoi, plot_paths,
                      plot_voronoi_iterations)
from housekeeping import *

# Define parameters
radius = 25
drone_count = 10
weed_centers = [[-15, -15], [15, 15]]
weed_cov = [[5, 0], [0, 5]]
iterations = 15
total_time_budget = 100
grid_resolution = 1
sensor_estimation_model = 'kde'
estimation = True

iteration_result_path = os.path.join(results_directory,f"{sensor_estimation_model}-iterations_data.pkl")
plot_path_2d = os.path.join(plots_directory,f'{sensor_estimation_model}-drone_movement_2d.gif')
plot_path_3d = os.path.join(plots_directory,f'{sensor_estimation_model}-drone_movement_3d.gif')

# Initialize field
field = Field(radius, drone_count, weed_centers, weed_cov, sensor_estimation_model)

# Create grid for the entire field
grid_points = create_circular_grid((0, 0), radius, grid_resolution)

# Iterations
iterations_data = []
for i in tqdm(range(iterations)):
    centers = field.get_drone_positions()
    paths, regions = generate_lawnmower_paths(grid_points, centers, grid_resolution, total_time_budget)
    new_centers = update_voronoi_centers(paths, regions, field.weeds, field.drones, 
                                         grid_points, centers, sensor_estimation_model, estimation)
    field.update_drone_positions(new_centers)
    iterations_data.append((centers, paths, new_centers))

# plot_field(field)
# plot_voronoi(field)
# plot_weed_distribution_with_voronoi(field)
# field.plot_3d()
# Plot lawnmower paths using grid for all Voronoi regions
# plot_paths(paths, 'Lawnmower Paths (Grid-Based Approach)', weed_centers)

# Save iterations data to a file
with open(iteration_result_path, "wb") as file:
    pickle.dump(iterations_data, file)

# Generate GIF
plot_voronoi_iterations(iterations_data, field.X, field.Y, field.weeds, plot_path_2d, interval=200)
plot_voronoi_iterations_3d(iterations_data, field.X, field.Y, field.weeds, plot_path_3d, interval=200)
