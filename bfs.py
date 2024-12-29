DIRECTIONS = {'left': (0, -1), 'right': (0, 1), 'up': (-1, 0), 'down': (1, 0)}
GOAL_STATE = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]


def is_goal(state):
    return state == GOAL_STATE


def get_neighbors(state):
    empty_row, empty_col = [(row, col) for row in range(4) for col in range(4) if state[row][col] == 0][0]
    neighbors = []

    for direction, (dr, dc) in DIRECTIONS.items():
        new_row, new_col = empty_row + dr, empty_col + dc
        if 0 <= new_row < 4 and 0 <= new_col < 4:
            new_state = [row[:] for row in state]
            new_state[empty_row][empty_col], new_state[new_row][new_col] = new_state[new_row][new_col], \
            new_state[empty_row][empty_col]
            neighbors.append(new_state)

    return neighbors


def bfs_solve_puzzle(start_state):
    queue = [(start_state, [])]
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    nodes_explored = 0

    while queue:
        current_state, path = queue.pop(0)
        nodes_explored += 1

        if is_goal(current_state):
            return path + [current_state], nodes_explored

        for neighbor in get_neighbors(current_state):
            neighbor_tuple = tuple(map(tuple, neighbor))
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                queue.append((neighbor, path + [current_state]))

    return None, nodes_explored
