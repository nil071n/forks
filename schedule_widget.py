import tkinter as tk
import datetime as dt
import time
import sys
import threading

# --- Your schedule dictionary here (keep it as-is) ---

class ScheduleWidget:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Schema-widget")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.9)
        self.root.config(bg="black")

        # --- Layout ---
        self.label_day = tk.Label(self.root, font=("Helvetica", 16, "bold"), fg="white", bg="black")
        self.label_day.pack(padx=10, pady=(8, 0))

        self.label_class = tk.Label(self.root, font=("Helvetica", 30, "bold"), fg="lightgreen", bg="black")
        self.label_class.pack(padx=10, pady=(5, 0))

        self.label_status = tk.Label(self.root, font=("Helvetica", 20, "bold"), fg="orange", bg="black")
        self.label_status.pack(padx=10, pady=(2, 0))

        self.label_time = tk.Label(self.root, font=("Helvetica", 16), fg="lightblue", bg="black")
        self.label_time.pack(padx=10, pady=(0, 5))

        # --- Fönsterdragning ---
        self.root.bind("<Button-1>", self.start_move)
        self.root.bind("<B1-Motion>", self.do_move)

        # --- Prevent closing ---
        self.root.protocol("WM_DELETE_WINDOW", self.disable_event)

        self.update_info()
        self.root.mainloop()

    def disable_event(self):
        pass  # Ignore all close attempts

    def find_next_or_current_class(self):
        now = dt.datetime.now()
        day_name = now.strftime("%A")
        days_sv = {
            "Monday": "Måndag", "Tuesday": "Tisdag", "Wednesday": "Onsdag",
            "Thursday": "Torsdag", "Friday": "Fredag",
            "Saturday": "Lördag", "Sunday": "Söndag"
        }
        day_sv = days_sv.get(day_name, day_name)
        if day_sv not in schedule:
            return day_sv, None, None, None, "Ingen skoldag idag 😊", None

        today = schedule[day_sv]
        for start, end, subject in today:
            start_time = dt.datetime.strptime(start, "%H:%M").replace(year=now.year, month=now.month, day=now.day)
            end_time = dt.datetime.strptime(end, "%H:%M").replace(year=now.year, month=now.month, day=now.day)

            if start_time <= now < end_time:
                mins_left = int((end_time - now).total_seconds() // 60)
                return day_sv, start, end, subject, f"Lektion pågår – {mins_left} min kvar", True
            elif now < start_time:
                mins_until = int((start_time - now).total_seconds() // 60)
                return day_sv, start, end, subject, f"Nästa lektion – börjar om {mins_until} min", False

        return day_sv, None, None, None, "Dagen är slut 🎉", None

    def update_info(self):
        day_sv, start, end, subject, status_text, ongoing = self.find_next_or_current_class()
        self.label_day.config(text=day_sv)

        if subject:
            self.label_class.config(text=subject)
            if ongoing:
                self.label_status.config(text="Lektion pågår", fg="yellow")
            else:
                self.label_status.config(text="Nästa lektion", fg="lightblue")
            self.label_time.config(text=f"{start} – {end}\n{status_text}")
        else:
            self.label_class.config(text="")
            self.label_status.config(text="")
            self.label_time.config(text=status_text)

        self.root.after(60000, self.update_info)

    def start_move(self, event):
        self.x = event.x
        self.y = event.y

    def do_move(self, event):
        x = self.root.winfo_x() + event.x - self.x
        y = self.root.winfo_y() + event.y - self.y
        self.root.geometry(f"+{x}+{y}")


def keep_running():
    while True:
        try:
            ScheduleWidget()
        except:
            time.sleep(1)  # Wait a bit before restarting


if __name__ == "__main__":
    t = threading.Thread(target=keep_running)
    t.daemon = True
    t.start()
    while True:
        time.sleep(1)  # Keep main thread alive
