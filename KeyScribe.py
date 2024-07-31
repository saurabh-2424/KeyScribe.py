# KeyScribe.py

import tkinter as tk
from tkinter import messagebox
from pynput.keyboard import Listener, Key
import logging
import os

class KeyScribe:
    def __init__(self, master):
        self.master = master
        master.title("KeyScribe")

        self.label = tk.Label(master, text="Press Start to begin logging.")
        self.label.pack(pady=10)

        self.start_button = tk.Button(master, text="Start", command=self.start_logging)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_logging, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.listener = None

    def start_logging(self):
        self.label.config(text="Logging started. Press Stop to stop logging.")
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Minimize the Tkinter window
        self.master.iconify()

        # Configure logging with explicit path
        log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keylog.txt")
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

        # Start listener
        self.listener = Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def stop_logging(self):
        self.label.config(text="Logging stopped. Press Start to begin logging.")
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

        # Stop listener
        if self.listener:
            self.listener.stop()
            self.listener = None

        # Close the Tkinter window
        self.master.destroy()

    def on_press(self, key):
        try:
            logging.info(f'Key pressed: {key.char}')
        except AttributeError:
            logging.info(f'Special key pressed: {key}')

    def on_release(self, key):
        if key == Key.esc:
            # Stop listener when Esc key is pressed
            return False

def main():
    root = tk.Tk()
    app = KeyScribe(root)
    root.mainloop()

if __name__ == "__main__":
    main()
