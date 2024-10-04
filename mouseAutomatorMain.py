import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QTimer
import threading
import mouseAutomatorPackage as ma
from pynput import keyboard


class SimpleMouseAutomator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.recording_thread = None
        self.playback_thread = None
        self.movements = []
        self.countdown_timer = QTimer(self)
        self.countdown_value = 3

        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def initUI(self):
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

        version_label = QLabel('Version 0.1.2', self)
        version_label.setAlignment(Qt.AlignCenter)
        version_label.setFont(QFont('Arial', 10))

        layout.addWidget(version_label)

        self.setLayout(layout)
        self.setWindowTitle('Simple Mouse Automator')
        self.setGeometry(300, 300, 400, 350)

    def start_countdown(self):
        if not self.recording_thread or not self.recording_thread.is_alive():
            self.countdown_value = 3
            self.countdown_timer.timeout.connect(self.update_countdown)
            self.countdown_timer.start(1000)

    def update_countdown(self):
        if self.countdown_value > 0:
            self.record_button.setText(f"Starting in {self.countdown_value}...")
            self.countdown_value -= 1
        else:
            self.countdown_timer.stop()
            self.countdown_timer.timeout.disconnect(self.update_countdown)
            self.on_start_recording()

    def on_start_recording(self):
        if not self.recording_thread or not self.recording_thread.is_alive():
            print("Recording Started...")
            self.record_button.setText("Press Q to Stop Recording")
            self.recording_thread = threading.Thread(target=self.record_movements)
            self.recording_thread.start()

    def record_movements(self):
        self.movements = ma.record_mouse_movements_and_clicks()
        print("Recording complete.")
        self.record_button.setText("Start Recording")

    def on_play(self):
        if not self.movements:
            QMessageBox.warning(self, "No Movements Recorded", "You must record movements before playing them back.")
            return

        if not self.playback_thread or not self.playback_thread.is_alive():
            if self.movements:
                print("Playing movements...")
                self.play_button.setText("Press Q to Stop Playback")
                self.playback_thread = threading.Thread(target=self.play_movements)
                self.playback_thread.start()

    def play_movements(self):
        ma.replay_mouse_movements_and_clicks(self.movements)
        print("Playback complete.")
        if not ma.stop_playback_func():
            self.play_button.setText("Play")

    def stop_all(self):
        print("Stopping...")
        ma.stop_recording_func()

        if ma.stop_playback_func():
            print("Playback stopped.")

        if not (self.playback_thread and self.playback_thread.is_alive()):
            print("Resetting play button text.")
            self.play_button.setText("Play")

    def on_press(self, key):
        try:
            if key.char == 'q':
                self.stop_all()

                if not (self.recording_thread and self.recording_thread.is_alive()):
                    self.record_button.setText("Start Recording")

                if not (self.playback_thread and self.playback_thread.is_alive()):
                    self.play_button.setText("Play")
        except AttributeError:
            pass


def main():
    app = QApplication(sys.argv)
    ex = SimpleMouseAutomator()
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()