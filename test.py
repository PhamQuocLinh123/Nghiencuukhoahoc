import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Demo Rê Chuột")
        self.geometry("400x300")

        # Tạo hình ảnh người dùng và nút "Đổi mật khẩu"
        self.current_user_image = ImageTk.PhotoImage(file="current_user.png")
        self.current_user_label = tk.Label(self, image=self.current_user_image, bg="white")
        self.current_user_label.place(x=100, y=100)

        self.reset_pass_button = tk.Button(self, text="Đổi mật khẩu", command=self.reset_pass)

        # Gắn các sự kiện chuột vào hình ảnh người dùng
        self.current_user_label.bind("<Enter>", self.show_reset_password_button)
        self.current_user_label.bind("<Leave>", self.hide_reset_password_button)
        self.reset_pass_button.bind("<Button-1>", self.reset_pass)

    def show_reset_password_button(self, event):
        self.reset_pass_button.place(x=150, y=150)

    def hide_reset_password_button(self, event):
        self.reset_pass_button.place_forget()

    def reset_pass(self, event=None):
        messagebox.showinfo("Thông báo", "Đã nhấn vào nút 'Đổi mật khẩu'.")

if __name__ == "__main__":
    app = App()
    app.mainloop()
