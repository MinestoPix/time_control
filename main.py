""" TODO doc
"""

import os.path
import timer
from datetime import datetime, timedelta

import gui
import systray

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
PATH = "time_log"


def calculate_time_left():
    if os.path.isfile(PATH):
        with open(PATH, "r") as log:
            sum_time = timedelta()
            first_date = None
            print("file opened, calculating time")
            for line in log:
                if line.startswith("B"):  # BEGINNING TIME
                    date_str = line[1:-1]
                    first_date = datetime.strptime(date_str, DATE_FORMAT)
                elif line.startswith("E") or line.startswith("T"):  # END TIME (T for TEMPORARY save in case of crash)
                    date_str = line[1:-1]
                    sec_date = datetime.strptime(date_str, DATE_FORMAT)
                    if first_date:
                        sum_time -= sec_date - first_date
                        first_date = None
                elif line.startswith("A"):  # MANUAL ADD
                    date_str = line[1:]
                    sum_time += timedelta(seconds=int(date_str))
            return int(sum_time.total_seconds())

    else:
        # print(path, "does not exist, creating empty")
        # open(path, "x").close()  # 'x' mode for exclusive file creation
        return 0


def save_time(entry_type, entry_datetime):
    print("saving entry ", entry_type)
    if entry_type == "T" or entry_type == "E":
        with open(PATH) as log:
            # Copy all lines except last one
            lines = log.readlines()
            last_line = lines[-1]
            lines = lines[:-1]
            if not last_line.startswith("T"):  # If last line is not temporary it copies it too
                lines.append(last_line)
        with open(PATH, "w") as log:
            log.writelines(lines)
            log.write(entry_type + entry_datetime.strftime(DATE_FORMAT) + "\n")
    elif entry_type == "B":
        with open(PATH, "a") as log:
            log.write(entry_type + entry_datetime.strftime(DATE_FORMAT) + "\n")
    else:
        with open(PATH, "a") as log:
            try:
                seconds = int(entry_datetime)
            except TypeError:
                seconds = int(entry_datetime.total_seconds())
            log.write(entry_type + str(seconds) + "\n")


if __name__ == "__main__":

    time_left = calculate_time_left()

    save_time("B", datetime.now())

    notified = False

    paused = False


    def countdown(id, elapsed):
        global time_left
        global notified
        global paused
        if not paused:
            time_left -= 1
        if time_left <= 0 and not notified:
            systray.WindowsBalloonTip("Time is up!", "You have 10 minutes to turn off your computer")
            notified = True

        save_interval = 60  # Saving interval in seconds
        if time_left % save_interval == 0:
            save_time("T", datetime.now())
        print(timedelta(seconds=time_left))


    sec_timer = timer.set_timer(1000, countdown)


    def time_change(delta):
        print(delta.total_seconds())
        global time_left
        time_left += int(delta.total_seconds())
        save_time("A", delta)


    def main_menu(sys_tray_icon):
        gui.Menu(time_change, timedelta(seconds=time_left)).mainloop()


    def ondblclick(sys_tray_icon):
        global paused
        paused = True
        gui.Fullscreen().mainloop()
        paused = False


    def on_quit(sys_tray_icon):
        gui.Password(sys_tray_icon).mainloop()


    menu_list = (("Pause", None, ondblclick),
                 ("Main Menu", None, main_menu))

    systray.SysTrayIcon("alarm-clock.ico", "test", menu_list, on_quit)

    save_time("E", datetime.now())
