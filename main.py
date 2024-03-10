import tkinter as tk
from tkinter import messagebox
import threading
import time
import os

class IdleFactoryGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Idle Factory Game")
        self.master.geometry("400x350")

        self.data_file = os.path.join(os.getenv("APPDATA"), "idle_factory_game_data.txt")

        self.load_progress()

        self.create_widgets()

        # Start auto-producing money in a separate thread
        self.auto_produce_thread = threading.Thread(target=self.auto_produce_money)
        self.auto_produce_thread.daemon = True
        self.auto_produce_thread.start()

    def load_progress(self):
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                lines = file.readlines()
                self.money = int(lines[0].strip())
                self.production_rate = int(lines[1].strip())
        else:
            self.money = 0
            self.production_rate = 1

    def save_progress(self):
        with open(self.data_file, "w") as file:
            file.write(f"{self.money}\n")
            file.write(f"{self.production_rate}\n")

    def create_widgets(self):
        # Frame for the money display
        money_frame = tk.Frame(self.master)
        money_frame.pack(pady=10)

        # Money label
        self.money_label = tk.Label(money_frame, text="Money: $0", font=("Arial", 14))
        self.money_label.pack(side=tk.LEFT, padx=10)

        # Frame for the production rate display
        production_frame = tk.Frame(self.master)
        production_frame.pack(pady=10)

        # Production rate label
        self.production_rate_label = tk.Label(production_frame, text="Production Rate: 1 per second", font=("Arial", 14))
        self.production_rate_label.pack(side=tk.LEFT, padx=10)

        # Upgrade cost label
        self.upgrade_cost_label = tk.Label(self.master, text="", font=("Arial", 12))
        self.upgrade_cost_label.pack(pady=5)

        # Button to manually produce money
        self.produce_button = tk.Button(self.master, text="Produce", command=self.produce, font=("Arial", 12), bg="lightblue", padx=10)
        self.produce_button.pack(pady=5)

        # Button to upgrade production rate
        self.upgrade_button = tk.Button(self.master, text="Upgrade Production Rate", command=self.upgrade_production_rate, font=("Arial", 12), bg="lightgreen", padx=10)
        self.upgrade_button.pack(pady=5)

        # Save progress button
        self.save_button = tk.Button(self.master, text="Save Progress", command=self.save_progress, font=("Arial", 12), bg="lightgrey", padx=10)
        self.save_button.pack(pady=5)

        # Reset progress button
        self.reset_button = tk.Button(self.master, text="Reset Progress", command=self.reset_progress, font=("Arial", 12), bg="red", fg="white", padx=10)
        self.reset_button.pack(pady=5)

    def produce(self):
        self.money += self.production_rate
        self.update_display()

    def upgrade_production_rate(self):
        upgrade_cost = 10 * self.production_rate  # Cost increases with current production rate
        if self.money >= upgrade_cost:
            self.money -= upgrade_cost
            self.production_rate += 1
            self.update_display()
        else:
            needed_money = upgrade_cost - self.money
            messagebox.showwarning("Insufficient Funds", f"You need ${needed_money} more to upgrade the production rate.")

    def auto_produce_money(self):
        while True:
            self.money += self.production_rate
            self.update_display()
            self.save_progress()  # Save progress every iteration
            time.sleep(1)  # Auto-save interval: 5 seconds

    def reset_progress(self):
        confirm = messagebox.askyesno("Reset Progress", "Are you sure you want to reset your progress?")
        if confirm:
            self.money = 0
            self.production_rate = 1
            self.save_progress()
            self.update_display()

    def update_display(self):
        self.money_label.config(text=f"Money: ${self.money}")
        self.production_rate_label.config(text=f"Production Rate: {self.production_rate} per second")
        upgrade_cost = 10 * self.production_rate
        self.upgrade_cost_label.config(text=f"Upgrade Cost: ${upgrade_cost}")

def main():
    root = tk.Tk()
    game = IdleFactoryGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
