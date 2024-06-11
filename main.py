import tkinter as tk
from tkinter import filedialog
import pygame
from pygame import mixer
import threading
import time


def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
    if file_path:
        mixer.music.load(file_path)
        mixer.music.play()
        song_length = mixer.Sound(file_path).get_length()
        progress_bar.config(to=song_length)
        threading.Thread(target=update_progress_bar, args=(song_length,)).start()


def update_progress_bar(song_length):
    while mixer.music.get_busy():
        if not progress_dragging:
            current_time = mixer.music.get_pos() / 1000  
            progress_var.set(current_time)
        time.sleep(1)
    progress_var.set(0)


def stop_audio():
    mixer.music.stop()
    progress_var.set(0)


def set_music_pos(event):
    if progress_dragging:
        mixer.music.play(start=progress_var.get())


def on_progress_press(event):
    global progress_dragging
    progress_dragging = True
    mixer.music.pause()

def on_progress_release(event):
    global progress_dragging
    progress_dragging = False
    set_music_pos(event)


mixer.init()


root = tk.Tk()
root.title("AudioPyPlayer 1.0a")


progress_dragging = False


play_button = tk.Button(root, text="Reproduzir", command=open_file)
play_button.pack(pady=10)


stop_button = tk.Button(root, text="Parar", command=stop_audio)
stop_button.pack(pady=10)


progress_var = tk.DoubleVar()
progress_bar = tk.Scale(root, variable=progress_var, orient="horizontal", length=300, from_=0, to=100)
progress_bar.pack(pady=10)
progress_bar.bind("<Button-1>", on_progress_press)
progress_bar.bind("<ButtonRelease-1>", on_progress_release)
progress_bar.bind("<B1-Motion>", set_music_pos)


root.mainloop()
