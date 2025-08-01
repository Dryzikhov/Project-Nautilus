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
    ai_model = AIModel(image_threshold=0.98) # High threshold to make it rare
    data_loader = DataLoader()

    # 2. Mission Setup
    start_pos = (2, 2)
    end_pos = (18, 18)
    # Generate some random obstacle clusters
    obstacles = set()
    for _ in range(5):
        obs_x, obs_y = random.randint(0, grid_size[0]-1), random.randint(0, grid_size[1]-1)
        if (obs_x, obs_y) != start_pos and (obs_x, obs_y) != end_pos:
            for i in range(random.randint(1, 2)):
                for j in range(random.randint(1, 2)):
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
    mission_summary = {"interesting_locations": 0, "lidar_objects": 0, "chemical_anomalies": 0}

    for i, position in enumerate(route):
        print(f"Step {i+1}/{len(route)}: At position {position}")

        # a. Load all sensor data
        sonar_data = data_loader.load_sonar_data()
        lidar_data = data_loader.load_lidar_data()
        chemical_data = data_loader.load_chemical_data()
        underwater_image = data_loader.load_underwater_image()

        # b. Obstacle Avoidance
        avoidance_action = navigator.avoid_obstacle(sonar_data, lidar_data)
        if avoidance_action != "Proceed":
            print(f"  - Obstacle detected! Sonar (dist: {sonar_data['distance']:.1f}), LIDAR (std: {np.std(lidar_data):.2f}). Action: {avoidance_action}")
        else:
            print("  - Path clear.")

        # c. Interesting Location Identification (Sensor Fusion)
        findings = ai_model.identify_interesting_locations(underwater_image, lidar_data, chemical_data)

        if findings["image_features"]:
            mission_summary["interesting_locations"] += 1
            print(f"  - AI found {len(findings['image_features'])} visual features.")
        if findings["lidar_object_detected"]:
            mission_summary["lidar_objects"] += 1
            print("  - AI confirmed a dense object with LIDAR.")
        if findings["chemical_anomalies"]:
            mission_summary["chemical_anomalies"] += 1
            print(f"  - AI detected chemical anomalies: {findings['chemical_anomalies']}")

    # 5. Mission Summary
    print("\nMission Complete.")
    print(f"Final position: {route[-1]}")
    print("Mission Summary:")
    print(f"  - Interesting locations based on imagery: {mission_summary['interesting_locations']}")
    print(f"  - Dense objects confirmed by LIDAR: {mission_summary['lidar_objects']}")
    print(f"  - Chemical anomalies detected: {mission_summary['chemical_anomalies']}")


if __name__ == "__main__":
    run_mission()
