import time

# Hướng đi có thể di chuyển (trái, phải, lên, xuống)
DIRECTIONS = {
    'left': (0, -1),
    'right': (0, 1),
    'up': (-1, 0),
    'down': (1, 0)
}

# Trạng thái mục tiêu cho trò chơi 15 ô (4x4)
GOAL_STATE = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 0]]

def is_goal(state):
    """Kiểm tra xem trạng thái hiện tại có phải là trạng thái đích không."""
    return state == GOAL_STATE

def get_neighbors(state):
    """Trả về danh sách các trạng thái lân cận."""
    empty_row, empty_col = [(row, col) for row in range(4) for col in range(4) if state[row][col] == 0][0]
    neighbors = []

    for direction, (dr, dc) in DIRECTIONS.items():
        new_row, new_col = empty_row + dr, empty_col + dc
        if 0 <= new_row < 4 and 0 <= new_col < 4:
            new_state = [row[:] for row in state]  # Tạo bản sao của trạng thái
            new_state[empty_row][empty_col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[empty_row][empty_col]
            neighbors.append(new_state)

    return neighbors

def misplaced_tiles(current_state):
    """Đếm số ô không đúng vị trí trong trạng thái hiện tại."""
    misplaced = 0
    for row in range(4):
        for col in range(4):
            if current_state[row][col] != 0 and current_state[row][col] != GOAL_STATE[row][col]:
                misplaced += 1
    return misplaced

def heuristic(current_state):
    """Hàm ước lượng chỉ dựa trên số ô sai vị trí."""
    return misplaced_tiles(current_state)

def astar_solve_puzzle(start_state):
    """Giải quyết trò chơi bằng thuật toán A*."""
    open_list = [(heuristic(start_state), 0, start_state, [])]  # Danh sách mở
    visited = set()
    visited.add(tuple(map(tuple, start_state)))
    nodes_explored = 0

    while open_list:
        # Tìm nút có chi phí thấp nhất
        min_index = 0
        for i in range(1, len(open_list)):
            if open_list[i][0] < open_list[min_index][0]:
                min_index = i

        heuristic_cost, cost, current_state, path = open_list.pop(min_index)  # Lấy nút với chi phí thấp nhất
        nodes_explored += 1

        if is_goal(current_state):
            return path, nodes_explored  # Trả về con đường đi và số bước duyệt

        # Lấy tất cả các trạng thái lân cận
        for neighbor in get_neighbors(current_state):
            neighbor_tuple = tuple(map(tuple, neighbor))
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)
                open_list.append((cost + 1 + heuristic(neighbor), cost + 1, neighbor, path + [neighbor]))

    return None, nodes_explored

if __name__ == "__main__":
    initial_state = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 0, 10, 12],
        [13, 14, 11, 15]
    ]