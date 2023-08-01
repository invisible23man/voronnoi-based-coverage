import pytest
from field import Field, Drone

def test_field_initialization():
    # Use the parameters from your project
    radius = 25
    drone_count = 2
    weed_centers = [[0, 0], [10, 10]]
    weed_cov = [[5, 0], [0, 5]]

    # Initialize a Field object
    field = Field(radius, drone_count, weed_centers, weed_cov)

    # Assert that the object is of type Field
    assert isinstance(field, Field)
