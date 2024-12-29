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

def dfs_solve_puzzle(start_state):
    stack = [(start_state, [])]  # Sử dụng ngăn xếp thay cho hàng đợi
    visited = set()  # Tập các trạng thái đã duyệt
    visited.add(tuple(map(tuple, start_state)))  # Lưu trạng thái đã duyệt
    nodes_explored = 0  # Đếm số nút đã duyệt

    while stack:
        current_state, path = stack.pop()  # Lấy trạng thái cuối cùng trong ngăn xếp
        nodes_explored += 1

        if is_goal(current_state):
            return path + [current_state], nodes_explored  # Trả về con đường đi và số nút đã duyệt

        # Lấy các trạng thái lân cận và duyệt chúng
        for neighbor in get_neighbors(current_state):
            neighbor_tuple = tuple(map(tuple, neighbor))
            if neighbor_tuple not in visited:
                visited.add(neighbor_tuple)  # Đánh dấu đã duyệt
                stack.append((neighbor, path + [current_state]))  # Thêm vào ngăn xếp

    return None, nodes_explored  # Trả về None nếu không tìm thấy giải pháp

# Ví dụ cách sử dụng
if __name__ == "__main__":
    initial_state = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 0, 10, 12],
        [13, 14, 11, 15]
    ]

    path, nodes_explored = dfs_solve_puzzle(initial_state)  # Giải bài toán
    if path is not None:
        print(f"Số bước cần thiết: {len(path)}")
        print(f"Số bước duyệt: {nodes_explored}")
    else:
        print("Không tìm được giải pháp cho trạng thái ban đầu.")
