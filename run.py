try:
    import tkinter as tk
    import entry
    import encryptions
    from PIL import Image, ImageTk
    import random
    import os
    import hashlib
except:
    import Tkinter as tk
    import entry
    import encryptions
    from PIL import Image, ImageTk
    import random
    import os
    import hashlib

class Window(tk.Frame):
    def __init__(self,master = None, **kwargs):
        tk.Frame.__init__(self,master)
        self.elements = {}

    def add(self,name,object):
        self.elements[name]=object

    def packobjs(self):
        for elem_name, elem_object in self.elements.items():
            elem_object.pack()

    def getEverything(self):
        ret = {}
        for elem_name, elem_obj in self.elements.items():
            try:
                ret[elem_name] = elem_obj.get()
            except:
                pass
        return ret

def login_win():
    login = Window(root)
    login.add("logo", entry.ImageGen(login, "rsz_key.png"))
    login.add("userinput", entry.InEntry(login))
    login.add("passinput", entry.InEntry(login))
    login.add("login", entry.ButtonGen(login, text="Login",command=lambda: login_check(login.getEverything())))
    login.add("register", entry.ButtonGen(login, text="Register", command=lambda: open_win("register")))
    login.add("msg", tk.Label(login, textvariable=msg))
    login.packobjs()
    return login

def register_win():
    register = Window(root)
    register.add("logo", entry.ImageGen(register, "rsz_key.png"))
    register.add("userinput", entry.InEntry(register, insert="Desired Username"))
    register.add("passinput", entry.InEntry(register, insert="Desired Password"))
    register.add("login", entry.ButtonGen(register, text="Login", command=lambda: open_win("login")))
    register.add("submit", entry.ButtonGen(register, text="Submit", command=lambda: submit_reg(register.getEverything())))
    register.add("msg", tk.Label(register,textvariable=msg))
    register.packobjs()
    return register

def view_win(user:str, key):
    view = Window()

    view.add("frame",tk.Frame(view))
    view.add("canvas", tk.Canvas(view.elements["frame"]))
    view.add("subframe", tk.Frame(view.elements["canvas"]))
    scrollbar = tk.Scrollbar(view.elements["frame"],orient="vertical",command=view.elements["canvas"].yview)
    view.elements["canvas"].configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right",fill="y")

    windows["create"] = create_win(user,key)
    view.add("create",entry.ButtonGen(view,text="Create Entry",command = lambda: open_win("create")))

    for filename in os.listdir(os.path.join(os.getcwd(),user)):
        if filename.endswith(".txt") and filename != "password.txt":
            with open(os.path.join(os.getcwd(),user+"\\"+filename), "r") as file:
                title = file.readline().rstrip("\r\n")
                usr = file.readline().rstrip("\r\n")
                pss = file.readline()
                view.add(filename,entry.AccEntry(key,view.elements["subframe"], title=title, user=usr, pwd=pss))
                view.elements[filename].decrypt()

    view.packobjs()
    view.elements["canvas"].create_window((0, 0), window=view.elements["subframe"], anchor='nw')

    def _configure_frame(event):
        size = (view.elements["subframe"].winfo_reqwidth(), view.elements["subframe"].winfo_reqheight())
        view.elements["canvas"].configure(scrollregion="0 0 %s %s" % size)

    view.elements["subframe"].bind("<Configure>",_configure_frame)

    return view

def create_win(user:str, key):

    def create_sub(values):
        title = values["title"]
        usr = values["user"]
        pwd = values["pass"]

        for filename in os.listdir(os.path.join(os.getcwd(),user)):
            if filename == title:
                msg.set("Title already exist.")
                return

        temp = entry.AccEntry(key,create, title=title, user=usr, pwd=pwd)
        temp.encrypt()

        path = os.path.join(os.getcwd(),user+'\\'+title+'.txt')
        with open(path, "w") as file:
            file.write(temp.getTitle()+"\n")
            file.write(temp.getUser()+"\n")
            file.write(temp.getPass())

        msg.set("Success. Click Go Back to go back.")

    create = Window()

    create.add("logo", entry.ImageGen(create, "rsz_key.png"))
    create.add("title", entry.InEntry(create,insert="Title"))
    create.add("user", entry.InEntry(create, insert="Username"))
    create.add("pass", entry.InEntry(create, insert="Password"))
    create.add("back", entry.ButtonGen(create, text= "Go Back", command = lambda: open_win("view")))
    create.add("submit", entry.ButtonGen(create, text= "Submit", command = lambda: create_sub(create.getEverything())))
    create.add("msg", tk.Label(create, textvariable=msg))
    create.packobjs()

    return create

def open_win(window:str):
    clear()
    windows[window].pack()

def clear():
    for win_name, win_obj in windows.items():
        win_obj.pack_forget()

def submit_reg(values:dict):
    user = values["userinput"]
    pwd = values["passinput"]

    if os.path.exists(user):
        msg.set("username already exist")
        return

    pwd = salt_sha(pwd,user)

    os.makedirs(user)
    with open(os.path.join(os.getcwd(),user+"\\password.txt"),"w") as file:
        file.write(pwd)

    msg.set("Account successfully created")


def gen_key(pwd:str):
    key_ret = []
    key_pat = []

    acc = 0
    for char in pwd:
        acc += ord(char)

    random.seed(acc)
    for x in range(3):
        temp = random.randint(1,3)
        if temp == 1:
            key_pat.append(encryptions.caesar) # int
            key_ret.append(random.randint(0,acc))
        elif temp == 2:
            key_pat.append(encryptions.railfence_handler) #int
            key_ret.append(random.randint(0,len(pwd)-1))
        elif temp == 3:
            key_pat.append(encryptions.keywordcipher) #string
            key_ret.append(gen_str(random.randint(1,(acc%26)+1),acc))

    return (key_ret, key_pat)

def gen_str(length,seed, **kwargs):
    random.seed(seed)
    if kwargs.get("numerics", False) and length <= 26:
        temp = random.sample(range(26), length)
        alpha = "abcdefghijklmnopqrstuvwxyz0123456789"

        return ''.join([alpha[i] for i in temp])

    elif length <= 26:
        temp = random.sample(range(26),length)
        alpha = "abcdefghijklmnopqrstuvwxyz"

        return ''.join([alpha[i] for i in temp])

def salt_sha(pwd:str,user:str): #TODO: break this function down
    ret = ""
    alphanum = "abdefhijklmnoqrstuvwyz012346789"
    temp = user
    for i in range(len(temp)-1,-1,-1):
        polyacc = 0
        for index in range(len(user)):
            polyacc += ord(user[index])*(33**index)

        compression = polyacc % 31
        ret += alphanum[compression]
        user = user[:i]

    return hashlib.sha512((pwd+ret).encode()).hexdigest()

def login_check(values):
    user = values["userinput"]
    pwd = values["passinput"]

    with open(os.path.join(os.getcwd(), user+"\\password.txt"), "r") as file:
        if file.readline() == salt_sha(pwd,user):
            msg.set("login successful")
            key = gen_key(pwd)
            windows["view"] = view_win(user,key)
            open_win("view")

        else:
            msg.set("login failed")
    return

if __name__ == '__main__':

    windows = {}

    root = tk.Tk()
    root.title("Pass Saver 2019")
    root.minsize(width=400, height=400)
    root.maxsize(width=400, height=400)

    msg = tk.StringVar()
    msg.set("")

    windows["login"] = login_win()
    windows["register"] = register_win()
    open_win("login")

    root.mainloop()
