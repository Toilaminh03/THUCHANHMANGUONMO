import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

class LinearEquationSolverApp:
    def __init__(self, root):
        self.root = root
        root.title("Giải Hệ Phương Trình Tuyến Tính")
        root.geometry("600x500")
        root.resizable(False, False)

        # Kiểu màu hiện đại
        root.configure(bg="#f0f2f5")

        # Khung nhập số phương trình
        frame_top = ttk.Frame(root, padding="10 10 10 10")
        frame_top.grid(row=0, column=0, columnspan=3, sticky="ew")

        label_n = ttk.Label(frame_top, text="Số phương trình (n):", font=("Arial", 10))
        label_n.grid(row=0, column=0, padx=(0, 5))
        
        self.entry_n = ttk.Entry(frame_top, width=10)
        self.entry_n.grid(row=0, column=1, padx=(0, 10))

        generate_button = ttk.Button(frame_top, text="Tạo ma trận hệ số", command=self.create_matrix)
        generate_button.grid(row=0, column=2)

        # Khung hiển thị ma trận hệ số
        self.matrix_frame = ttk.Frame(root, padding="10 10 10 10", relief="ridge")
        self.matrix_frame.grid(row=1, column=0, columnspan=3, pady=(10, 0), sticky="nsew")

        # Khung kết quả
        result_frame = ttk.Frame(root, padding="10 10 10 10")
        result_frame.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

        self.result_label = ttk.Label(result_frame, text="Kết quả:", font=("Arial", 12, "bold"))
        self.result_label.grid(row=0, column=0, sticky="w")

        self.result_text = tk.Text(result_frame, height=10, width=70, state="disabled", bg="#ffffff", fg="#333333", font=("Arial", 10))
        self.result_text.grid(row=1, column=0, pady=5)

        # Khung các nút điều khiển
        control_frame = ttk.Frame(root, padding="10 10 10 10")
        control_frame.grid(row=3, column=0, columnspan=3, pady=10)

        solve_button = ttk.Button(control_frame, text="Giải phương trình", command=self.solve)
        solve_button.grid(row=0, column=0, padx=5)
        
        clear_button = ttk.Button(control_frame, text="Xóa dữ liệu", command=self.clear)
        clear_button.grid(row=0, column=1, padx=5)

    def create_matrix(self):
        # Xóa các ô nhập liệu cũ nếu có
        for widget in self.matrix_frame.winfo_children():
            widget.destroy()

        try:
            self.n = int(self.entry_n.get())
            self.entries = []

            # Tạo ma trận nhập liệu cho hệ phương trình
            for i in range(self.n):
                row_entries = []
                for j in range(self.n + 1):  # Thêm 1 cho hệ số tự do
                    entry = ttk.Entry(self.matrix_frame, width=10)
                    entry.grid(row=i, column=j, padx=5, pady=2)
                    row_entries.append(entry)
                self.entries.append(row_entries)

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số nguyên cho n")

    def solve(self):
        try:
            # Lấy hệ số từ các ô nhập
            coefficients = []
            constants = []
            for i in range(self.n):
                row = [float(self.entries[i][j].get()) for j in range(self.n)]
                coefficients.append(row)
                constants.append(float(self.entries[i][self.n].get()))

            # Chuyển đổi sang ma trận NumPy
            A = np.array(coefficients)
            B = np.array(constants)

            # Kiểm tra định thức
            det_A = np.linalg.det(A)
            if det_A != 0:
                # Hệ có nghiệm duy nhất
                solutions = np.linalg.solve(A, B)
                result_str = "Giá trị của các ẩn số:\n"
                for i, solution in enumerate(solutions):
                    result_str += f"x{i+1} = {solution:.2f}\n"
            else:
                # Kiểm tra hạng của ma trận
                rank_A = np.linalg.matrix_rank(A)
                augmented_matrix = np.hstack((A, B.reshape(-1, 1)))
                rank_augmented = np.linalg.matrix_rank(augmented_matrix)

                if rank_A == rank_augmented:
                    if rank_A == self.n:
                        result_str = "Hệ có vô số nghiệm."
                    else:
                        result_str = "Hệ vô số nghiệm (hạng nhỏ hơn số ẩn)."
                else:
                    result_str = "Hệ phương trình vô nghiệm."

            # Hiển thị kết quả
            self.result_text.config(state="normal")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result_str)
            self.result_text.config(state="disabled")

        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập tất cả các giá trị cần thiết.")

    def clear(self):
        # Xóa các giá trị trong ô nhập và Text
        for row_entries in self.entries:
            for entry in row_entries:
                entry.delete(0, tk.END)
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state="disabled")
        self.entry_n.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = LinearEquationSolverApp(root)
    root.mainloop()
