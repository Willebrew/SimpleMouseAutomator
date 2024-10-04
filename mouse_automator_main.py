"""
This module provides a simple mouse automation tool using PyQt5.
"""

import sys
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
from pynput import keyboard
from mouse_automator_package import MouseAutomation


class SimpleMouseAutomator(QWidget):
    """A simple GUI application for recording and replaying mouse actions."""

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.threads = {'recording': None, 'playback': None}
        self.movements = []
        self.countdown = {
            'timer': QTimer(self),
            'value': 3
        }
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()
        self.mouse_automation = MouseAutomation()

    def init_ui(self):
        """Initialize the user interface."""
        layout = QVBoxLayout()

        header_label = QLabel('Simple Mouse Automator', self)
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont('Arial', 20, QFont.Bold))
        layout.addWidget(header_label)

        self.record_button = QPushButton('Start Recording', self)
        self.play_button = QPushButton('Play', self)

        button_style = """
            QPushButton {
                background-color: #3498db;
                border-radius: 10px;
                color: white;
                padding: 15px;
                text-align: center;
                font-size: 16px;
                margin: 10px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        """
        self.record_button.setStyleSheet(button_style)
        self.play_button.setStyleSheet(button_style)

        self.record_button.clicked.connect(self.start_countdown)
        self.play_button.clicked.connect(self.on_play)

        layout.addWidget(self.record_button)
        layout.addWidget(self.play_button)

        version_label = QLabel('Version 0.1.4', self)
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont('Arial', 10))

        layout.addWidget(version_label)

        self.setLayout(layout)
        self.setWindowTitle('Simple Mouse Automator')
        self.setGeometry(300, 300, 400, 350)

    def start_countdown(self):
        """Start the countdown before recording."""
        if not self.threads['recording'] or not self.threads['recording'].is_alive():
            self.countdown['value'] = 3
            self.countdown['timer'].timeout.connect(self.update_countdown)
            self.countdown['timer'].start(1000)

    def update_countdown(self):
        """Update the countdown timer."""
        if self.countdown['value'] > 0:
            self.record_button.setText(f"Starting in {self.countdown['value']}...")
            self.countdown['value'] -= 1
        else:
            self.countdown['timer'].stop()
            self.countdown['timer'].timeout.disconnect(self.update_countdown)
            self.on_start_recording()

    def on_start_recording(self):
        """Start recording mouse movements."""
        if not self.threads['recording'] or not self.threads['recording'].is_alive():
            print("Recording Started...")
            self.record_button.setText("Press Q to Stop Recording")
            self.threads['recording'] = threading.Thread(target=self.record_movements)
            self.threads['recording'].start()

    def record_movements(self):
        """Record mouse movements and clicks."""
        self.movements = self.mouse_automation.record_mouse_movements_and_clicks()
        print("Recording complete.")
        self.record_button.setText("Start Recording")

    def on_play(self):
        """Play back recorded mouse movements."""
        if not self.movements:
            QMessageBox.warning(
                self,
                "No Movements Recorded",
                "You must record movements before playing them back."
            )
            return

        if not self.threads['playback'] or not self.threads['playback'].is_alive():
            if self.movements:
                print("Playing movements...")
                self.play_button.setText("Press Q to Stop Playback")
                self.threads['playback'] = threading.Thread(target=self.play_movements)
                self.threads['playback'].start()

    def play_movements(self):
        """Replay recorded mouse movements and clicks."""
        self.mouse_automation.replay_mouse_movements_and_clicks(self.movements)
        self.play_button.setText("Play")
        print("Playback complete.")

    def stop_all(self):
        """Stop all ongoing actions."""
        print("Stopping...")
        if hasattr(self.mouse_automation, 'stop_recording_func'):
            getattr(self.mouse_automation, 'stop_recording_func')()
        if hasattr(self.mouse_automation, 'stop_playback_func'):
            getattr(self.mouse_automation, 'stop_playback_func')()
        if not (self.threads['recording'] and
            (self.threads['recording'].is_alive() or
            (self.threads['playback'] and
            (self.threads['playback'].is_alive())))):
            print("Playback stopped.")
        if hasattr(self.mouse_automation, 'stop_recording_func'):
            getattr(self.mouse_automation, 'stop_recording_func')()
        if hasattr(self.mouse_automation, 'stop_playback_func'):
            getattr(self.mouse_automation, 'stop_playback_func')()

    def on_press(self, key):
        """Handle global key press events."""
        try:
            if key.char == 'q':
                print("Stopping all actions...")
                if hasattr(self.mouse_automation, 'stop_recording_func'):
                    getattr(self.mouse_automation, 'stop_recording_func')()
                if hasattr(self.mouse_automation, 'stop_playback_func'):
                    getattr(self.mouse_automation, 'stop_playback_func')()
                if not (self.threads['recording'] and
                        (self.threads['recording'].is_alive() or
                         (self.threads['playback'] and
                          (self.threads['playback'].is_alive())))):
                    print("Playback stopped.")
                    if hasattr(self.mouse_automation, 'stop_recording_func'):
                        getattr(self.mouse_automation, 'stop_recording_func')()
                    if hasattr(self.mouse_automation, 'stop_playback_func'):
                        getattr(self.mouse_automation, 'stop_playback_func')()
        except AttributeError:
            pass


def main():
    """Run the application."""
    app = QApplication(sys.argv)
    ex = SimpleMouseAutomator()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
