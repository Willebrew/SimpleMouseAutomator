"""
This module provides a simple mouse automation interface using pynput and pyautogui.
"""

import time
import random
import pyautogui
from pynput import mouse

# Configure PyAutoGUI settings
pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

class MouseAutomation:
    """
        A class to automate mouse movements and clicks.

        This class provides methods to record and replay mouse movements and clicks using
        the pynput and pyautogui libraries. It supports stopping recording and replaying
        actions through dedicated methods.
        """
    def __init__(self):
        self.stop_recording = False
        self.stop_replaying = False

    def record_mouse_movements_and_clicks(self):
        """
        Record mouse movements and clicks until stopped.

        Returns:
            list: A list of tuples containing recorded mouse actions.
        """
        movements = []
        self.stop_recording = False

        def on_move(x, y):
            """Callback for mouse movement."""
            movements.append(('move', x, y))

        def on_click(x, y, button, pressed):
            """Callback for mouse clicks."""
            if pressed:
                movements.append(('click', x, y, button))

        mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
        mouse_listener.start()

        while not self.stop_recording:
            time.sleep(0.01)

        mouse_listener.stop()
        return movements

    def replay_mouse_movements_and_clicks(self, movements):
        """
        Replay recorded mouse movements and clicks.

        Args:
            movements (list): A list of tuples containing recorded mouse actions.
        """
        self.stop_replaying = False
        repetition_count = 0

        while not self.stop_replaying:
            for action in movements:
                if self.stop_replaying:
                    break
                if action[0] == 'move':
                    _, x, y = action
                    pyautogui.moveTo(x, y)
                elif action[0] == 'click':
                    _, x, y, button = action
                    pyautogui.click(x=x, y=y, button=button.name)

            repetition_count += 1

            if repetition_count % 2 == 0:
                wait_time = random.uniform(3, 7)
                print(f"Waiting for {wait_time:.2f} seconds before next repetition...")
                time.sleep(wait_time)

    def stop_recording_func(self):
        """
        Stop recording mouse movements and clicks.
        """
        self.stop_recording = True

    def stop_playback_func(self):
        """
        Stop replaying mouse movements and clicks.
        """
        self.stop_replaying = True
