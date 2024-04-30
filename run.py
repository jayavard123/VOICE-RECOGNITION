import tkinter as tk
from tkinter import ttk
import speech_recognition as sr
import pyttsx3
import threading
import spacy
import random
from PIL import Image, ImageTk

class SpeechApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speech Processing App")

        # Load background image and resize it
        image = Image.open("C:\\Users\\pvjay\\OneDrive\\Desktop\\voice recognition\\background_image.png")
        image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(image)
        self.background_label = tk.Label(root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Increase font size for better readability
        self.font = ('Helvetica', 16)

        # Labels and Buttons
        self.label = ttk.Label(root, text="Press 'Start Recording' to speak.", font=self.font)
        self.label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        self.record_button = ttk.Button(root, text="Start Recording", command=self.start_recording, style='TButton', width=15)
        self.record_button.place(relx=0.3, rely=0.2, anchor=tk.CENTER)

        self.stop_button = ttk.Button(root, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED, style='TButton', width=15)
        self.stop_button.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        self.clear_button = ttk.Button(root, text="Clear", command=self.clear_all, style='TButton', width=15)
        self.clear_button.place(relx=0.7, rely=0.2, anchor=tk.CENTER)

        # Text Areas
        self.input_label = ttk.Label(root, text="Input:", font=self.font)
        self.input_label.place(relx=0.2, rely=0.3, anchor=tk.CENTER)

        self.input_text = tk.Text(root, height=4, width=50, font=self.font)
        self.input_text.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        self.output_label = ttk.Label(root, text="Output:", font=self.font)
        self.output_label.place(relx=0.2, rely=0.6, anchor=tk.CENTER)

        self.output_text = tk.Text(root, height=4, width=50, state=tk.DISABLED, font=self.font)
        self.output_text.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

        # Initialize components
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.nlp = spacy.load("en_core_web_sm")

        self.root.state('zoomed')


    def start_recording(self):
        self.record_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.clear_button.config(state=tk.DISABLED)
        self.label.config(text="Recording...", foreground='green')

        self.audio = sr.Microphone()
        self.is_recording = True
        self.recording_thread = threading.Thread(target=self.record)
        self.recording_thread.start()

    def record(self):
        with self.audio as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_recording:
                try:
                    audio_data = self.recognizer.listen(source, timeout=None)  # Continuous listening
                    text = self.recognizer.recognize_google(audio_data)
                    self.input_text.insert(tk.END, text + '\n')
                    self.process_input(text)
                except sr.WaitTimeoutError:
                    pass
                except sr.UnknownValueError:
                    self.input_text.insert(tk.END, "Unknown input\n")
                    self.process_input("Unknown input")

    def stop_recording(self):
        self.is_recording = False
        self.record_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.clear_button.config(state=tk.NORMAL)
        self.label.config(text="Press 'Start Recording' to speak.", foreground='black')

    def process_input(self, text):
        response = self.generate_response(text)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, response)
        self.output_text.config(state=tk.DISABLED)

        # Convert text to speech
        self.engine.say(response)
        self.engine.runAndWait()

    def generate_response(self, input_text):
        input_text = input_text.lower()
        doc = self.nlp(input_text)

        # Common response patterns
        greetings = ["hello", "hi", "hey"]
        gratitude = ["thank you", "thanks"]
        farewells = ["goodbye", "bye"]
        weather_queries = ["weather"]
        time_queries = ["time"]
        unknown_responses = ["I'm sorry, I didn't catch that. Can you please repeat or ask something else?",
                            "I'm not sure I understand. Could you please provide more context?"]

        # Check for specific keywords in the input
        if any(token.text in greetings for token in doc):
            return "Hello! How can I assist you today?"
        elif any(token.text in gratitude for token in doc):
            return "You're welcome! Is there anything else I can help with?"
        elif any(token.text in farewells for token in doc):
            return "Goodbye! Have a great day!"
        elif any(token.text in weather_queries for token in doc):
            return "Sure, let me check the weather for you."
        elif any(token.text in time_queries for token in doc):
            return "The current time is [insert current time here]."
        else:
            return random.choice(unknown_responses)

    def clear_all(self):
        self.input_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete(1.0, tk.END)
        self.output_text.config(state=tk.DISABLED)

def main():
    root = tk.Tk()
    style = ttk.Style()
    style.configure('TButton', font=('Helvetica', 12))
    app = SpeechApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()