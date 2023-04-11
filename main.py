import os
import string
from urllib.error import URLError

import pytube
from pytube import YouTube

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showinfo, askyesno 

# Video download function
def download() -> None:
    """
    This is the main download function.
    The link, format, resolution and download path are gotten from the UI and are used here to specify the download requirements.
    """
    try:
        try:
            # Variable declarations
            url = YouTube(str(link.get()), on_progress_callback=progress)
            format = str(down_type.get())
            path = str(selected_directory.get())
            resolution = str(selected_quality.get())


            if format == 'Audio':   # The if-else statement decides if the program is required to download an audio or video file.
                audio = url.streams.get_audio_only('mp4')   # Gets the YouTube audio in '.mp3' format.
                name = f'{audio.title}'
            else:
                video = url.streams.filter(file_extension='mp4').get_by_resolution(resolution)  # Gets the YouTube video with the resolution specified in the GUI.
                name=f'{video.title}'

        except AttributeError:  # Runs if the video is a 'NoneType' object. This happens if the selected resolution or file extension can't be found.
            error('Selected resolution is unavailable. Try a different resolution.')
        confirm = audio if format == 'Audio' else video
        if query(f'File size: {round((confirm.filesize/1000000), 2)} MB. Proceed with download?'):
            new_name = []

            for x in name:  # Checks and removes punctuations from the video name.
                if x not in list(string.punctuation):
                    new_name.append(x)

            if not path:    # Runs if the download path is empty.
                error('Select a download location.')
            else:
                if format == 'Audio':
                    aud_name = ''.join(new_name).replace(' ', '_') + ' ' + '(' + format + ')' + '.mp3'
                    if not os.path.isfile(os.path.join(path, aud_name)):
                        # create_widgets(prog_label, prog_bar)
                        audio.download(filename=aud_name, output_path=path)
                        info('Download Completed.')
                        # destroy_widgets(prog_label, prog_bar)
                    else:
                        if query("This file already exists in the current directory. Do you want to download it anyway?"):
                            # create_widgets(prog_label, prog_bar)
                            audio.download(filename=new_file_name(aud_name, path), output_path=path)
                            info('Download Completed.')
                            # destroy_widgets(prog_label, prog_bar)
                else:
                    vid_name = ''.join(new_name).replace(' ', '_') + ' ' + '(' + resolution + ')' + '.mp4'
                    if not os.path.isfile(os.path.join(path, vid_name)):
                        # create_widgets(prog_label, prog_bar)
                        video.download(filename=vid_name, output_path=path)
                        info('Download Completed.')
                        # destroy_widgets(prog_label, prog_bar)
                    else:
                        if query("This file already exists in the current directory. Do you want to download it anyway?"):
                            # create_widgets(prog_label, prog_bar)
                            video.download(filename=new_file_name(vid_name, path), output_path=path)
                            info('Download Completed.')
                            # destroy_widgets(prog_label, prog_bar)

    except pytube.exceptions.VideoUnavailable:  # Runs if the link is not a YouTube link or the YT video is unavailable
        error('Link is invalid or the video is unavailable.')

    except pytube.exceptions.RegexMatchError:   # Runs if the entry is not a link
        error('Please enter a valid YouTube link.')

    except URLError:
        error('Failed to connect. Ensure you have a stable internet connection.')

def select_directory():
    """
    This function runs when the user clicks the 'Browse...' button on the UI.
    It returns the selected directory to the entry widget beside the 'Browse...' button.
    """
    select_dir = filedialog.askdirectory()
    selected_directory.insert(tk.END, select_dir)

def disable_buttons():
    """
    This function disables the radio buttons for the video quality when the format is on 'Audio'.
    It also re-enables the radio buttons when the format is on 'Video'.
    """
    if str(down_type.get()) == "Audio":
        for key in side_by_side_widgets:
            side_by_side_widgets[key]['state'] = 'disabled'
    else:
        for key in side_by_side_widgets:
            side_by_side_widgets[key]['state'] = 'enabled'

def query(question: str) -> bool:
    """
    This function confirms if the user wants to perform an action.
    """
    answer = askyesno(title='Alert', message=question)
    return answer

def error(errormessage: str) -> None:
    """
    This function displays an error message.
    """
    showerror(title='Error', message=errormessage)

def info(information: str) -> None:
    """
    This function displays information.
    """
    showinfo(title='Success', message=information)

def new_file_name(name: str, path: str) -> str:
    """
    This function appends a unique number to the file name if a file with the same name already exists.
    Why would someone want to download the same video again? I have no idea.
    This function exists to make sure your duplicate downloads are duplicates.
    """
    file_parts = os.path.splitext(name)
    base_name = file_parts[0]
    extension = file_parts[1]
    i = 1
    while True:
        n_name = f'{base_name}({i}){extension}'
        if not os.path.isfile(os.path.join(n_name, path)):
            return n_name
        i += 1

def progress(stream, chunk, bytes_remaining):
    percent = (100 * (stream.filesize - bytes_remaining)) / stream.filesize
    prog_label.config(text=f'{round(percent, 2)}%')
    prog_bar['value'] = percent
    root.update()

# def create_widgets(*args):
#     for b in args:
#         b.pack(padx=10, pady=2 ,fill=tk.X, anchor=tk.CENTER)

# def destroy_widgets(*args):
#     for a in args:
#         a.destroy()

root = tk.Tk()

# Window size
width = 500
height = 390

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

prog_bar = ttk.Progressbar(
        root,
        orient='horizontal',
        mode='determinate'
    )

prog_label = ttk.Label(
    root,
    text=''
)

version_no = ttk.Label(
    root,
    foreground='gray',
    text='Build 7',
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
prog_label.pack(padx=10, pady=2 ,fill=tk.X, anchor=tk.CENTER)
prog_bar.pack(padx=10, pady=2 ,fill=tk.X, anchor=tk.CENTER)
version_no.pack(anchor=tk.SE, side=tk.BOTTOM)

root.mainloop()

