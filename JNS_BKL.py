import tkinter as tk
import time

class PlayerStats:
    def __init__(self):
        self.reset()

    def reset(self):
        self.two_pt_made = 0
        self.two_pt_attempt = 0
        self.three_pt_made = 0
        self.three_pt_attempt = 0
        self.turnovers = 0
        self.assists = 0
        self.steals = 0

    def two_pt_display(self):
        if self.two_pt_attempt == 0:
            return "0/0 (0.0%)"
        percent = (self.two_pt_made / self.two_pt_attempt) * 100
        return f"{self.two_pt_made}/{self.two_pt_attempt} ({percent:.1f}%)"

    def three_pt_display(self):
        if self.three_pt_attempt == 0:
            return "0/0 (0.0%)"
        percent = (self.three_pt_made / self.three_pt_attempt) * 100
        return f"{self.three_pt_made}/{self.three_pt_attempt} ({percent:.1f}%)"

class BasketballStatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("3v3 籃球數據統計")
        self.players = [PlayerStats() for _ in range(6)]
        self.frames = []
        self.labels_list = []

        self.timer_running = False
        self.start_time = 0
        self.elapsed_time = 0

        self.create_ui()

    def create_ui(self):
        for i in range(6):
            frame = tk.LabelFrame(self.root, text=f"Player {i+1}", padx=5, pady=5,
                                  bg="#DDF" if i < 3 else "#FDD")
            frame.grid(row=i // 3, column=i % 3, padx=5, pady=5, sticky="n")
            self.frames.append(frame)
            self.create_stat_controls(frame, i)

        reset_all_btn = tk.Button(self.root, text="全部清除", bg="#FF6666", fg="white",
                                  command=self.reset_all_stats)
        reset_all_btn.grid(row=2, column=0, columnspan=3, pady=10, sticky="ew")

        # Timer Section
        self.timer_label = tk.Label(self.root, text="時間：00:00.00", font=("Arial", 18, "bold"),
                                    bg="black", fg="white", width=20, pady=10)
        self.timer_label.grid(row=3, column=0, columnspan=3, pady=10)

        btn_frame = tk.Frame(self.root)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=5)

        tk.Button(btn_frame, text="開始", bg="#66CC66", fg="white", width=10,
                  command=self.start_timer).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="暫停", bg="#FFCC00", fg="black", width=10,
                  command=self.pause_timer).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="結束比賽", bg="#FF3333", fg="white", width=10,
                  command=self.stop_timer).grid(row=0, column=2, padx=5)
        tk.Button(btn_frame, text="時間歸零", bg="#AAAAAA", fg="white", width=10,
                  command=self.reset_timer).grid(row=0, column=3, padx=5)

    def create_stat_controls(self, frame, index):
        player = self.players[index]
        labels = {}

        def update_labels():
            labels['2pt'].config(text=player.two_pt_display())
            labels['3pt'].config(text=player.three_pt_display())
            labels['to'].config(text=str(player.turnovers))
            labels['ast'].config(text=str(player.assists))
            labels['stl'].config(text=str(player.steals))

        def make_btn(stat, delta, label_key):
            def inner():
                if stat == "2pt_made":
                    player.two_pt_made = max(0, player.two_pt_made + delta)
                    player.two_pt_attempt = max(player.two_pt_made, player.two_pt_attempt)
                elif stat == "2pt_attempt":
                    player.two_pt_attempt = max(0, player.two_pt_attempt + delta)
                elif stat == "3pt_made":
                    player.three_pt_made = max(0, player.three_pt_made + delta)
                    player.three_pt_attempt = max(player.three_pt_made, player.three_pt_attempt)
                elif stat == "3pt_attempt":
                    player.three_pt_attempt = max(0, player.three_pt_attempt + delta)
                else:
                    setattr(player, stat, max(0, getattr(player, stat) + delta))
                update_labels()
            return inner

        row = 0
        for label_text, key, stats in [
            ("二分命中率", '2pt', [("2pt_made", +1), ("2pt_made", -1), ("2pt_attempt", +1), ("2pt_attempt", -1)]),
            ("三分命中率", '3pt', [("3pt_made", +1), ("3pt_made", -1), ("3pt_attempt", +1), ("3pt_attempt", -1)]),
            ("失誤", 'to', [("turnovers", +1), ("turnovers", -1)]),
            ("助攻", 'ast', [("assists", +1), ("assists", -1)]),
            ("抄截", 'stl', [("steals", +1), ("steals", -1)]),
        ]:
            tk.Label(frame, text=label_text, anchor='w').grid(row=row, column=0, sticky="w")
            labels[key] = tk.Label(frame, text="0/0 (0.0%)" if 'pt' in key else "0", width=14)
            labels[key].grid(row=row, column=1)
            for j, (stat, delta) in enumerate(stats):
                tk.Button(frame, text=f"{'+' if delta > 0 else '-'}1", width=3,
                          command=make_btn(stat, delta, key)).grid(row=row, column=2 + j)
            row += 1

        clear_btn = tk.Button(frame, text="清除", bg="#FFA500", fg="white",
                              command=lambda: self.reset_player(index))
        clear_btn.grid(row=row, column=0, columnspan=6, sticky="ew", pady=(5, 0))

        self.labels_list.append(labels)
        update_labels()

    def reset_player(self, index):
        self.players[index].reset()
        self.update_labels(index)

    def reset_all_stats(self):
        for i in range(6):
            self.players[i].reset()
            self.update_labels(i)

    def update_labels(self, index):
        player = self.players[index]
        labels = self.labels_list[index]
        labels['2pt'].config(text=player.two_pt_display())
        labels['3pt'].config(text=player.three_pt_display())
        labels['to'].config(text=str(player.turnovers))
        labels['ast'].config(text=str(player.assists))
        labels['stl'].config(text=str(player.steals))

    def start_timer(self):
        if not self.timer_running:
            self.start_time = time.time() - self.elapsed_time
            self.timer_running = True
            self.update_timer()

    def pause_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.elapsed_time = time.time() - self.start_time

    def stop_timer(self):
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.elapsed_time = 0
        self.timer_label.config(text="時間：00:00.00")

    def update_timer(self):
        if self.timer_running:
            current_time = time.time()
            elapsed = current_time - self.start_time
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            fraction = int((elapsed - int(elapsed)) * 100)
            self.timer_label.config(text=f"時間：{mins:02}:{secs:02}.{fraction:02}")
            self.root.after(10, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = BasketballStatsApp(root)
    root.mainloop()
