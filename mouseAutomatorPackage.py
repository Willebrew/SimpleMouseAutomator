import pyautogui
import time
import random
from pynput import mouse

pyautogui.PAUSE = 0
pyautogui.FAILSAFE = False

stop_recording = False

def record_mouse_movements_and_clicks():
    global stop_recording
    movements = []
    stop_recording = False

    def on_move(x, y):
        movements.append(('move', x, y))

    def on_click(x, y, button, pressed):
        if pressed:
            movements.append(('click', x, y, button))

    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    mouse_listener.start()

    while not stop_recording:
        time.sleep(0.01)

    mouse_listener.stop()
    return movements

def replay_mouse_movements_and_clicks(movements):
    global stop_replaying
    stop_replaying = False

    repetition_count = 0

    while not stop_replaying:
        for action in movements:
            if stop_replaying:
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

def stop_recording_func():
    global stop_recording
    stop_recording = True

def stop_playback_func():
    global stop_replaying
    stop_replaying = True
