####################################################
#  D1014636 潘子珉                                                									
####################################################
import tkinter as tk
import tkinter.simpledialog as sd
import threading

lock = threading.Lock()

class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.socket = None
        self.isSrart = False
        self.title('Server')
        self.geometry("500x500")
        self.menubar = tk.Menu(self)
        self.menubar.add_cascade(label = "開始", command = self.changeState)
        self.menubar.add_cascade(label = "清除", command = self.clear)
        self.configure(menu = self.menubar)
        self.protocol("WM_DELETE_WINDOW", self.close)
        
    def changeState(self):
        if self.socket.isSrart:
            print('socket stop')
            self.menubar.entryconfig(1, label="開始")
            self.socket.stop()
        else:
            print('socket start')
            self.menubar.entryconfig(1, label="停止")
            self.socket.start()
            
    def clear(self):
        pass
    
    def close(self):
        self.socket.stop()
        self.destroy()

class Page(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        vscrollbar = tk.Scrollbar(self, orient = 'vertical')
        vscrollbar.pack(fill = 'y', side = 'right', expand = False)
        self.canvas = tk.Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set)
        vscrollbar.config(command = self.canvas.yview)
        self.frame = tk.Frame(self.canvas)
        self.canvas.config(yscrollcommand = vscrollbar.set)
        self.canvas.create_window((0, 0), window = self.frame, anchor="nw")
        self.canvas.pack(side = 'left', fill = 'both', expand = True)
        self.frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        self.pack(fill = 'both', side = 'top', expand = True)
        
    def append(self, text, color):
        tk.Label(self.frame, text = text).pack(fill = 'x', expand = True)
        
class Console(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.listbox = tk.Listbox(self, font = ("Times", 11, ""))
        self.listbox.pack(side = "left", fill = "both", expand = True)
        self.scrollbar = tk.Scrollbar(self, orient = "vertical", command = self.listbox.yview)
        self.scrollbar.pack(side = "left", fill = "both", expand = False)
        self.listbox.configure(yscrollcommand = self.scrollbar.set)
        self.pack(fill = 'both', expand = True)
        self.master.menubar.entryconfig(2, command = self.clear)
        
    def append(self, text, color = None):
        lock.acquire()
        self.listbox.insert(tk.END, text)
        if color:
            self.listbox.itemconfig(tk.END, { 'bg' :  color, 'fg' : '#fff'})
        else:
            self.listbox.itemconfig(tk.END)
        lock.release()
            
    def clear(self):
        self.listbox.delete(0,tk.END)

class Dialog(sd.Dialog):
    def __init__(self, parent, text):
        self.text = text
        super().__init__(parent, "錯誤")
        
    def body(self, frame):
        tk.Label(frame, text = self.text, justify = 'left', width = 50, pady = 10).pack()

    def buttonbox(self):
        self.ok__button = tk.Button(self, text = '好', command = self.ok_pressed, default = 'active', width = 5)
        self.ok__button.pack(side = 'bottom', pady = 10, expand = True)

    def ok_pressed(self):
        self.destroy()