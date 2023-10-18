from tkinter import filedialog
from tkinter import *
import pygame
import os

root = Tk()
root.title('Music Player')
root.geometry("500x300")

pygame.init()

menubar = Menu(root)
root.config(menu=menubar)

songs= []
current_song = ""
paused = False

def load_music():
    global current_song
    music_directory = filedialog.askdirectory()
    
    # Change the working directory to the music directory
    os.chdir(music_directory)
    
    for song in os.listdir(music_directory):
        name, ext = os.path.splitext(song)
        if ext == '.mp3':
            songs.append(song)

    for song in songs:
        songlist.insert('end', song)

    songlist.selection_set(0)
    current_song = songs[songlist.curselection()[0]]


def play_music():
    global current_song, paused

    get_music_info()
    if not paused:
        pygame.mixer.music.load(current_song)
        pygame.mixer.music.play()
    else:
        pygame.mixer.music.unpause()
        paused = False

def pause_music():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_music():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) + 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def prev_music():
    global current_song, paused

    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(current_song) - 1)
        current_song = songs[songlist.curselection()[0]]
        play_music()
    except:
        pass

def get_music_info():
    # length = pygame.mixer.music.get_pos()
    position_ms = pygame.mixer.music.get_pos()  # Get position in milliseconds
    position_sec = position_ms / 1000  # Convert to seconds
    # print(f"Music Length: {length} seconds")
    print(f"Current Playback Position: {position_sec} seconds")

organise_menu = Menu(menubar, tearoff=False)
organise_menu.add_command(label='Select Folder', command=load_music)
menubar.add_cascade(label='Organise', menu=organise_menu)

songlist = Listbox(root, bg='black', fg='white', width=100, height=15)
songlist.pack()

play_btn_image = PhotoImage(file='img/play.png')
pause_btn_image = PhotoImage(file='img/pause.png')
next_btn_image = PhotoImage(file='img/next.png')
prev_btn_image = PhotoImage(file='img/previous.png')

control_frame = Frame(root)
control_frame.pack()

play_btn = Button(control_frame, image=play_btn_image, borderwidth=0, command=play_music)
pause_btn = Button(control_frame, image=pause_btn_image, borderwidth=0, command=pause_music)
next_btn = Button(control_frame, image=next_btn_image, borderwidth=0, command=next_music)
prev_btn = Button(control_frame, image=prev_btn_image, borderwidth=0, command=prev_music)

play_btn.grid(row=0, column=1, padx=7, pady=10)
pause_btn.grid(row=0, column=2, padx=7, pady=10)
next_btn.grid(row=0, column=3, padx=7, pady=10)
prev_btn.grid(row=0, column=0, padx=7, pady=10)

root.mainloop()