import numpy as np
class ParticleFilter:
    def __init__(self, num_particles, field_size):
        self.num_particles = num_particles
        self.field_size = field_size
        self.particles = self.initialize_particles()

    def initialize_particles(self):
        # Initialize particles randomly within the field
        particles = np.random.uniform(-self.field_size, self.field_size, (self.num_particles, 2))
        return particles

    def predict(self, move):
        # Update particles based on the drone's movement
        self.particles += move

    def update(self, measurement, sensor_model):
        # Update particle weights based on the measurement
        weights = np.array([sensor_model(particle, measurement) for particle in self.particles])
        self.weights = weights / np.sum(weights)

    def resample(self):
        # Resample particles based on their weights
        indices = np.random.choice(np.arange(self.num_particles), size=self.num_particles, p=self.weights)
        self.particles = self.particles[indices]
