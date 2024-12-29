import tkinter as tk
from tkinter import messagebox
import time
import pandas as pd
import random
from puzzle import astar_solve_puzzle  # Import thuật toán A*
from bfs import bfs_solve_puzzle  # Import thuật toán BFS
from dfs import dfs_solve_puzzle
from knn import KNNModel  # Import mô hình KNN mà bạn đã tạo

# Kích thước của ô và mảnh hình ảnh
piece_size = 50

# Trạng thái ban đầu của trò chơi
puzzle = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 0, 10, 12],
    [13, 14, 11, 15]
]

# Biến để theo dõi thời gian và điểm số
start_time = None
is_solved = False
score = 0

# Hàm tạo trạng thái hợp lệ ngẫu nhiên cho trò chơi 15 ô
def generate_puzzle_state():
    state = list(range(16))
    random.shuffle(state)
    return state

# Tạo dữ liệu cho tệp CSV chỉ nếu nó không tồn tại
def create_csv(filename, num_samples=1000):
    if not pd.io.common.file_exists(filename):
        data = []
        moves = ["right", "left", "up", "down"]

        for _ in range(num_samples):
            state = generate_puzzle_state()
            move = random.choice(moves)
            data.append(state + [move])

        columns = [f"state_{i+1}" for i in range(16)] + ["move"]
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(filename, index=False)

# Tạo tệp CSV với 1000 mẫu (nếu cần)
create_csv("puzzle_data.csv", num_samples=1000)

# Đọc dữ liệu từ tệp CSV
def load_data(filename):
    df = pd.read_csv(filename)
    X = df.iloc[:, :-1].values  # Các trạng thái
    y = df.iloc[:, -1].values  # Các nước đi
    return X, y

# Huấn luyện mô hình KNN
knn_model = KNNModel("puzzle_data.csv")

# Cập nhật giao diện của lưới
def update_grid():
    for i in range(4):
        for j in range(4):
            value = puzzle[i][j]
            buttons[i][j].config(text=str(value) if value != 0 else "", bg="#90ee90")
            if value == 0:
                buttons[i][j].config(bg="white")
    check_solved()

def get_pos(current_state, element):
    for row in range(len(current_state)):
        if element in current_state[row]:
            return row, current_state[row].index(element)

def slide_tile(i, j):
    global puzzle
    empty_row, empty_col = get_pos(puzzle, 0)
    if abs(empty_row - i) + abs(empty_col - j) == 1:
        puzzle[empty_row][empty_col], puzzle[i][j] = puzzle[i][j], puzzle[empty_row][empty_col]
        update_grid()

def reset_puzzle():
    global puzzle, is_solved, score
    puzzle = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 0, 10, 12],
        [13, 14, 11, 15]
    ]
    is_solved = False
    score = 0
    update_grid()
    reset_timer()

def check_solved():
    global is_solved, score
    if puzzle == [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]:
        is_solved = True
        stop_timer()
        score = sum(100 for i in range(4) for j in range(4) if puzzle[i][j] == i * 4 + j + 1)
        score_label.config(text=f"Điểm: {score}")
        messagebox.showinfo("Thành công", "Thành công! Bạn đã xếp đúng tất cả các ô!")

def animate_solution(path):
    if not path:
        return

    def move_next_state(step):
        global puzzle
        if step < len(path):
            puzzle = path[step]
            update_grid()
            steps_label.config(text=f"Số bước đi: {step + 1}")
            root.after(1000, lambda: move_next_state(step + 1))

    move_next_state(0)

def solve_puzzle_event():
    global puzzle
    start_time_astar = time.time()
    path, nodes_explored = astar_solve_puzzle(puzzle)
    end_time_astar = time.time()

    if path:
        solving_time = (end_time_astar - start_time_astar) * 1000
        solving_time_label.config(text=f"Thời gian giải A*: {solving_time:.2f} ms")
        nodes_label.config(text=f"Số bước duyệt: {nodes_explored}")
        animate_solution(path)
    else:
        messagebox.showinfo("No Solution", "Câu đố không thể giải quyết!")

def giai_bfs():
    global puzzle
    start_time_bfs = time.time()
    path, so_buoc = bfs_solve_puzzle(puzzle)
    end_time_bfs = time.time()
    thoi_gian = (end_time_bfs - start_time_bfs) * 1000
    if path:
        solving_time_bfs_label.config(text=f"Thời gian giải DFS: {thoi_gian:.2f} ms")
        nodes_label.config(text=f"Số bước duyệt: {so_buoc}")
        animate_solution(path)
    else:
        messagebox.showinfo("Thông báo", "Không thể giải quyết câu đố này!")

def giai_dfs():
    global puzzle
    start_time_dfs = time.time()
    path, so_buoc = dfs_solve_puzzle(puzzle)
    end_time_dfs = time.time()
    thoi_gian = (end_time_dfs - start_time_dfs) * 1000

    if path:
        solving_time_dfs_label.config(text=f"Thời gian giải DFS: {thoi_gian:.2f} ms")
        nodes_label.config(text=f"Số bước duyệt: {so_buoc}")
        animate_solution(path)
    else:
        messagebox.showinfo("Thông báo", "Không thể giải quyết câu đố này!")

def predict_move():
    global puzzle
    move = knn_model.predict([num for row in puzzle for num in row])
    messagebox.showinfo("Dự đoán", f"Nước đi tiếp theo: {move}")

def update_timer():
    global start_time
    if start_time is not None:
        elapsed_time = time.time() - start_time
        timer_label.config(text=f"{int(elapsed_time // 3600):02}:{int((elapsed_time // 60) % 60):02}:{int(elapsed_time % 60):02}")

    root.after(1000, update_timer)

def start_timer():
    global start_time
    start_time = time.time()
    update_timer()

def stop_timer():
    global start_time
    start_time = None

def reset_timer():
    global start_time
    start_time = None
    timer_label.config(text="00:00:00")


# Setup tkinter window
root = tk.Tk()
root.title("Sliding Puzzle Game")
root.geometry("900x700")
root.config(bg="#6699FF")

# Header
header = tk.Label(root, text="Trò chơi ghép hình", font=("Helvetica", 25), bg="pink", anchor="center")
header.pack(fill="x")

# Frame for puzzle grid
grid_frame = tk.Frame(root, borderwidth=2, relief="solid", bg="white")
grid_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

# Create buttons for the puzzle grid
buttons = [[None for _ in range(4)] for _ in range(4)]
for i in range(4):
    for j in range(4):
        button = tk.Button(grid_frame, text=str(puzzle[i][j]) if puzzle[i][j] != 0 else "",
                           width=piece_size // 5, height=piece_size // 10, bg="lightgrey", font=("Helvetica", 12),
                           command=lambda i=i, j=j: slide_tile(i, j))
        button.grid(row=i, column=j, padx=3, pady=3)
        buttons[i][j] = button

    # Frame for buttons
button_frame = tk.Frame(grid_frame)
button_frame.grid(row=4, column=0, columnspan=4, pady=10)

# Play button to start the game
play_button = tk.Button(button_frame, text="Chơi", command=start_timer)
play_button.grid(row=0, column=0, padx=5)

# Play again button to reset the game
reset_button = tk.Button(button_frame, text="Chơi lại", command=reset_puzzle)
reset_button.grid(row=0, column=1, padx=5)

# Solve using A* button
solve_button = tk.Button(button_frame, text="Giải A*", command=solve_puzzle_event)
solve_button.grid(row=0, column=2, padx=5)

# Solve using BFS button
bfs_button = tk.Button(button_frame, text="Giải BFS", command=giai_bfs)
bfs_button.grid(row=0, column=3, padx=5)

# Solve using DFS button
dfs_button = tk.Button(button_frame, text="Giải DFS", command=giai_bfs)
dfs_button.grid(row=0, column=5, padx=5)

# Prediction button
predict_button = tk.Button(button_frame, text="Dự đoán", command=predict_move)
predict_button.grid(row=0, column=4, padx=5)

# Frame for labels
label_frame = tk.Frame(root)
label_frame.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

# Timer label
timer_label = tk.Label(label_frame, text="00:00:00", font=("Helvetica", 30), bg="#FFCCCC")
timer_label.pack(pady=10)

# Score label
score_label = tk.Label(label_frame, text="Điểm: 0", font=("Helvetica", 18), bg="#FFCCCC")
score_label.pack(pady=10)

# Solving time labels for A* and BFS
solving_time_label = tk.Label(label_frame, text="Thời gian giải A*: 0 ms", font=("Helvetica", 14), bg="#FFCCCC")
solving_time_label.pack(pady=5)

solving_time_bfs_label = tk.Label(label_frame, text="Thời gian giải DFS: 0 ms", font=("Helvetica", 14), bg="#FFCCCC")
solving_time_bfs_label.pack(pady=5)

# Solving time label for DFS

solving_time_dfs_label = tk.Label(label_frame, text="Thời gian giải BFS: 0 ms", font=("Helvetica", 14), bg="#FFCCCC")
solving_time_dfs_label.pack(pady=5)

# Steps label for A* or BFS
steps_label = tk.Label(label_frame, text="Số bước đi: 0", font=("Helvetica", 14), bg="#FFCCCC")
steps_label.pack(pady=5)

# Nodes label for both algorithms
nodes_label = tk.Label(label_frame, text="Số bước duyệt: 0", font=("Helvetica", 14), bg="#FFCCCC")
nodes_label.pack(pady=5)

# Nodes label for both algorithms
nodes_label = tk.Label(label_frame, text="Số bước duyệt: 0", font=("Helvetica", 14), bg="#FFCCCC")
nodes_label.pack(pady=5)

# Start the tkinter main loop
root.mainloop()
