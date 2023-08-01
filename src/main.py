import pickle
from field import Field
from coverage import (create_circular_grid, 
                      generate_lawnmower_paths, update_voronoi_centers)
from plotting import (plot_field, plot_voronoi, plot_voronoi_iterations_3d,
                      plot_weed_distribution_with_voronoi, plot_paths,
                      plot_voronoi_iterations)

# Define parameters
radius = 25
drone_count = 10
weed_centers = [[-15, -15], [15, 15]]
weed_cov = [[5, 0], [0, 5]]
iterations = 10

# Initialize field
field = Field(radius, drone_count, weed_centers, weed_cov)

# Create grid for the entire field
grid_points = create_circular_grid((0, 0), 25, 1)

# Iterations
iterations_data = []
for i in range(iterations):
    centers = field.get_drone_positions()
    paths = generate_lawnmower_paths(grid_points, centers, 1)
    new_centers = update_voronoi_centers(paths, field.weeds, grid_points, centers)
    field.update_drone_positions(new_centers)
    iterations_data.append((centers, paths, new_centers))

# plot_field(field)
# plot_voronoi(field)
# plot_weed_distribution_with_voronoi(field)
# field.plot_3d()
# Plot lawnmower paths using grid for all Voronoi regions
# plot_paths(paths, 'Lawnmower Paths (Grid-Based Approach)', weed_centers)

# Save iterations data to a file
with open("./results/runs/iterations_data.pkl", "wb") as file:
    pickle.dump(iterations_data, file)


# Generate GIF
plot_voronoi_iterations(iterations_data, field.X, field.Y, field.weeds)
plot_voronoi_iterations_3d(iterations_data, field.X, field.Y, field.weeds)
