import os
import string
import pytube
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from pytube import YouTube

random_number = 0

# Video download function
def download():
    try:
        url = YouTube(str(link.get()))
        # video = url.streams.filter(file_extension='mp4')
        # print(video)
        # print(url.streams.filter(file_extension='mp4'))
        # Runs if the user has not selected a video quality
        if not str(selected_quality.get()):
            showinfo(title='Error', message='Please select a video quality')
        else:
            try:
                # Gets the YouTube video with the resolution specified in the GUI
                video = url.streams.filter(file_extension='mp4').get_by_resolution(str(selected_quality.get()))
                # print(video)
                # pass
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
            path='./'
            # if name in os.path.join(path, name):
            #     name = f'{video.title}({selected_quality.get()})({random_number + 1}).mp4'
            # try:
            # url.register_on_progress_callback(progress)
            video.download(filename=''.join(new_name).replace(' ', '_') + ' ' + '(' + str(selected_quality.get()) + ')' + '.mp4', output_path=path)
            showinfo(title='Success', message='Download Completed')
    # Runs if the link is not a YouTube link or the YT video is unavailable
    except pytube.exceptions.VideoUnavailable:
        showinfo(title='Error', message='Link is invalid or the video is unavailable')
    # Runs if the entry is not a link
    except pytube.exceptions.RegexMatchError:
        showinfo(title='Error', message='Please enter a valid YouTube link')

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
height = 300

# Screen Size
scr_width = root.winfo_screenwidth()
scr_height = root.winfo_screenheight()

# Center Positions
center_x = int(scr_width/2 - width/2)
center_y = int(scr_height/2 - width/2)

root.geometry(f'{width}x{height}+{center_x}+{center_y}')
root.resizable(False, False)
# for x in range(1, 11):
#     root.attributes('-alpha', x/10)
root.title('VideoTube')
# print(f"{root.winfo_screenwidth()} {root.winfo_screenheight()}")

qualities = ttk.LabelFrame(root, text='Video Quality')

label = ttk.Label(
    root,
    text='A Simple YouTube Video Downloader',
    font=('Helvetica', 12)
)

link_label = ttk.Label(
    root,
    text='Enter your link here',
    font=('Helvetica bold' , 12),
)

link = tk.StringVar()
link_entry = ttk.Entry(
    root,
    textvariable=link,
    # width=72
)

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

# quality_label = tk.Label(
#     root,
#     text = 'Quality:',
#     bg='blue'
# )

side_by_side_widgets = dict()

# More qualities to be added later
selected_quality = tk.StringVar()
video_qualities = ('144p', '240p', '360p', '480p', '720p', '1080p')

pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='determinate',
)

version_no = ttk.Label(
    root,
    foreground='gray',
    text='Build 3',
)

label.pack(anchor=tk.N, pady=10)
link_label.pack()
link_entry.pack(padx=10, pady=5, fill=tk.X, anchor=tk.N)
link_entry.focus()
for quality in video_qualities:
    side_by_side_widgets[quality] = ttk.Radiobutton(
        qualities,
        text = quality,
        value = quality,
        variable = selected_quality,
    )
    side_by_side_widgets[quality].pack(side=tk.LEFT, expand=True, padx=5, pady=5)
qualities.pack(padx=10, pady=5, fill=tk.X)
download_button.pack()
pb.pack(padx=10, pady=5 ,fill=tk.X)
version_no.pack(anchor=tk.SE, side=tk.BOTTOM)

root.mainloop()

