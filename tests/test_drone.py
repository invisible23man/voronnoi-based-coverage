import pytest
from drone import Drone
def test_drone_initialization():
    # Initialize a Drone object
    drone = Drone(0, 0)

    # Assert that the object is of type Drone
    assert isinstance(drone, Drone)
