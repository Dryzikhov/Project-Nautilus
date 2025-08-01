# Project Nautilus

Project Nautilus is an AI-powered autonomous navigation system for an exploration submarine, built with Python. This repository contains the Minimum Viable Product (MVP) of the system, which demonstrates core functionalities such as route optimization, obstacle avoidance, and identification of interesting locations using simulated data.

## Project Structure

The project is organized into the following directories:

- `nautilus/`: Contains the core source code for the project.
  - `navigation/`: Houses the `Navigator` class, responsible for pathfinding (A*) and obstacle avoidance.
  - `ml/`: Contains the `AIModel` for identifying interesting locations and the `DataLoader` for simulating sensor data.
- `tests/`: Contains unit tests for all the core modules.
- `data/`: Intended to hold data files. Currently unused as data is simulated.
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

This will start a simulation that calculates a route, traverses it, and reports on obstacle avoidance and interesting locations found.

### Running Tests

To run the unit tests, use the `unittest` module from the root directory:

```bash
python3 -m unittest discover tests
```

All tests should pass, ensuring the core components are functioning correctly.

## MVP Functionalities

-   **Route Optimization:** The system uses an A* pathfinding algorithm to calculate the most efficient route from a start to an end point, avoiding known obstacles.
-   **Obstacle Avoidance:** During the mission, the submarine uses simulated sonar data to detect and react to nearby obstacles.
-   **Identification of Interesting Locations:** The AI model analyzes simulated underwater imagery to identify and flag locations of potential scientific interest.
