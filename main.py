import os
import string

import pytube
from pytube import YouTube

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo

random_number = 0

# Video download function
def download():
    try:
        url = YouTube(str(link.get()))
        
        # Runs if the selected format is 'Audio'
        if str(down_type.get()) == 'Audio':
            # ---
            # Work on this tonight
            audio = url.streams.get_audio_only('mp4')
            name = f'{audio.title}'
            new_name = []
            # Checks and removes punctuations from the video name
            for x in name:
                if x not in list(string.punctuation):
                    new_name.append(x)
            # Download Path
            # Gotten from the directory entry in the UI
            path=str(selected_directory.get())
            # Runs if the download path is empty
            if not path:
                showerror(title='Error', message='Select a download location')
            else:
                audio.download(filename=''.join(new_name).replace(' ', '_') + ' ' + '(' + str(down_type.get()) + ')' + '.mp3', output_path=path)
                showinfo(title='Success', message='Download Completed')

        # Runs if the user has not selected a format
        elif not str(down_type.get()):
            showinfo(title='Error', message='Please select a download format')

        # Runs if the selected format is 'Video'
        else:
            if not str(selected_quality.get()):
                showinfo(title='Error', message='Please select a video quality')
            else:
                try:
                    # Gets the YouTube video with the resolution specified in the GUI
                    video = url.streams.filter(file_extension='mp4').get_by_resolution(str(selected_quality.get()))
                    name=f'{video.title}'
                # Runs if the video is a 'NoneType' object
                # This happens if the selected resolution or file extension can't be found
                except AttributeError:
                    showinfo(title='Error', message='Selected resolution is unavailable. Try a different resolution.')
                new_name = []
                # Checks and removes punctuations from the video name
                for x in name:
                    if x not in list(string.punctuation):
                        new_name.append(x)
                # Download Path
                # Gotten from the directory entry in the UI
                path=str(selected_directory.get())
                # Runs if the download path is empty
                if not path:
                    showerror(title='Error', message='Select a download location')
                else:
                    # if name in os.path.join(path, name):
                    #     name = f'{video.title}({selected_quality.get()})({random_number + 1}).mp4'
                    # try:
                    # url.register_on_progress_callback(progress)
                    video.download(filename=''.join(new_name).replace(' ', '_') + ' ' + '(' + str(selected_quality.get()) + ')' + '.mp4', output_path=path)
                    showinfo(title='Success', message='Download Completed')
    # Runs if the link is not a YouTube link or the YT video is unavailable
    except pytube.exceptions.VideoUnavailable:
        showerror(title='Error', message='Link is invalid or the video is unavailable')
    # Runs if the entry is not a link
    except pytube.exceptions.RegexMatchError:
        showerror(title='Error', message='Please enter a valid YouTube link')

def select_directory():
    select_dir = filedialog.askdirectory()
    selected_directory.insert(tk.END, select_dir)

def disable_buttons():
    if str(down_type.get()) == "Audio":
        for key in side_by_side_widgets:
            side_by_side_widgets[key]['state'] = 'disabled'
    else:
        for key in side_by_side_widgets:
            side_by_side_widgets[key]['state'] = 'enabled'

# Function for the progress bar
# P.S.: I don't know how to do this yet
# def progress(stream, chunk, bytes_remaining):
#     max_value = stream.filesize
#     bytes_downloaded = max_value - bytes_remaining
#     pb['value'] = bytes_downloaded
#     pb['maximum'] = max_value
#     if bytes_downloaded < max_value:
#         pb.after(100, progress())

root = tk.Tk()

# Window size
width = 500
height = 370

# Screen Size
scr_width = root.winfo_screenwidth()
scr_height = root.winfo_screenheight()

# Center Positions
center_x = int(scr_width/2 - width/2)
center_y = int(scr_height/2 - width/2)

root.geometry(f'{width}x{height}+{center_x}+{center_y}')
root.resizable(False, False)

root.title('VideoTube')

qualities = ttk.LabelFrame(root, text='Video Quality')
mode = ttk.LabelFrame(root, text='Download Format')
download_dir = ttk.Frame(root)

label = ttk.Label(
    root,
    text='A Simple YouTube Video Downloader',
    font=('Helvetica', 12)
)

link_label = ttk.Label(
    root,
    text='Enter your link here',
    font=('Helvetica bold', 12),
)

link = tk.StringVar()
link_entry = ttk.Entry(
    root,
    textvariable=link,
)

directory = tk.StringVar()

directory_label = ttk.Label(
    root,
    text='Download Location',
    font=('Helvetica bold', 12)
)

selected_directory = ttk.Entry(
    download_dir,
    textvariable=directory
)
selected_directory.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)

dir_button = ttk.Button(
    download_dir,
    text='Browse...',
    command=select_directory
).pack(side=tk.RIGHT, padx=10)

download_icon = tk.PhotoImage(file="./assets/download icon.png")
download_button = ttk.Button(
    root,
    image = download_icon,
    text='Download',
    # font=('Helvetica', 12),
    # bg='blue',
    compound=tk.LEFT,
    command=download
)

side_by_side_widgets = dict()
formats = dict()

# More qualities to be added later
# Probably
selected_quality = tk.StringVar()
video_qualities = ('144p', '240p', '360p', '480p', '720p', '1080p')
down_type = tk.StringVar()
types = ('Video', 'Audio')

pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
)

version_no = ttk.Label(
    root,
    foreground='gray',
    text='Build 5',
)

label.pack(anchor=tk.N, pady=10)
link_label.pack()
link_entry.pack(padx=10, pady=5, fill=tk.X, anchor=tk.N)
link_entry.focus()
directory_label.pack()
download_dir.pack(pady=5, fill=tk.X)
for type in types:
    formats[type] = ttk.Radiobutton(
        mode,
        text = type,
        value = type,
        variable = down_type,
        command = disable_buttons
    )
    formats[type].pack(side=tk.LEFT, expand=True, padx=20, pady=5)

for quality in video_qualities:
    side_by_side_widgets[quality] = ttk.Radiobutton(
        qualities,
        text = quality,
        value = quality,
        variable = selected_quality,
        command = disable_buttons
    )
    side_by_side_widgets[quality].pack(side=tk.LEFT, expand=True, padx=5, pady=5)
mode.pack(padx=10, pady=5, fill=tk.X)
qualities.pack(padx=10, pady=5, fill=tk.X)
download_button.pack()
pb.pack(padx=10, pady=5 ,fill=tk.X)
version_no.pack(anchor=tk.SE, side=tk.BOTTOM)

root.mainloop()

