import random
import numpy as np
from nautilus.navigation.navigator import Navigator
from nautilus.ml.model import AIModel
from nautilus.ml.data_loader import DataLoader

def run_mission(weather_condition):
    """
    Simulates a full submarine mission, integrating all system components
    under a specific weather condition.
    """
    print(f"\n{'='*50}")
    print(f"STARTING MISSION: WEATHER CONDITION - {weather_condition.upper()}")
    print(f"{'='*50}")

    # 1. Initialization with weather condition
    grid_size = (20, 20)
    navigator = Navigator(grid_size=grid_size)
    ai_model = AIModel(weather_condition=weather_condition)
    data_loader = DataLoader(weather_condition=weather_condition)

    # 2. Mission Setup
    start_pos = (2, 2)
    end_pos = (18, 18)
    obstacles = set()
    for _ in range(5):
        obs_x, obs_y = random.randint(0, grid_size[0]-1), random.randint(0, grid_size[1]-1)
        if (obs_x, obs_y) != start_pos and (obs_x, obs_y) != end_pos:
            obstacles.add((obs_x, obs_y))

    print(f"Mission from {start_pos} to {end_pos}. Generated {len(obstacles)} static obstacles.")

    # 3. Route Optimization
    print("\nCalculating optimal route...")
    route = navigator.optimize_route(start_pos, end_pos, list(obstacles))
    if not route:
        print("Mission failed: No route could be calculated.")
        return
    print(f"Route calculated with {len(route)} steps.")

    # 4. Mission Execution Simulation
    print("\nExecuting mission...")
    mission_summary = {"interesting_locations_found": 0, "obstacle_avoidance_actions": 0}

    for i, position in enumerate(route):
        print(f"Step {i+1}/{len(route)}: At position {position}")

        # a. Load all sensor data
        sonar_data = data_loader.load_sonar_data()
        lidar_data = data_loader.load_lidar_data()
        chemical_data = data_loader.load_chemical_data()
        underwater_image = data_loader.load_underwater_image()

        # b. Risk-Based Obstacle Avoidance
        obstacle_risk = ai_model.assess_obstacle_risk(sonar_data, lidar_data)
        avoidance_action = navigator.avoid_obstacle(obstacle_risk, sonar_data['angle'])

        if avoidance_action != "Proceed":
            mission_summary["obstacle_avoidance_actions"] += 1
            print(f"  - Obstacle Risk: {obstacle_risk:.2f}. AI recommends: {avoidance_action}")
        else:
            print(f"  - Path clear. (Obstacle Risk: {obstacle_risk:.2f})")

        # c. Advanced Interesting Location Identification
        findings = ai_model.identify_interesting_locations(underwater_image, lidar_data, chemical_data)
        if findings["is_interesting"]:
            mission_summary["interesting_locations_found"] += 1
            conf = findings['fused_confidence']
            scores = findings['individual_scores']
            print(f"  - AI found an interesting location! (Confidence: {conf:.2f})")
            print(f"    - Sensor Scores: Image({scores['image']:.2f}), LIDAR({scores['lidar']:.2f}), Chemical({scores['chemical']:.2f})")

    # 5. Mission Summary
    print("\nMission Complete.")
    print(f"Final position: {route[-1]}")
    print("Mission Summary:")
    print(f"  - Total interesting locations identified: {mission_summary['interesting_locations_found']}")
    print(f"  - Total obstacle avoidance maneuvers: {mission_summary['obstacle_avoidance_actions']}")
    print(f"{'-'*50}\n")


if __name__ == "__main__":
    # Run the simulation for each weather condition to demonstrate adaptability
    weather_scenarios = ['clear', 'fog', 'storm']
    for scenario in weather_scenarios:
        run_mission(weather_condition=scenario)
