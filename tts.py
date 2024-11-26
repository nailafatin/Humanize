import edge_tts
import io
import pygame
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import asyncio
import threading

# Fetch audio
async def fetch_audio(text, assistant_voice="en-US-EricNeural", pitch="+0Hz", rate="+0%") -> bytes:
    try:
        communicate = edge_tts.Communicate(text, assistant_voice, pitch=pitch, rate=rate)
        audio_bytes = b""
        async for element in communicate.stream():
            if element["type"] == "audio":
                audio_bytes += element["data"]
        return audio_bytes
    except Exception as e:
        print(f"Error: {e}")
        return b""

# Wrapper function
async def text_to_speech_bytes(text: str, assistant_voice="en-US-EricNeural", pitch="+0Hz", rate="+0%") -> bytes:
    return await fetch_audio(text, assistant_voice, pitch, rate)

# Audio player class
class AudioPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.channel = None
        self.sound = None
        self.volume = 1

    def play(self, audio_bytes: bytes) -> None:
        try:
            audio_file = io.BytesIO(audio_bytes)
            self.sound = pygame.mixer.Sound(audio_file)
            if self.channel and self.channel.get_busy():
                self.channel.stop()
            self.channel = self.sound.play()
            self.channel.set_volume(self.volume)
        except Exception as e:
            print(f"Playback Error: {e}")

    def stop(self):
        if self.channel and self.channel.get_busy():
            self.channel.stop()

    def set_volume(self, volume: float):
        if self.channel:
            self.channel.set_volume(volume)
        self.volume = volume

# Global player instance
player = AudioPlayer()

# Voice options with culture
voice_options = [
    ("en-US-EricNeural", "Male", "English (US)"),
    ("en-US-GuyNeural", "Male",  "English (US)"),
    ("en-US-JennyNeural", "Female", "English (US)"),
    ("en-US-AriaNeural", "Female", "English (US)"),
    ("en-GB-RyanNeural", "Male", "English (UK)"),
    ("fr-FR-DeniseNeural", "Female", "French (France)"),
    ("fr-FR-HenriNeural", "Male", "French (France)"),
    ("pt-PT-DuarteNeural", "Male", "Portuguese (Portugal)"),
    ("ja-JP-KeitaNeural", "Male", "Japanese (Japan)"),
    ("zh-CN-XiaoxiaoNeural", "Female", "Chinese (Mandarin)"),
    ("zh-CN-YunyangNeural", "Male", "Chinese (Mandarin)"),
    ("cs-CZ-AntoninNeural", "Male", "Czech (Czech Republic)"),
    ("bg-BG-KalinaNeural", "Female", "Bulgarian (Bulgaria)"),
]

def get_text_input():
    root = tk.Tk()
    root.title("")
    root.geometry("350x350")
    root.config(bg="#1e1e1e")

    # Title
    tk.Label(root, text="HUMANIZER", font=("Arial", 14, "bold"), fg="#ffffff", bg="#1e1e1e").pack(pady=10)

    # Text input
    text_input = tk.Text(root, height=4, width=50, font=("Arial", 10), bg="#2e2e2e", fg="#ffffff", insertbackground="#ffffff")
    text_input.pack(pady=10)

    # Controls frame
    controls_frame = tk.Frame(root, bg="#1e1e1e")
    controls_frame.pack(pady=10)

    # Style customization for dropdown
    style = ttk.Style()
    style.theme_use("clam")
    style.configure(
        "TCombobox",
        fieldbackground="#2e2e2e",
        background="#1e1e1e",
        foreground="#ffffff",
        bordercolor="#4caf50",
        arrowcolor="#ffffff"
    )

    dropdown_values = [
    f"{voice[0]} | {voice[1]} | {voice[2]}"
    for voice in voice_options
    ]

    voice_combo = ttk.Combobox(
        controls_frame, 
        values=dropdown_values, 
        state="readonly", 
        font=("Arial", 10), 
        width=40, 
        style="TCombobox"
    )
    voice_combo.set(dropdown_values[0])  # Default voice
    voice_combo.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

    # Sliders
    tk.Label(controls_frame, text="Pitch:", font=("Arial", 10), fg="#ffffff", bg="#1e1e1e").grid(row=1, column=0, sticky="e", padx=5)
    pitch_scale = tk.Scale(controls_frame, from_=0, to=100, orient="horizontal", bg="#2e2e2e", fg="#ffffff", sliderlength=15)
    pitch_scale.set(0)
    pitch_scale.grid(row=1, column=1)

    tk.Label(controls_frame, text="Rate:", font=("Arial", 10), fg="#ffffff", bg="#1e1e1e").grid(row=2, column=0, sticky="e", padx=5)
    rate_scale = tk.Scale(controls_frame, from_=0, to=100, orient="horizontal", bg="#2e2e2e", fg="#ffffff", sliderlength=15)
    rate_scale.set(0)
    rate_scale.grid(row=2, column=1)

    # Status
    status_label = tk.Label(root, text="", font=("Arial", 10), fg="#ffcc00", bg="#1e1e1e")
    status_label.pack(pady=5)

    # Generate button
    def on_generate(event=None):
        text = text_input.get("1.0", "end-1c").strip()
        selected_voice_info = voice_combo.get().split(" | ")
        if not text:
            messagebox.showwarning("Input Error", "Please enter some text.")
            return

        selected_voice = selected_voice_info[0]
        pitch = f"+{pitch_scale.get()}Hz"
        rate = f"+{rate_scale.get()}%"

        status_label.config(text="Generating...")
        threading.Thread(target=generate_audio, args=(text, selected_voice, pitch, rate)).start()

    generate_button = tk.Button(controls_frame, text="Generate", font=("Arial", 10, "bold"), bg="#4caf50", fg="#ffffff", command=on_generate)
    generate_button.grid(row=3, column=0, columnspan=3, pady=10)

    # Bind Enter key to Generate button
    root.bind("<Return>", on_generate)

    # Generate audio
    def generate_audio(text, voice, pitch, rate):
        try:
            player.stop()
            audio_bytes = asyncio.run(text_to_speech_bytes(text, assistant_voice=voice, pitch=pitch, rate=rate))
            if audio_bytes:
                player.play(audio_bytes)
                status_label.config(text="Playing audio...")
                if messagebox.askyesno("Download", "Save the audio file?"):
                    file_path = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV files", "*.wav")])
                    if file_path:
                        with open(file_path, "wb") as file:
                            file.write(audio_bytes)
                        messagebox.showinfo("Success", "Audio saved successfully.")
        except Exception as e:
            status_label.config(text="Error.")
            print(f"Error: {e}")

    root.mainloop()

if __name__ == "__main__":
    get_text_input()
