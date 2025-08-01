# Project Nautilus

Project Nautilus is an AI-powered autonomous navigation system for an exploration submarine, built with Python. This repository contains the first MVP, which focuses on **Advanced Sensor Integration**. The system demonstrates enhanced functionalities such as multi-sensor fusion for route optimization, obstacle avoidance, and identification of interesting locations using simulated data from a variety of sensors.

## Project Structure

The project is organized into the following directories:

- `nautilus/`: Contains the core source code for the project.
  - `navigation/`: Houses the `Navigator` class, responsible for pathfinding (A*) and enhanced obstacle avoidance.
  - `ml/`: Contains the `AIModel` for sensor fusion and the `DataLoader` for simulating all sensor data.
- `tests/`: Contains unit tests for all the core modules.
- `main.py`: The main entry point to run the mission simulation.
- `requirements.txt`: A list of Python packages required for the project.

## Setup and Installation

To set up the project locally, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd project-nautilus
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

### Running the Simulation

To run the main mission simulation, execute the `main.py` script:

```bash
python3 main.py
```

This will start a simulation that calculates a route, traverses it, and reports on obstacle avoidance and interesting locations found using fused sensor data.

### Running Tests

To run the unit tests, use the `unittest` module from the root directory:

```bash
python3 -m unittest discover tests
```

All tests should pass, ensuring the core components are functioning correctly.

## MVP Functionalities: Advanced Sensor Integration

-   **Route Optimization:** The system uses an A* pathfinding algorithm to calculate the most efficient route from a start to an end point, avoiding known obstacles.
-   **Enhanced Obstacle Avoidance:** The submarine uses a combination of simulated **sonar** and **LIDAR** data to detect and react to nearby obstacles. The fusion of these sensors allows for more reliable and decisive actions (e.g., "Hard Turn Left/Right").
-   **Multi-Sensor Fusion for Location Identification:** The AI model analyzes and fuses data from multiple sources to identify locations of interest:
    -   **Underwater Imagery:** Identifies visual features.
    -   **LIDAR Point Clouds:** Detects dense objects that may not be clear in images.
    -   **Chemical Sensors:** Detects anomalies in pH, salinity, and temperature, which could indicate unique environmental conditions.
-   **Comprehensive Mission Summary:** At the end of the simulation, a summary is provided detailing all findings, including visual features, LIDAR-confirmed objects, and chemical anomalies.
