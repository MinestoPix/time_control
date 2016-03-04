import tkinter as tk
from datetime import timedelta


class Menu(tk.Tk):
    def __init__(self, time_change_func, time_left, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.time_change_func = time_change_func

        self.time_left = time_left

        # self.minsize(500, 150)
        # self.geometry("{0}x{1}+0+0".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        # self.attributes("-fullscreen", True)

        container = tk.Frame(self)
        container.pack()

        self.time_track = tk.Label(container)
        self.time_track.grid(columnspan=5)

        self.one_sec = timedelta(seconds=1)

        self.hour_label = tk.Label(container, text="H:")
        self.hour_label.grid(row=1, column=0, sticky=tk.W)

        self.hour_text = tk.Entry(container, width=2)
        self.hour_text.grid(row=1, column=1, sticky=tk.W)
        # self.hour_text.bind("<Key-KP_Enter>", self.test_handler)

        self.min_label = tk.Label(container, text="M:")
        self.min_label.grid(row=1, column=2, sticky=tk.W)

        self.min_text = tk.Entry(container, width=3)
        self.min_text.grid(row=1, column=3, sticky=tk.W)
        # self.min_text.bind("<Key-KP_Enter>", self.test_handler)

        self.time_add_button = tk.Button(container, text="Add time", command=self.test_handler)
        self.time_add_button.grid(row=1, column=4)

        self.password_entry = tk.Entry(container, show="*")
        self.password_entry.grid(columnspan=5)
        # self.password_entry.bind("<Key-KP_Enter>", self.test_handler)

        self.bind_all("<KeyPress-Return>", self.test_handler)

        self.sec_func()

    def sec_func(self):
        self.time_left -= self.one_sec
        if self.time_left.total_seconds() < 0:
            self.time_track.config(text="-" + str(abs(self.time_left)))
            self.time_track.config(fg="#f00")
        else:
            self.time_track.config(text=str(self.time_left))
        self.after(1000, self.sec_func)

    def test_handler(self, event=None):
        if self.password_entry.get() == "aoeu":
            self.add_time()

    def add_time(self):
        try:
            hours = int(self.hour_text.get())
        except ValueError:
            hours = 0
        try:
            minutes = int(self.min_text.get())
        except ValueError:
            minutes = 0
        td = timedelta(hours=hours, minutes=minutes)
        self.time_left += td
        self.time_change_func(td)


class Fullscreen(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.focus_force()

        self.attributes("-fullscreen", True)
        self.config(bg="#000")
        self.bind("<KeyPress>", self.on_press)
        self.bind("<Button>", self.on_press)
        # self.bind("<FocusOut>", self.on_press)

    def on_press(self, *args):
        self.destroy()


class Password(tk.Tk):
    def __init__(self, sysTray, *args, **kwargs):
        self.sysTray = sysTray
        tk.Tk.__init__(self, *args, **kwargs)

        self.password_label = tk.Label(self, text="Insert Password")
        self.password_label.pack()

        self.password_entry = tk.Entry(self)
        self.password_entry.bind("<KeyPress>", self.check_password)
        self.password_entry.pack()

    def check_password(self, key):
        if (self.password_entry.get() + key.char == "aoeu" or
                    self.password_entry.get() == "aoeu"):
            print("pass correct")
            self.sysTray.close_window()
            self.destroy()
