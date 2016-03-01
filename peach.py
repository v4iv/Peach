from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import asksaveasfile
from tkinter.filedialog import askopenfile


# Peach Text Editor

class Editor(Text):
    def __init__(self, master, **kw):
        Text.__init__(self, master, **kw)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)

    def copy(self, event=None):
        try:
            self.clipboard_clear()
            text = self.get("sel.first", "sel.last")
            self.clipboard_append(text)
        except:
            pass

    def cut(self, event):
        try:
            self.copy()
            self.delete("sel.first", "sel.last")
        except:
            pass

    def paste(self, event):
        try:
            text = self.selection_get(selection='CLIPBOARD')
            self.insert('insert', text)
        except:
            pass


filename = None


def new_file():
    global filename
    filename = 'untitled'
    text_area.delete(0.0, END)


def save_file():
    global filename
    data = text_area.get(0.0, END)
    if filename != 'untitled':
        file = open(filename, 'w')
        file.write(data)
        file.close()
    else:
        file = asksaveasfile(defaultextension='.txt')
        data = text_area.get(0.0, END)
        try:
            file.write(data.rstrip())
        except:
            tkinter.messagebox.showinfo("Oops!", "Unable To Save File!")


def save_as():
    file = asksaveasfile(defaultextension='.txt')
    data = text_area.get(0.0, END)
    try:
        file.write(data.rstrip())
    except:
        tkinter.messagebox.showinfo("Cancel", "File Not Saved!")


def open_file():
    global filename
    file = askopenfile(parent=root, title='Open File')
    filename = file.name
    data = file.read()
    text_area.delete(0.0, END)
    text_area.insert(0.0, data)
    file.close()


def exit_peach():
    global filename
    if filename == 'untitled':
        answer = tkinter.messagebox.askquestion("Unsaved Changes", "Do you want to exit without saving the file?")
        if answer == 'yes':
            root.quit()
        else:
            save_file()
    else:
        root.quit()


root = Tk()
root.title("Peach")
root.minsize(width=700, height=450)

# ******** Menu Bar **********
menu = Menu(root)
root.config(menu=menu)

file_menu = Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_peach)

# ******** Editor *********
text_area = Editor(root)
text_area.pack(expand=True, fill='both')

new_file()

# ******** Status Bar **********
status = Label(root, text=filename, bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

root.mainloop()
