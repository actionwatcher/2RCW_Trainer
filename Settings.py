import tkinter as tk
from tkinter import ttk
import shelve

class SettingsWindow:
    def __init__(self, root, create_second_window, close_second_window):
        self.create_second_window = create_second_window
        self.close_second_window = close_second_window

        # Load settings if available
        self.window = tk.Toplevel(root)
        self.window.title("Settings")
        self.window.geometry("400x300")

        # Initialize mode_var
        self.mode_var = tk.StringVar()

        # Create the notebook (tab container)
        self.notebook = ttk.Notebook(self.window)
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # General tab
        general_frame = ttk.Frame(self.notebook)
        self.notebook.add(general_frame, text="General")

        # Contest Selection
        contest_label = ttk.Label(general_frame, text="Contest Selection:")
        contest_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.contest_entry = ttk.Entry(general_frame)
        self.contest_entry.grid(row=0, column=1, padx=10, pady=5)

        # SO1R, SO2R, 2BSIQ Radio Buttons
        mode_label = ttk.Label(general_frame, text="Operating Mode:")
        mode_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        so1r_button = ttk.Radiobutton(general_frame, text="SO1R", variable=self.mode_var, value="SO1R", command=self.update_windows)
        so2r_button = ttk.Radiobutton(general_frame, text="SO2R", variable=self.mode_var, value="SO2R", command=self.update_windows)
        twobs_button = ttk.Radiobutton(general_frame, text="2BSIQ", variable=self.mode_var, value="2BSIQ", command=self.update_windows)
        so1r_button.grid(row=2, column=0, padx=10, pady=2, sticky="w")
        so2r_button.grid(row=3, column=0, padx=10, pady=2, sticky="w")
        twobs_button.grid(row=4, column=0, padx=10, pady=2, sticky="w")

        # Audio tab
        audio_frame = ttk.Frame(self.notebook)
        self.notebook.add(audio_frame, text="Audio")

        # Volume Slider
        volume_label = ttk.Label(audio_frame, text="Volume:")
        volume_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.volume_slider = ttk.Scale(audio_frame, from_=0, to=100, orient="horizontal")
        self.volume_slider.grid(row=0, column=1, padx=10, pady=5)

        # Tone Slider
        tone_label = ttk.Label(audio_frame, text="Tone:")
        tone_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.tone_slider = ttk.Scale(audio_frame, from_=0, to=100, orient="horizontal")
        self.tone_slider.grid(row=1, column=1, padx=10, pady=5)

        # Softness Slider
        softness_label = ttk.Label(audio_frame, text="Softness:")
        softness_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.softness_slider = ttk.Scale(audio_frame, from_=0, to=100, orient="horizontal")
        self.softness_slider.grid(row=2, column=1, padx=10, pady=5)

        # Noise Slider
        noise_label = ttk.Label(audio_frame, text="Noise:")
        noise_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.noise_slider = ttk.Scale(audio_frame, from_=0, to=100, orient="horizontal")
        self.noise_slider.grid(row=3, column=1, padx=10, pady=5)

        # QRN Slider
        qrn_label = ttk.Label(audio_frame, text="QRN:")
        qrn_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.qrn_slider = ttk.Scale(audio_frame, from_=0, to=100, orient="horizontal")
        self.qrn_slider.grid(row=4, column=1, padx=10, pady=5)

        # QRM Slider
        qrm_label = ttk.Label(audio_frame, text="QRM:")
        qrm_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.qrm_slider = ttk.Scale(audio_frame, from_=0, to=100, orient="horizontal")
        self.qrm_slider.grid(row=5, column=1, padx=10, pady=5)

        # Source tab (empty for now)
        source_frame = ttk.Frame(self.notebook)
        self.notebook.add(source_frame, text="Source")

        # Set protocol for closing the settings window
        self.window.protocol("WM_DELETE_WINDOW", self.on_settings_close)
        self.window.protocol("::tk::mac::Quit", self.on_settings_close)

        # Load settings if available
        self.load_settings()

    def update_windows(self):
        if self.mode_var.get() in ("SO2R", "2BSIQ"):
            self.window.protocol("WM_DELETE_WINDOW", self.on_settings_close)
        else:
            self.window.protocol("WM_DELETE_WINDOW", self.window.destroy)
            self.close_second_window()

    def on_settings_close(self):
        self.save_settings()
        print(f'On save: {self.mode_var.get()}')
        if self.mode_var.get() in ("SO2R", "2BSIQ"):
            self.create_second_window()
        self.window.destroy()

    def save_settings(self):
        with shelve.open('settings') as settings:
            settings['contest_selection'] = self.contest_entry.get()
            settings['mode'] = self.mode_var.get()
            settings['volume'] = self.volume_slider.get()
            settings['tone'] = self.tone_slider.get()
            settings['softness'] = self.softness_slider.get()
            settings['noise'] = self.noise_slider.get()
            settings['qrn'] = self.qrn_slider.get()
            settings['qrm'] = self.qrm_slider.get()

    def load_settings(self):
        with shelve.open('settings') as settings:
            self.contest_entry.insert(0, settings.get('contest_selection', ''))
            self.mode_var.set(settings.get('mode', 'SO1R'))
            self.volume_slider.set(settings.get('volume', 50))
            self.tone_slider.set(settings.get('tone', 50))
            self.softness_slider.set(settings.get('softness', 50))
            self.noise_slider.set(settings.get('noise', 50))
            self.qrn_slider.set(settings.get('qrn', 50))
            self.qrm_slider.set(settings.get('qrm', 50))
        print(f'On load: {self.mode_var.get()}')
        
