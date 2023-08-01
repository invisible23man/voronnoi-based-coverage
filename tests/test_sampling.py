import pytest
import numpy as np
from sampling import create_weed_distribution, sample_weed_density

def test_create_weed_distribution():
    weed_centers = [[0, 0], [10, 10]]
    weed_cov = [[5, 0], [0, 5]]
    grid_points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])

    weed_distribution = create_weed_distribution(weed_centers, weed_cov, grid_points)

    assert len(weed_distribution) == len(grid_points)

def test_sample_weed_density():
    weed_distribution = np.array([1, 2, 3, 4])
    path_points = np.array([[0, 0], [1, 1]])
    grid_points = np.array([[0, 0], [1, 0], [0, 1], [1, 1]])
    grid_resolution = 1

    sampled_values = sample_weed_density(weed_distribution, path_points, grid_points, grid_resolution)

    assert sampled_values[0] == weed_distribution[0]
    assert sampled_values[1] == weed_distribution[3]
