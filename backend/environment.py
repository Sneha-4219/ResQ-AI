import random

class DisasterEnvironment:
    def __init__(self, size=15):
        self.size = size
        # Initialize a 15x15 grid with safe cells '.'
        self.grid = [['.' for _ in range(size)] for _ in range(size)]
        self.victims = []
        self.hazards = []
        self.agents = []
        
        self._generate_scenario()

    def _generate_scenario(self):
        # Set Rescue Base at top-left
        self.grid[0][0] = 'R'

        # Place some static obstacles '#'
        obstacles = [(2, 2), (2, 3), (2, 4), (5, 5), (5, 6), (6, 5), (10, 10), (10, 11), (11, 10)]
        for r, c in obstacles:
            self.grid[r][c] = '#'

        # Place initial fire hazards 'F'
        self.hazards = [(3, 8), (4, 8), (8, 2)]
        for r, c in self.hazards:
            self.grid[r][c] = 'F'

        # Place victims 'V' with random severity
        victim_locations = [(12, 12), (2, 10), (9, 4)]
        for i, (r, c) in enumerate(victim_locations):
            self.grid[r][c] = 'V'
            self.victims.append({
                "id": f"V{i+1}",
                "pos": (r, c),
                "severity": random.choice(["Critical", "Moderate"]),
                "rescued": False
            })

    def get_state(self):
        """Returns the current state of the environment for the frontend."""
        return {
            "size": self.size,
            "grid": self.grid,
            "victims": self.victims,
            "hazards": self.hazards
        }

# Instantiate a global environment object so all agents share the same world
env_state = DisasterEnvironment()