import pytest
import matplotlib.pyplot as plt
from field import Field, Drone
from plotting import (plot_field, plot_voronoi,
                      plot_weed_distribution_with_voronoi, plot_paths)

def test_plot_field():
    # Define parameters
    radius = 25
    drone_count = 2
    weed_centers = [[0, 0], [10, 10]]
    weed_cov = [[5, 0], [0, 5]]
    
    # Initialize field
    field = Field(radius, drone_count, weed_centers, weed_cov)

    # Plot the field
    plot_field(field)

    assert plt.gcf().number == 1

def test_plot_voronoi():
    # Define parameters
    radius = 25
    drone_count = 2
    weed_centers = [[0, 0], [10, 10]]
    weed_cov = [[5, 0], [0, 5]]

    # Initialize field
    field = Field(radius, drone_count, weed_centers, weed_cov)

    # Plot the Voronoi
    plot_voronoi(field)

    assert plt.gcf().number == 1
