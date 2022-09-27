# I use this to test code without altering the main.py file

try:                        # In order to be able to import tkinter for
    import tkinter as tk    # either in python 2 or in python 3
except ImportError:
    import Tkinter as tk


def main():
    root = tk.Tk()
    side_by_side_widgets = dict()
    the_widget_beneath = tk.Entry(root)
    frame = tk.Frame(root)
    for name in {"side b", "y side"}:
        side_by_side_widgets[name] = tk.Label(frame, text=name)
        side_by_side_widgets[name].pack(side='left', expand=True)
    frame.pack(fill='x')
    the_widget_beneath.pack()
    root.mainloop()


if __name__ == '__main__':
    main()