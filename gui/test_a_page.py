from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import threading
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import time

class TestAPage(QWidget):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.layout = QVBoxLayout()
        
        self.title_label = QLabel('Test B - Vertical', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont('Arial', 18, QFont.Bold))
        self.title_label.setStyleSheet('color: #4A90E2;')
        self.layout.addWidget(self.title_label)

        self.recording = False
        self.speech_thread = None
        self.result = None
        
        self.record_button = QPushButton('Record', self)
        self.record_button.setFont(QFont('Arial', 14))
        self.record_button.setStyleSheet('''
            background-color: #4A90E2;
            color: white;
            border-radius: 5px;
            padding: 10px;
        ''')
        self.record_button.setCursor(Qt.PointingHandCursor)
        self.record_button.clicked.connect(self.start_recognition)
        self.layout.addWidget(self.record_button)

        self.stop_button = QPushButton("Stop Recognition", self)
        self.stop_button.clicked.connect(self.stop_recognition)
        self.layout.addWidget(self.stop_button)
        
        self.setLayout(self.layout)
        
    def start_recognition(self):
        if not self.recording:
            self.recording = True
            self.speech_thread = threading.Thread(target=self.recognize_from_microphone)
            self.speech_thread.start()

    def stop_recognition(self):
        if self.recording:
            self.recording = False
            if self.speech_thread is not None:
                self.speech_thread.join()

    def recognize_from_microphone(self):
        # configuring speech_config parameter with key, region, and language
        speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))
        speech_config.speech_recognition_language = "en-US"

        # configuring audio_config with using the default microphone
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        
        # recognized_text and duration will be returned at the end of this function
        recognized_text = ""
        duration = 0

        # taking a starting time right before recording starts
        start_time = time.time()

        # callback function for generating recognized_text and error handling
        def recognized_cb(evt):
            nonlocal recognized_text
            if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
                recognized_text += evt.result.text
            elif evt.result.reason == speechsdk.ResultReason.NoMatch:
                print("No speech could be recognized: {}".format(evt.result.no_match_details))
            elif evt.result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = evt.result.cancellation_details
                print("Speech Recognition canceled: {}".format(cancellation_details.reason))
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    print("Error details: {}".format(cancellation_details.error_details))
                    print("Did you set the speech resource key and region values?")

        # callback function is called when speech is recognized
        speech_recognizer.recognized.connect(recognized_cb)

        # microphone is continuously listening for speech
        print("Speak into the microphone.")
        speech_recognizer.start_continuous_recognition()

        # function continuously runs until recognition is stopped
        while self.recording:
            time.sleep(0.1)
        
        end_time = time.time()
        print("Stopping recognition...")
        duration = end_time - start_time
        time.sleep(2)
        speech_recognizer.stop_continuous_recognition()

        # Store the result in the shared variable
        self.result = {"text": recognized_text, "duration": duration}
        print(self.result)

    def update_test_a(self, text):
        self.title_label.setText(text)

    