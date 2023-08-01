import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

from voronoi import voronoi_finite_polygons_2d

def plot_field(field):
    fig, ax = plt.subplots()
    c = ax.contourf(field.X, field.Y, field.weeds, cmap='YlGn')
    fig.colorbar(c)
    plt.title('Ground Truth of Weed Distribution')
    plt.grid(True)
    plt.show()

def plot_voronoi(field):
    regions, vertices = voronoi_finite_polygons_2d(field.vor, field.radius)
    for region in regions:
        polygon = vertices[region]
        plt.fill(*zip(*polygon), alpha=0.4)
    positions = field.get_drone_positions()
    plt.plot(positions[:, 0], positions[:, 1], 'ko')
    plt.xlim(-field.radius, field.radius); plt.ylim(-field.radius, field.radius)
    plt.title('Voronoi Partitions (Colored) with Drone Positions')
    plt.show()

def plot_weed_distribution_with_voronoi(field):
    fig, ax = plt.subplots()
    c = ax.contourf(field.X, field.Y, field.weeds, cmap='YlGn')
    positions = field.get_drone_positions()
    ax.scatter(positions[:, 0], positions[:, 1], color='r', label='Drones')
    regions, vertices = voronoi_finite_polygons_2d(field.vor, field.radius)
    for region in regions:
        polygon = vertices[region]
        plt.plot(*zip(*polygon), 'k-')
    plt.title('Overlay of Weed Distribution, Drone Positions and Voronoi Partitions')
    plt.grid(True)
    plt.show()


def plot_paths(paths, title, weed_centers):
    """Plot the given paths."""
    weed_centers = np.array(weed_centers)
    plt.figure(figsize=(6, 6))
    for path in paths:
        plt.plot(path[:, 0], path[:, 1])
    plt.scatter(weed_centers[:, 0], weed_centers[:, 1], color='g', label='Weed Centers')
    plt.xlim(-30, 30); plt.ylim(-30, 30)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_voronoi_iterations(iterations_data, X, Y, weeds, path, interval=2000):
    fig, ax = plt.subplots()

    def animate(i):
        ax.clear()
        centers, paths, new_centers = iterations_data[i]
        c = ax.contourf(X, Y, weeds, cmap='YlGn')
        ax.scatter(centers[:, 0], centers[:, 1], color='r', label='Old Drone Positions')
        ax.scatter(new_centers[:, 0], new_centers[:, 1], color='b', label='New Drone Positions')
        ax.legend()
        ax.set_xlim(-30, 30)
        ax.set_ylim(-30, 30)
        ax.set_title(f"Iteration {i+1}")

    ani = FuncAnimation(fig, animate, frames=len(iterations_data), interval=interval)
    ani.save(path, writer='imagemagick')

def plot_voronoi_iterations_3d(iterations_data, X, Y, weeds, path, interval=2000):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    def animate(i):
        ax.clear()
        centers, paths, new_centers = iterations_data[i]
        ax.scatter(centers[:, 0], centers[:, 1], 5, color='r', label='Old Drone Positions')
        ax.scatter(new_centers[:, 0], new_centers[:, 1], 5, color='b', label='New Drone Positions')
        ax.plot_surface(X, Y, weeds, cmap='YlGn', alpha=0.5)
        ax.legend()
        ax.set_xlim(-30, 30)
        ax.set_ylim(-30, 30)
        ax.set_zlim(0, 5)
        ax.set_title(f"Iteration {i+1}")

    ani = FuncAnimation(fig, animate, frames=len(iterations_data), interval=interval)
    ani.save(path, writer='imagemagick')
