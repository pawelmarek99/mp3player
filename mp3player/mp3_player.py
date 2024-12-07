import os
import pygame
import tkinter as tk
from tkinter import ttk

# Globalne zmienne
current_index = 0
playlist = []
is_paused = False

def init_player():
    """Inicjalizacja odtwarzacza."""
    pygame.mixer.init()
    print("Player initialized.")

def load_songs_from_folder(folder_path):
    """Wczytanie listy plików MP3 z folderu."""
    global playlist
    if not os.path.exists(folder_path):
        print(f"Folder {folder_path} nie istnieje!")
        return []
    playlist = [f for f in os.listdir(folder_path) if f.endswith(".mp3")]
    if not playlist:
        print("Brak plików MP3 w folderze.")
    return playlist

def play_music(index):
    """Odtwarzanie muzyki na podstawie indeksu w playlist."""
    global current_index
    if index < 0 or index >= len(playlist):
        print("Indeks poza zakresem!")
        return
    current_index = index
    filepath = os.path.join(folder_path, playlist[current_index])
    try:
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
        print(f"Playing: {playlist[current_index]}")
        update_display()
    except pygame.error as e:
        print(f"Error playing file: {e}")

def stop_music():
    """Zatrzymanie muzyki."""
    pygame.mixer.music.stop()
    print("Music stopped.")

def pause_or_resume_music():
    """Pauza lub wznowienie muzyki."""
    global is_paused
    if is_paused:
        pygame.mixer.music.unpause()
        print("Music resumed.")
    else:
        pygame.mixer.music.pause()
        print("Music paused.")
    is_paused = not is_paused

def next_song():
    """Odtworzenie następnej piosenki."""
    global current_index
    if current_index + 1 < len(playlist):
        play_music(current_index + 1)

def prev_song():
    """Odtworzenie poprzedniej piosenki."""
    global current_index
    if current_index - 1 >= 0:
        play_music(current_index - 1)

def update_display():
    """Aktualizacja informacji o odtwarzanej i następnej piosence."""
    current_song_label.config(text=f"Obecnie odtwarzane: {playlist[current_index]}")
    next_song_label.config(text=f"Następna: {playlist[current_index + 1] if current_index + 1 < len(playlist) else '---'}")

def create_gui():
    """Tworzenie interfejsu użytkownika."""
    root = tk.Tk()
    root.title("MP3 Player")
    root.geometry("400x300")  # Rozmiar okna

    # Lista odtwarzania
    playlist_box = ttk.Treeview(root, columns=("Songs"), show="headings", height=8)
    playlist_box.heading("Songs", text="Lista piosenek")
    playlist_box.column("Songs", anchor="center")
    playlist_box.pack(pady=10)

    for song in playlist:
        playlist_box.insert("", "end", values=(song,))
    
    # Funkcjonalność kliknięcia na piosenkę
    def on_select(event):
        selected_item = playlist_box.focus()
        values = playlist_box.item(selected_item, 'values')
        if values:
            play_music(playlist.index(values[0]))

    playlist_box.bind("<<TreeviewSelect>>", on_select)

    # Informacje o aktualnej i następnej piosence
    global current_song_label, next_song_label
    current_song_label = tk.Label(root, text="Obecnie odtwarzane: ---", font=("Arial", 12))
    current_song_label.pack(pady=5)

    next_song_label = tk.Label(root, text="Następna: ---", font=("Arial", 10), fg="gray")
    next_song_label.pack(pady=5)

    # Przycisk Pauzy/Wznowienia
    pause_button = tk.Button(root, text="Pauza/Wznów", command=pause_or_resume_music)
    pause_button.pack(pady=5)

    # Przycisk Stop
    stop_button = tk.Button(root, text="Stop", command=stop_music)
    stop_button.pack(pady=5)

    # Przycisk Następna
    next_button = tk.Button(root, text="Następna", command=next_song)
    next_button.pack(side="left", padx=10)

    # Przycisk Poprzednia
    prev_button = tk.Button(root, text="Poprzednia", command=prev_song)
    prev_button.pack(side="right", padx=10)

    root.protocol("WM_DELETE_WINDOW", lambda: (stop_music(), root.destroy()))  # Zatrzymaj muzykę i zamknij okno

    root.mainloop()

if __name__ == "__main__":
    # Ścieżka do folderu z muzyką
    folder_path = r"C:\Users\pawci\Desktop\mp3player\music"

    # Inicjalizacja
    init_player()

    # Wczytanie piosenek
    load_songs_from_folder(folder_path)

    # Tworzenie GUI
    create_gui()
