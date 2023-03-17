import pyautogui
import keyboard
import time
from mss import mss
from threading import Thread
import os
import json
from PIL import Image

class ActionLogger:
    def __init__(self, capture_rate=10, output_folder='output', resize_factor=3.16):
        self.capture_rate = capture_rate
        self.running = False
        self.keyboard_buffer = []
        self.output_folder = output_folder
        self.screen_counter = 0
        self.screen_timestamps = []
        self.resize_factor = resize_factor
        self.start_time = None
        self.end_time = None
        self.mouse_positions = []  # Add this line to store the mouse positions as an instance variable
        
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)


    def log_mouse_position(self):
        position = pyautogui.position()
        return {'x': position.x, 'y': position.y, 'time': time.time()}

    def log_screen(self):
        with mss() as sct:
            monitor = sct.monitors[0]
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            resized_img = img.resize((int(screenshot.width / self.resize_factor), int(screenshot.height / self.resize_factor)))
            filename = os.path.join(self.output_folder, f'screen_{self.screen_counter}.png')
            resized_img.save(filename)
            timestamp = time.time()
            self.screen_timestamps.append({'path': filename, 'time': timestamp})
            self.screen_counter += 1
            return filename

    def keyboard_listener(self):
        while self.running:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                self.keyboard_buffer.append({'name': event.name, 'time': event.time})

    def save_mouse_positions(self, mouse_positions):
        with open(os.path.join(self.output_folder, 'mouse_positions.json'), 'w') as f:
            json.dump(mouse_positions, f)

    def save_keyboard_buffer(self):
        with open(os.path.join(self.output_folder, 'keyboard_buffer.json'), 'w') as f:
            json.dump(self.keyboard_buffer, f)

    def save_screen_timestamps(self):
        metadata = {
            'screen_timestamps': self.screen_timestamps,
            'resize_factor': self.resize_factor,
            'original_screen_size': (pyautogui.size().width, pyautogui.size().height),
            'start_time': self.start_time,
            'end_time': self.end_time
        }
        with open(os.path.join(self.output_folder, 'screen_metadata.json'), 'w') as f:
            json.dump(metadata, f)

    def start(self):
        self.running = True
        self.start_time = time.time()
        self.keyboard_thread = Thread(target=self.keyboard_listener)
        self.keyboard_thread.start()

    def stop(self):
        self.running = False
        self.end_time = time.time()
        self.keyboard_thread.join()

    def run(self, capture_duration, save_every=60):
        self.start()
        
        start_time = time.time()
        last_save_time = start_time
        

        # Add this print statement to display the recording duration and output location
       


        while time.time() - start_time < capture_duration:
            current_time = time.time()
            time_elapsed = current_time - last_save_time
            recording_duration = current_time - start_time
            print(f"\rRecording for {recording_duration:.2f} seconds. Saving data to {self.output_folder}", end='', flush=True)

            self.mouse_positions.append(self.log_mouse_position())  # Update this line
            self.log_screen()
            
            time_elapsed = time.time() - last_save_time
            if time_elapsed >= save_every:
                self.save_mouse_positions(self.mouse_positions)  # Update this line
                self.save_keyboard_buffer()
                self.save_screen_timestamps()
                last_save_time = time.time()

            time.sleep(1 / self.capture_rate)

        self.stop()

        self.save_mouse_positions(self.mouse_positions)  # Update this line

