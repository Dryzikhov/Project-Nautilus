import heapq
import numpy as np

class Navigator:
    def __init__(self, grid_size=(100, 100)):
        self.grid_size = grid_size

    def avoid_obstacle(self, obstacle_risk_score, sonar_angle):
        """
        Makes a navigation decision based on a fused obstacle risk score from the AI model.
        """
        if obstacle_risk_score >= 0.7:
            # High risk: take decisive action
            if sonar_angle < 0:
                return "Hard Turn Right"
            else:
                return "Hard Turn Left"
        elif obstacle_risk_score >= 0.3:
            # Moderate risk: suggest a turn
            if sonar_angle < 0:
                return "Turn Right"
            else:
                return "Turn Left"

        return "Proceed"

    def optimize_route(self, start, end, obstacles):
        """
        A* pathfinding algorithm for route optimization.
        'start' and 'end' are tuples (x, y).
        'obstacles' is a list of obstacle coordinates [(x1, y1), (x2, y2), ...].
        """
        if not (0 <= start[0] < self.grid_size[0] and 0 <= start[1] < self.grid_size[1] and \
                0 <= end[0] < self.grid_size[0] and 0 <= end[1] < self.grid_size[1]):
            raise ValueError("Start or end point is out of grid bounds.")

        # The set of nodes already evaluated
        close_set = set()
        # The set of currently discovered nodes that are not evaluated yet
        open_set = {start}
        # For each node, which node it can most efficiently be reached from
        came_from = {}
        # For each node, the cost of getting from the start node to that node
        g_score = {start: 0}
        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node. This value is partly known, partly heuristic
        f_score = {start: self._heuristic(start, end)}

        # The priority queue of nodes to be evaluated
        oheap = []
        heapq.heappush(oheap, (f_score[start], start))

        while oheap:
            current = heapq.heappop(oheap)[1]

            if current == end:
                return self._reconstruct_path(came_from, current)

            open_set.remove(current)
            close_set.add(current)

            for neighbor in self._get_neighbors(current, obstacles):
                if neighbor in close_set:
                    continue

                tentative_g_score = g_score[current] + 1  # Assuming grid movement cost is 1

                if neighbor not in open_set:
                    open_set.add(neighbor)
                elif tentative_g_score >= g_score.get(neighbor, float('inf')):
                    continue

                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + self._heuristic(neighbor, end)
                heapq.heappush(oheap, (f_score[neighbor], neighbor))

        return None  # No path found

    def _heuristic(self, a, b):
        """
        Manhattan distance heuristic for A*.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _get_neighbors(self, node, obstacles):
        """
        Get neighbors of a node in the grid.
        """
        neighbors = []
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # 4-directional
            nx, ny = node[0] + dx, node[1] + dy
            if 0 <= nx < self.grid_size[0] and 0 <= ny < self.grid_size[1] and (nx, ny) not in obstacles:
                neighbors.append((nx, ny))
        return neighbors

    def _reconstruct_path(self, came_from, current):
        """
        Reconstruct the path from the came_from map.
        """
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]
