import keyboard
import time
from mss import mss
from threading import Thread
import os
import json
from PIL import Image
from pynput import mouse


class ActionLogger:
    def __init__(self, capture_rate=10, output_folder='output', resize_factor=3.16):
        self.capture_rate = capture_rate
        self.running = False
        self.mouse_positions = []
        self.key_presses = []
        self.clicks = []
        self.image_data = []
        self.output_folder = output_folder
        self.screen_counter = 0
        self.resize_factor = resize_factor
        self.start_time = time.time()

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        self.save_meta_data()

    def save_meta_data(self):
        meta_data = {
            'image_resolution': (int(mss().monitors[0]['width'] / self.resize_factor),
                                 int(mss().monitors[0]['height'] / self.resize_factor)),
            'start_time': self.start_time,
            'rescale_factor': self.resize_factor
        }

        with open(os.path.join(self.output_folder, 'meta_data.json'), 'w') as outfile:
            json.dump(meta_data, outfile)

    def log_mouse_position(self, x, y):
        timestamp = time.time()
        self.mouse_positions.append({'name': f"mouse_position {x} {y}", 'time': timestamp})

    def on_click(self, x, y, button, pressed):
        if pressed:
            click = {'name': f"{str(button.name)}+click", 'time': time.time()}
            self.clicks.append(click)

    def stop(self):
        self.running = False
        self.keyboard_thread.join(timeout=1)
        self.mouse_listener.stop()

    def run(self, capture_duration, save_every=60):
        self.start()

        start_time = time.time()
        last_save_time = start_time

        try:
            while time.time() - start_time < capture_duration:
                current_time = time.time()
                time_elapsed = current_time - last_save_time
                recording_duration = current_time - start_time
                print(f"\rRecording for {recording_duration:.2f} seconds. Saving data to {self.output_folder}", end='', flush=True)

                self.log_screen()

                if time_elapsed >= save_every:
                    self.save_data()
                    last_save_time = time.time()

                time.sleep(1 / self.capture_rate)
        except KeyboardInterrupt:
            self.stop()

    def log_screen(self):
        with mss() as sct:
            monitor = sct.monitors[0]
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            resized_img = img.resize((int(screenshot.width / self.resize_factor), int(screenshot.height / self.resize_factor)))
            filename = os.path.join(self.output_folder, f'screen_{self.screen_counter}.png')
            resized_img.save(filename)
            self.image_data.append({'image_path': filename, 'time': time.time()})
            self.screen_counter += 1
            return filename

    def keyboard_listener(self):
        while self.running:
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                self.key_presses.append({'name': event.name, 'time': event.time})
            elif event.event_type == keyboard.KEY_UP:
                self.key_presses.append({'name': f"up {event.name}", 'time': event.time})

    def save_data(self):
        with open(os.path.join(self.output_folder, 'mouse_positions.json'), 'w') as outfile:
            json.dump(self.mouse_positions, outfile)

        with open(os.path.join(self.output_folder, 'key_presses.json'), 'w') as outfile:
            json.dump(self.key_presses, outfile)

        with open(os.path.join(self.output_folder, 'clicks.json'), 'w') as outfile:
            json.dump(self.clicks, outfile)

        with open(os.path.join(self.output_folder, 'image_data.json'), 'w') as outfile:
            json.dump(self.image_data, outfile)

    def start(self):
        self.running = True
        self.keyboard_thread = Thread(target=self.keyboard_listener)
        self.keyboard_thread.start()

        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.log_mouse_position)
        self.mouse_listener.start()

    def stop(self):
        self.running = False
        self.keyboard_thread.join(timeout=1)
        self.mouse_listener.stop()