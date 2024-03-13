import tkinter as tk  # Importing tkinter for GUI
from tkinter import messagebox  # Importing messagebox for user alerts
import threading  # Importing threading for auto-producing money
import time  # Importing time for auto-save interval
import os  # Importing os for accessing appdata

class IdleFactoryGame:
    def __init__(self, master):
        # Initialize the IdleFactoryGame class with a tkinter master (main window)
        self.master = master
        self.master.title("Idle Factory Game")
        self.master.geometry("400x350")

        self.data_file = os.path.join(os.getenv("APPDATA"), "idle_factory_game_data.txt")
        # Set the data file path to store the game progress in the user's appdata folder

        self.load_progress()  # Load the game progress from the data file

        self.create_widgets()  # Create all the GUI widgets

        # Start auto-producing money in a separate thread
        self.auto_produce_thread = threading.Thread(target=self.auto_produce_money)
        self.auto_produce_thread.daemon = True
        self.auto_produce_thread.start()

    def load_progress(self):
        # Load game progress from the data file
        if os.path.exists(self.data_file):
            with open(self.data_file, "r") as file:
                lines = file.readlines()
                self.money = int(lines[0].strip())  # Load money
                self.production_rate = int(lines[1].strip())  # Load production rate
        else:
            self.money = 0  # Initialize money
            self.production_rate = 1  # Initialize production rate

    def save_progress(self):
        # Save game progress to the data file
        with open(self.data_file, "w") as file:
            file.write(f"{self.money}\n")  # Save money
            file.write(f"{self.production_rate}\n")  # Save production rate

    def create_widgets(self):
        # Create all the GUI widgets

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
        # Manually produce money
        self.money += self.production_rate
        self.update_display()

    def upgrade_production_rate(self):
