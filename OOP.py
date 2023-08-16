import os
import re
import string
import tkinter as tk
from tkinter import filedialog, ttk
from tkinter.messagebox import showerror, showinfo, askyesno
from threading import Thread

import pytube
from pytube import YouTube

class Downloader:

    def __init__(self, root, url, file_format, file_quality, download_path):

        # Get file info

        self.root = root
        self.url = YouTube(url, on_progress_callback=self.progress)
        self.file_format = file_format
        self.file_quality = file_quality
        self.download_path = download_path

        # Maybe put this in a separate function?
        self.stream = self.url.streams.get_audio_only('mp4') if \
            file_format == 'Audio' else \
            self.url.streams.filter(file_extension='mp4').get_by_resolution(self.file_quality)
        self.file_name = self.create_file_name()

    def create_file_name(self):

        name = []
        for x in self.stream.title:
            if x not in list(string.punctuation):
                name.append(x)
            

        if self.file_format == 'Video':
            final_name = ''.join(name).replace(' ', '_') + ' ' + '(' + self.file_quality + ')' + '.mp4'
        else:
            final_name = ''.join(name).replace(' ', '_') + ' ' + '(' + self.file_format + ')' + '.mp3'
        
        return final_name


    def download(self):

        # video = self.url.streams.filter(file_extension='mp4').get_by_resolution(self.file_quality)
        # Name creation will have to occur in a separate function

        self.stream.download(filename=self.file_name, output_path=self.download_path)

    def check_size(self):

        return round((self.stream.filesize/1048576), 2)

    def progress(self, stream, chunk, bytes_remaining):
        percent = (100 * (stream.filesize - bytes_remaining))/stream.filesize
        self.status_label.configure(text=f'{round(percent, 2)}% ({round(((stream.filesize/1048576) - (bytes_remaining/1048576)), 2)} MB/{round((stream.filesize/1048576), 2)} MB)')
        self.prog_bar['value'] = percent
        self.prog_bar.update()

    def render_widgets(self):
        self.status_label = tk.Label(
            self.root,
            text='---'
        )
        self.status_label.grid(
            row=7,
            column=0,
            columnspan=6,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            pady=(0, 6)
        )

        self.prog_bar = ttk.Progressbar(
            self.root,
            orient=tk.HORIZONTAL,
            mode='determinate'
        )
        self.prog_bar.grid(
            row=8,
            column=0,
            columnspan=6,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            pady=(0, 10)
        )

    def remove_widgets(self):
        self.status_label.grid_forget()
        self.prog_bar.grid_forget()

    def abort(self):

        os.remove(self.final_name)


class GUI(tk.Tk):

    def __init__(self):

        super().__init__()

        self.qualities = ('144p','240p','360p','480p','720p','1080p',)

        # If defaults have been created
        if os.path.isfile('defaults'):
            self._path = tk.StringVar()
            self._quality = tk.StringVar()

            with open('defaults') as d:
                def_values = d.readlines()
            for val in def_values:

                # Check if default value is a valid path
                if os.path.exists(val[:-1]):
                    self._path = tk.StringVar(value=val[:-1])

                # Check if default value is a valid resolution
                elif val[:-1] in self.qualities:
                    self._quality = tk.StringVar(value=val[:-1])

                # This handles defaults that were not chosen
                elif val == '\n':
                    continue

                # Error displays when value is invalid
                else:
                    self.error(
                        'One or more default values were invalid. Please use valid default values'
                    )
        # If defaults have not been created
        else:
            self._path = tk.StringVar()
            self._quality = tk.StringVar()

        self.media_stream = None
        self._link = tk.StringVar()
        self._format = tk.StringVar()
        
        self.cancel = False

        self.title('PyTube Program')
        self.resizable(0, 0)
        
        self.menu_bar = tk.Menu(self)

        self.file_menu = tk.Menu(
            self.menu_bar,
            tearoff=0
        )
        self.about_menu = tk.Menu(
            self.menu_bar,
            tearoff=0
        )

        self.file_menu.add_command(
            label='Set Defaults',
            command=self.select_defaults
        )
        self.file_menu.add_command(
            label='Exit',
            command=self.destroy
        )

        self.about_menu.add_command(
            label='How to Use',
            command=self.show_help
        )
        self.about_menu.add_command(
            label='About',
            command=self.show_about
        )
        
        self.menu_bar.add_cascade(
            label='File',
            menu=self.file_menu
        )
        self.menu_bar.add_cascade(
            label='Info',
            menu=self.about_menu
        )

        self.configure(menu=self.menu_bar)

        self.link_entry_label = tk.Label(
            self, 
            text='Enter YouTube Link Below'
        )
        self.link_entry_label.grid(
            row=0,
            column=0,
            columnspan=6,
            pady=(10, 6),
            padx=10,
        )

        self.link_entry = tk.Entry(
            self,
            textvariable=self._link,
            relief=tk.RIDGE,
            bd=5,
            exportselection=0
        )
        self.link_entry.grid(
            row=1,
            column=0,
            columnspan=6,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            ipady=10,
            pady=(0, 6)
        )
        self.link_entry.focus()

        self.path_select_label = tk.Label(
            self,
            text='Enter Download Path Here or Use the \'BROWSE...\' button'
        )
        self.path_select_label.grid(
            row=2,
            column=0,
            columnspan=6,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            # ipady=10,
            pady=(0, 6)
        )

        self.path_entry = tk.Entry(
            self,
            textvariable=self._path,
            relief=tk.RIDGE,
            bd=5,
            exportselection=0
        )
        self.path_entry.grid(
            row=3,
            column=0,
            columnspan=4,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            ipady=10,
            pady=(0, 6)
        )

        self.browse = tk.Button(
            self,
            text='BROWSE...',
            command=self.path_select,
            relief=tk.GROOVE,
            bg='#3498DB',
            bd=3
        )
        self.browse.grid(
            row=3,
            column=4,
            columnspan=2,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            ipady=10,
            pady=(0, 6)
        )

        self.format_frame = tk.LabelFrame(
            self,
            text='Format',
            # relief=tk.RIDGE,
            # bd=5
            # bg='#482315'
        )

        self.format_1 = tk.Radiobutton(
            self.format_frame,
            text='Video',
            value='Video',
            variable=self._format,
            command=self.disable_qualities
        )
        self.format_1.pack(
            side=tk.LEFT,
            expand=True,
            padx=5,
            ipady=10,
        )

        self.format_2 = tk.Radiobutton(
            self.format_frame,
            text='Audio',
            value='Audio',
            variable=self._format,
            command=self.disable_qualities,
            # bg='#6546b5'
        )
        self.format_2.pack(
            side=tk.LEFT,
            expand=True,
            padx=5,
            ipady=10,
        )

        self.format_frame.grid(
            row=4,
            column=0,
            columnspan=6,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            pady=(0, 6)
        )

        self.quality_frame = tk.LabelFrame(
            self,
            text='Quality',
            # relief=tk.RIDGE,
            # bd=5
        )

        self.available_qualities = dict()
        for q in self.qualities:
            self.available_qualities[q] = tk.Radiobutton(
                self.quality_frame,
                text=q,
                value=q,
                variable=self._quality,
            )
            self.available_qualities[q].grid(
                row=0,
                column=self.qualities.index(q),
                ipady=10,
                # columnspan=1,
            )
        
        self.quality_frame.grid(
            row=5,
            column=0,
            columnspan=6,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            pady=(0, 6)
        )

        self.download_icon = tk.PhotoImage(file="./assets/download icon.png")
        self.download_button = tk.Button(
            self,
            image=self.download_icon,
            text='Download',
            compound=tk.LEFT,
            relief=tk.GROOVE,
            # bg='#4CAF50',
            bd=3,
            command=self.download_check,
            background='#4CAF50'
        )
        self.download_button.grid(
            row=6,
            column=0,
            columnspan=3,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            ipady=10,
            pady=(0, 10)
        )

        self.cancel_button = tk.Button(
            self,
            text='Cancel (NOT WORKING)',
            compound=tk.LEFT,
            relief=tk.GROOVE,
            bg='#aaaaaa',
            fg='#ffffff',
            state=tk.DISABLED,
            bd=3
        )
        self.cancel_button.grid(
            row=6,
            column=3,
            columnspan=3,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            ipady=10,
            pady=(0, 10)
        )

        # self.build_no = tk.Label(
        #     self,
        #     text='Build 10',
        #     fg='gray',
        #     anchor=tk.E
        # )
        # self.build_no.grid(
        #     row=7,
        #     column=5,
        #     padx=10,
        #     pady=(0, 10),
        #     sticky=tk.N + tk.S + tk.E + tk.W
        # )

    def create_stream(self):

        self.media_stream = Downloader(
            self, self.link, self.format, self.quality, self.path
        )

    def download_check(self):

        self.link = self._link.get()
        self.format = self._format.get()
        self.quality = self._quality.get()
        self.path = self._path.get()

        if os.path.exists(self.path):
            pass
        else:
            self.info('This path is invalid. Select a valid path.')
            return

        link_pattern = r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/'
        if not re.match(link_pattern, self.link):
            self.info('This is an invalid YouTube link. Enter a valid link.')
            return
        elif not self.format:
            self.info('Select a file format.')
            return
        elif not self.quality:
            self.info('Select a video quality.')
            return

        try:
            self.create_stream()
        except Exception as e:
            self.error(e)
            return

        if self.query(f'File size: {self.media_stream.check_size()} MB'):
            self.media_stream.render_widgets()
            self.download_callback()

    def download_callback(self):
        thr = Thread(target=self.download_execute)
        thr.start()
        

    def download_execute(self):
        
        self.disable_controls()

        try:
            if not os.path.isfile(os.path.join(self.path, self.media_stream.file_name)):
                self.media_stream.download()
                self.info('Download Complete.')

            else:
                if self.query('File Exists. Download Anyway?'):
                    aaa = self.media_stream.file_name
                    self.media_stream.file_name = self.duplicate_name(aaa, self.path) 
                    self.media_stream.download()
                    self.info('Download Complete.')
                else:
                    self.info('Download Cancelled.')
        except Exception as e:
            self.error(e)
        
        self.media_stream.remove_widgets()
        self.enable_controls()
        self.media_stream = None

    def show_about(self):
        self.info(
            '''A YouTube video downloader made by SidKay.\n
There are still a few bugs in the program so
Everything may not work as intended.
Please bear with me while I fix them (or not).\n
Plus I may decide to add a few other features as time passes.'''
        )

    def show_help(self):
        self.info(
            """__HOW TO USE__\n
1. Enter the YouTube video link of the media that you want to download.\n
2. Enter the download path of the media.\n
3. Choose if you want it in an audio or video format.\n
4. Select the video quality (Only applies for video downloads).\n
NOTE: You can use 'Select Defaults' to reduce the hassle of selecting a download path or quality everytime.
            """
        )

    def disable_qualities(self):
        
        if self._format.get() == 'Audio':
            for q in self.available_qualities:
                self.available_qualities[q].configure(state=tk.DISABLED)
            return
        
        else:
            for q in self.available_qualities:
                self.available_qualities[q].configure(state=tk.NORMAL)
            return

    def disable_controls(self):

        self.link_entry.configure(state=tk.DISABLED)
        self.path_entry.configure(state=tk.DISABLED)
        self.browse.configure(state=tk.DISABLED, bg='#aaaaaa')
        self.format_1.configure(state=tk.DISABLED)
        self.format_2.configure(state=tk.DISABLED)
        for q in self.available_qualities:
            self.available_qualities[q].configure(state=tk.DISABLED)
        self.download_button.configure(state=tk.DISABLED, background='#aaaaaa')
        self.cancel_button.configure(state=tk.NORMAL, bg='#e74C3C')

    def enable_controls(self):

        self.link_entry.configure(state=tk.NORMAL)
        self.path_entry.configure(state=tk.NORMAL)
        self.browse.configure(state=tk.NORMAL, bg='#3498DB')
        self.format_1.configure(state=tk.NORMAL)
        self.format_2.configure(state=tk.NORMAL)
        for q in self.available_qualities:
            self.available_qualities[q].configure(state=tk.NORMAL)
        self.download_button.configure(state=tk.NORMAL, background='#4CAF50')
        self.cancel_button.configure(state=tk.DISABLED, bg='#aaaaaa')

    def path_select(self):
        select_path = filedialog.askdirectory()
        self.path_entry.delete(0, tk.END)
        self.path_entry.insert(tk.END, select_path)
        return

    def duplicate_name(self, file_name, file_path):
        file_parts = os.path.splitext(file_name)
        base_name = file_parts[0]
        extension = file_parts[1]
        i = 1
        while True:
            new_name = f'{base_name}({i}){extension}'
            if not os.path.isfile(os.path.join(new_name, file_path)):
                return new_name
            i += 1
    
    def select_defaults(self):

        self.def_path = tk.StringVar()
        self.def_quality = tk.StringVar()

        self.sub_window = tk.Toplevel(self)
        self.resizable(0, 0)

        self.sub_window.attributes('-toolwindow', True)

        self.sub_window.title('Set Default Options')

        self.heading = tk.Label(
            self.sub_window,
            text='Use this to set default download parameters'
        )
        self.heading.grid(
            row=0,
            column=0,
            columnspan=6,
            pady=(10, 6),
            padx=10,
        )

        self.sep = ttk.Separator(
            self.sub_window, orient=tk.HORIZONTAL
        )
        self.sep.grid(
            row=1,
            column=0,
            columnspan=6,
            padx=10,
            pady=(0, 6)
        )

        self.def_path_select_label = tk.Label(
            self.sub_window,
            text='Enter Download Path Here or Use the \'BROWSE...\' button'
        )
        self.def_path_select_label.grid(
            row=2,
            column=0,
            columnspan=6,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            pady=(0, 6)
        )

        self.def_path_entry = ttk.Entry(
            self.sub_window,
            textvariable=self.def_path,
            exportselection=0
        )
        self.def_path_entry.grid(
            row=3,
            column=0,
            columnspan=4,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            pady=(0, 6)
        )
        self.def_path_entry.focus()

        self.def_browse = ttk.Button(
            self.sub_window,
            text='BROWSE...',
            command=self.def_path_select,
        )
        self.def_browse.grid(
            row=3,
            column=4,
            columnspan=2,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            pady=(0, 6)
        )

        self.def_quality_frame = tk.LabelFrame(
            self.sub_window,
            text='Quality',
        )

        self.def_available_qualities = dict()
        for q in self.qualities:
            self.def_available_qualities[q] = ttk.Radiobutton(
                self.def_quality_frame,
                text=q,
                value=q,
                variable=self.def_quality,
            )
            self.def_available_qualities[q].grid(
                row=0,
                column=self.qualities.index(q),
                # columnspan=1,
            )
        
        self.def_quality_frame.grid(
            row=4,
            column=0,
            columnspan=6,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            pady=(0, 6)
        )

        self.def_select = ttk.Button(
            self.sub_window,
            text='Save',
            command=self.create_defaults
        )
        self.def_select.grid(
            row=5,
            column=2,
            columnspan=2,
            padx=10,
            sticky=tk.E + tk.W + tk.N + tk.S,
            pady=(0, 10)
        )

        self.sub_window.grab_set()

    def def_path_select(self):
        self.sub_window.grab_set()
        select_path = filedialog.askdirectory()
        self.def_path_entry.delete(0, tk.END)
        self.def_path_entry.insert(tk.END, select_path)
        return

    def create_defaults(self):
        with open('defaults', 'w') as f:
            print(self.def_path.get(), file=f)
            print(self.def_quality.get(), file=f)
        self.info(
            """
Defaults Saved.
This will apply when you restart the application.
            """
        )
        self.sub_window.destroy

    def info(self, message):
        showinfo('Info', message)

    def error(self, message):
        showerror('Error', message)

    def query(self, message):
        askyesno('Query', message)

if __name__ == '__main__':
    main_window = GUI()
    main_window.mainloop()
