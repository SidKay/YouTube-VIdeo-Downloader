# I use this to test code without altering the main.py file
import tkinter as tk


def on_rb_press():
    sum_label['text'] += var.get()
    if sum_label['text'] >= 30:
        for key in radiobuttons:
            radiobuttons[key]['state'] = 'disabled'


root = tk.Tk()
sum_label = tk.Label(root, text=0)
sum_label.pack()
radiobuttons = dict()
var = tk.IntVar(value=1)
for i in range(1, 6):
    radiobuttons[i] = tk.Radiobutton(root, text=i, variable=var,
                                                value=i, command=on_rb_press)
    radiobuttons[i].pack()
tk.mainloop()