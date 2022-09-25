import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from pytube import YouTube

def download():
    url = YouTube(str(link.get()))
    video = url.streams.filter(file_extension='mp4').get_by_resolution('360p')
    video.download(filename=f'{video.title}.mp4', output_path='./')
    showinfo(title='', message='Download Completed')
        
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
    width=72
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

label.pack()
link_label.pack(pady=25)
link_entry.pack()
link_entry.focus()
download_button.pack(pady=10)

root.mainloop()

