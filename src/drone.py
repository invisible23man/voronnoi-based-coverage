class Drone:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update_position(self, x, y):
        """Update the position of the drone."""
        self.x = x
        self.y = y
