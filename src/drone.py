from sensors import set_sensor_estimation_model


class Drone:
    def __init__(self, x, y, method):
        self.x = x
        self.y = y
        self.sensor_estimation_model = set_sensor_estimation_model(method)

    def update_position(self, x, y):
        """Update the position of the drone."""
        self.x = x
        self.y = y

    def update_sensor_model(self, sampled_points, sampled_concentrations, method='kde'):
        self.sensor_estimation_model.fit(sampled_points, sampled_concentrations)