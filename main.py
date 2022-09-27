import os
import pytube
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from pytube import YouTube

random_number = 0

def download():
    try:
        url = YouTube(str(link.get()))
        # print(url.streams.filter(file_extension='mp4'))
        if not str(selected_quality.get()):
            showinfo(title='Error', message='Please select a video quality')
        else:
            video = url.streams.filter(file_extension='mp4').get_by_resolution(str(selected_quality.get()))
            name=f'{video.title}({str(selected_quality.get())})'
            path='./'
            # if name in os.path.join(path, name):
            #     name = f'{video.title}({selected_quality.get()})({random_number + 1}).mp4'
            video.download(filename=f'{name}.mp4', output_path=path)
            showinfo(title='', message='Download Completed')
    except pytube.exceptions.VideoUnavailable:
        showinfo(title='Error', message='Link is invalid or the video is unavailable')
    except pytube.exceptions.RegexMatchError:
        showinfo(title='Error', message='Please enter a valid YouTube link')
    
        
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

version_no = ttk.Label(
    root,
    foreground='gray',
    text='Build 2',
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
version_no.pack(anchor=tk.SE, side=tk.BOTTOM)

root.mainloop()

