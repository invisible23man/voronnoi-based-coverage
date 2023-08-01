import pytest
import numpy as np
from coverage import (create_grid, assign_grid_to_regions,
                      generate_lawnmower_path_for_region,
                      generate_lawnmower_paths, update_voronoi_centers)

def test_create_grid():
    x_range = (-1, 1)
    y_range = (-1, 1)
    grid_resolution = 1
    grid_points = create_grid(x_range, y_range, grid_resolution)

    assert len(grid_points) == 9

def test_assign_grid_to_regions():
    grid_points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    centers = np.array([[0, 0], [1, 1]])
    regions = assign_grid_to_regions(grid_points, centers)

    assert len(regions) == len(centers)
