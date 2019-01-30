try:
    import tkinter as tk
    from encryptions import *
    import random
    from datetime import datetime
    from PIL import Image, ImageTk
except:
    import Tkinter as tk
    from encryptions import *
    import random
    from datetime import datetime
    from PIL import Image, ImageTk

class AccEntry:
    def __init__(self, keys, master, **kwargs):
        self.master = master
        self.title = kwargs.get("title","None")
        self.userentry = tk.StringVar()
        self.passentry = tk.StringVar()
        self.keys = keys
        self.side = kwargs.get("side", None)

        self.titlelabel = tk.Label(self.master, text=self.title)
        self.userlabel = tk.Label(self.master, textvariable = self.userentry)
        self.passlabel = tk.Label(self.master, textvariable = self.passentry)

        self.userentry.set(kwargs.get("user", "none"))
        self.passentry.set(kwargs.get("pwd", "none"))

    def encrypt(self):
        keys = self.keys[0]
        encrypt_pat = self.keys[1]
        for index in range(len(keys)):
            self.userentry.set(encrypt_pat[index](self.userentry.get(),keys[index]))
            self.passentry.set(encrypt_pat[index](self.passentry.get(),keys[index]))

    def decrypt(self):
        keys = [key for key in self.keys[0][::-1]]
        decrypt_pat = [pat for pat in self.keys[1][::-1]]
        for index in range(len(keys)):
            self.userentry.set(decrypt_pat[index](self.userentry.get(), keys[index],decode=True))
            self.passentry.set(decrypt_pat[index](self.passentry.get(), keys[index],decode=True))

    def getTitle(self):
        return self.title

    def getUser(self):
        return self.userentry.get()

    def getPass(self):
        return self.passentry.get()

    def pack(self):
        self.titlelabel.pack(side = self.side)
        self.userlabel.pack(side= self.side)
        self.passlabel.pack(side= self.side)

    def unpack(self):
        self.titlelabel.pack_forget()
        self.userlabel.pack_forget()
        self.passlabel.pack_forget()

class InEntry:
    def __init__(self, master, **kwargs):
        self.master = master
        self.side = kwargs.get("side", None)

        self.entry = tk.Entry(self.master)
        self.entry.delete(0,tk.END)
        self.entry.insert(0,kwargs.get("insert","Entry"))
        self.entry.config(foreground = "grey")
        self.entry.bind("<1>",self._clicked)

    def _clicked(self,event):
        self.entry.delete(0,tk.END)
        self.entry.config(foreground = "black")

    def pack(self):
        self.entry.pack(side = self.side)

    def get(self):
        return self.entry.get()

class ImageGen:
    def __init__(self,master, path, **kwargs):
        self.master = master
        self.side = kwargs.get("side", None)

        img = ImageTk.PhotoImage(Image.open(path).convert("RGBA"))
        self.labeling = tk.Label(self.master,image=img)
        self.labeling.image = img

    def pack(self):
        self.labeling.pack(side = self.side)


class ButtonGen:
    def __init__(self,master, **kwargs):
        self.master = master
        self.text = kwargs.get("text","None")
        self.command = kwargs.get("command",None)
        self.side = kwargs.get("side", None)
        self.button = tk.Button(self.master,text=self.text, command = self.command)

    def pack(self):
        self.button.pack(side=self.side)
