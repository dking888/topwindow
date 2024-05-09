import tkinter as tk
import pystray
from PIL import Image


def create_safe_resizable_window():

    # 创建无标题栏的主窗口
    root = tk.Tk()
    root.title("Safe Resizable Window")
    root.overrideredirect(True)  # 这将去掉标题栏

    # 获取屏幕尺寸以便居中
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = 800
    window_height = 50

    # 计算窗口居中的x和y坐标
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # 设置窗口始终在顶部
    root.attributes("-topmost", True)

    # 设置初始背景颜色为白色
    root.config(bg="white")

    # 移动窗口的功能
    def on_drag_start(event):
        if getattr(root, "resizing", False):  # 如果正在调整大小，则不移动窗口
            return
        root.x_start = event.x
        root.y_start = event.y

    def on_drag_motion(event):
        if getattr(root, "resizing", False):  # 如果正在调整大小，则不移动窗口
            return
        x = root.winfo_x() - root.x_start + event.x
        y = root.winfo_y() - root.y_start + event.y
        root.geometry(f"+{x}+{y}")

    root.bind("<Button-1>", on_drag_start)
    root.bind("<B1-Motion>", on_drag_motion)

    # 调整窗口大小的功能
    def start_resize(event):
        root.resizing = True  # 设置调整大小标志
        root.start_x = event.x
        root.start_y = event.y

    def do_resize(event):
        if root.resizing:
            delta_x = event.x - root.start_x
            delta_y = event.y - root.start_y
            new_width = max(root.winfo_width() + delta_x, 100)  # 设置最小宽度为100
            new_height = max(root.winfo_height() + delta_y, 50)  # 设置最小高度为50
            root.geometry(f"{new_width}x{new_height}")

    def stop_resize(event):
        root.resizing = False

    # 创建更改颜色的按钮
    def change_color(color):
        text_color = "white" if color == "black" else "black"
        root.config(bg=color)
        top_frame.config(bg=color)  # 设置 top_frame 的背景颜色
        bottom_frame.config(bg=color)  # 设置 bottom_frame 的背景颜色
        change_to_black.config(bg=color, fg=text_color)
        change_to_white.config(bg=color, fg=text_color)
        close_button.config(bg=color, fg=text_color)

    # 创建托盘图标并最小化窗口的功能
    def minimize_to_tray():
        root.withdraw()  # 隐藏窗口

        # 创建托盘图标
        image = Image.open("icon.png")  # 使用你的图标文件替换"icon.png"
        menu = (
            pystray.MenuItem("恢复", lambda: restore_from_tray(icon)),
            pystray.MenuItem("关闭", lambda: exit_program(icon)),
        )
        icon = pystray.Icon("name", image, "My System Tray Icon", menu)

        # 恢复窗口的功能
        def restore_from_tray(icon):
            icon.stop()
            root.deiconify()

        # 关闭程序的功能
        def exit_program(icon):
            icon.stop()
            root.destroy()

        icon.run()

    # 在窗口的顶部创建一个框架来放置按钮
    top_frame = tk.Frame(root, bg="white")
    top_frame.pack(side="top", fill="x")

    # 创建最小化按钮
    minimize_button = tk.Button(top_frame, text="—", command=minimize_to_tray, width=2)
    minimize_button.pack(side="right")

    # 在底部创建一个框架来放置调整大小的标签
    bottom_frame = tk.Frame(root, bg="white")
    bottom_frame.pack(side="bottom", fill="x")

    # 将黑色和白色按钮放在框架的左侧
    change_to_black = tk.Button(
        top_frame, text="Black", command=lambda: change_color("black"), width=5
    )
    change_to_black.pack(side="left", padx=2)

    change_to_white = tk.Button(
        top_frame, text="White", command=lambda: change_color("white"), width=5
    )
    change_to_white.pack(side="left", padx=2)

    # 将关闭按钮放在框架的右侧
    close_button = tk.Button(top_frame, text="✖", command=root.destroy, width=2)
    close_button.pack(side="right")

    resize_grip = tk.Label(
        bottom_frame, text="↘", bg="grey", cursor="bottom_right_corner", width=2
    )
    resize_grip.pack(side="right", padx=2, pady=2)
    resize_grip.bind("<Button-1>", start_resize)
    resize_grip.bind("<B1-Motion>", do_resize)
    resize_grip.bind("<ButtonRelease-1>", stop_resize)

    # 进入主事件循环
    root.mainloop()


if __name__ == "__main__":
    create_safe_resizable_window()
