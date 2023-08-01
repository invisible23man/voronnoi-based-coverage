from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import multivariate_normal
from drone import Drone
from voronoi import voronoi_finite_polygons_2d
from scipy.spatial import Voronoi

class Field:
    """Class representing a circular field."""
    def __init__(self, radius, drone_count, weed_centers, weed_cov, sensor_estimation_model):
        self.radius = radius
        self.drone_count = drone_count
        self.sensor_estimation_model = sensor_estimation_model
        self.drones:Drone = self._distribute_drones()
        self.weed_centers = weed_centers
        self.weed_cov = weed_cov
        self.X, self.Y, self.weeds = self._generate_weed_distribution()
        self.vor = self._compute_voronoi()

    def _distribute_drones(self):
        """Distribute drones evenly within the circle."""
        drones = []
        r = np.sqrt((self.radius**2) / self.drone_count)  # Radius of the smaller circle
        for i in range(self.drone_count):
            angle = 2 * np.pi * i / self.drone_count  # Equally spaced angles
            x = r * np.cos(angle) + np.random.uniform(-0.001, 0.001)
            y = r * np.sin(angle) + np.random.uniform(-0.001, 0.001)
            drones.append(Drone(x, y, self.sensor_estimation_model))
        return drones

    def _generate_weed_distribution(self):
        """Generate a weed concentration distribution within a circular boundary using multivariate normal distributions."""
        x = np.arange(-self.radius, self.radius, 0.1)
        y = np.arange(-self.radius, self.radius, 0.1)
        X, Y = np.meshgrid(x, y)
        weeds = np.zeros(X.shape)
        for center in self.weed_centers:
            rv = multivariate_normal(center, self.weed_cov)
            weeds += rv.pdf(np.dstack((X, Y)))
        return X, Y, weeds

    def _compute_voronoi(self):
        """Compute Voronoi tesselation for drone positions."""
        positions = self.get_drone_positions()
        return Voronoi(positions)

    def get_drone_positions(self):
        """Get drone positions as an array."""
        positions = np.array([[drone.x, drone.y] for drone in self.drones])
        return positions

    def update_drone_positions(self, new_positions):
        """Update the positions of drones and recompute the Voronoi diagram."""
        for drone, new_position in zip(self.drones, new_positions):
            drone.update_position(new_position[0], new_position[1])
        self.vor = self._compute_voronoi()

    def plot_3d(self):
        """Plot a 3D representation of the field, with drones and Voronoi partitions at a height of 5m."""
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot_surface(self.X, self.Y, self.weeds, cmap='YlGn', alpha=0.5)
        positions = self.get_drone_positions()
        ax.scatter(positions[:, 0], positions[:, 1], 5, color='r', label='Drones')
        ax.set_title('3D Representation of the Field')
        plt.show()