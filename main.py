import random
import numpy as np
from nautilus.navigation.navigator import Navigator
from nautilus.ml.model import AIModel
from nautilus.ml.data_loader import DataLoader

def run_mission():
    """
    Simulates a full submarine mission, integrating all system components.
    """
    print("Starting Project Nautilus Mission Simulation...")

    # 1. Initialization
    grid_size = (20, 20)
    navigator = Navigator(grid_size=grid_size)
    ai_model = AIModel(threshold=0.98) # High threshold to make it rare
    data_loader = DataLoader()

    # 2. Mission Setup
    start_pos = (2, 2)
    end_pos = (18, 18)
    # Generate some random obstacle clusters
    obstacles = set()
    for _ in range(5): # Reduced from 15 to 5
        obs_x, obs_y = random.randint(0, grid_size[0]-1), random.randint(0, grid_size[1]-1)
        if (obs_x, obs_y) != start_pos and (obs_x, obs_y) != end_pos:
            for i in range(random.randint(1, 3)): # Reduced cluster size
                for j in range(random.randint(1, 3)):
                    obstacles.add((obs_x+i, obs_y+j))

    print(f"Mission from {start_pos} to {end_pos}.")
    print(f"Generated {len(obstacles)} obstacles.")

    # 3. Route Optimization
    print("\nCalculating optimal route...")
    route = navigator.optimize_route(start_pos, end_pos, list(obstacles))

    if not route:
        print("Mission failed: No route could be calculated.")
        return

    print(f"Route calculated with {len(route)} steps.")

    # 4. Mission Execution Simulation
    print("\nExecuting mission...")
    interesting_locations_found = []
    for i, position in enumerate(route):
        print(f"Step {i+1}/{len(route)}: At position {position}")

        # a. Obstacle Avoidance Simulation
        sonar_data = data_loader.load_sonar_data()
        avoidance_action = navigator.avoid_obstacle(sonar_data)
        if avoidance_action != "Proceed":
            print(f"  - Sonar detected potential obstacle (dist: {sonar_data['distance']:.1f}). Action: {avoidance_action}")
        else:
            print("  - Path clear.")

        # b. Interesting Location Identification Simulation
        underwater_image = data_loader.load_underwater_image()
        locations = ai_model.identify_interesting_locations(underwater_image)
        if locations:
            # For simulation, let's assume the location is at the current sub position
            interesting_locations_found.append(position)
            print(f"  - AI model identified an interesting feature at {position}!")

    # 5. Mission Summary
    print("\nMission Complete.")
    print(f"Final position: {route[-1]}")
    if interesting_locations_found:
        print(f"Found {len(interesting_locations_found)} interesting locations at: {interesting_locations_found}")
    else:
        print("No interesting locations were found on this mission.")


if __name__ == "__main__":
    run_mission()
