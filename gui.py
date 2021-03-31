import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageGrab
from chatbot import process_input
from language import read_text

BG_COLOUR = 'white'

class ChatbotGUI:
    last_x, last_y = None, None

    def __init__(self):
        self.app = tk.Tk()
        self.app.title("Cocktail Chatbot")
        self.app.geometry("1280x720")
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_columnconfigure(0, weight=1)

        self.message_window = tk.Listbox(self.app, bg=BG_COLOUR, font=('Times', 24))
        self.message_window.grid(column=0, row=0, columnspan=16, rowspan=6, sticky="nsew")
        self.message_window.bind('<<ListboxSelect>>', self.on_select)

        self.message_scroll = tk.Scrollbar(self.app)
        self.message_scroll.grid(column=15, row=0, rowspan=6, sticky="nse")

        self.message_window.config(yscrollcommand=self.message_scroll.set)
        self.message_scroll.config(command=self.message_window.yview)

        self.text_entry = tk.Entry(self.app, bg=BG_COLOUR)
        self.text_entry.grid(column=0, row=6, columnspan=16, sticky="nsew")
        self.text_entry.bind("<Return>", self.on_input)
 
        self.canvas = tk.Canvas(self.app, bg=BG_COLOUR)
        self.canvas.grid(row=7, column=0, columnspan=14, rowspan=2, sticky="nsew")
        self.canvas.bind("<Button-1>", self.get_xy)
        self.canvas.bind("<B1-Motion>", self.draw)

        self.clear_button = tk.Button(self.app, bg='red', text="Clear")
        self.clear_button.grid(column=14, columnspan=2, row=8, rowspan=1, sticky="nsew")
        self.clear_button.bind("<Button-1>", self.clear_canvas)

        self.submit_button = tk.Button(self.app, bg='green', text="Submit")
        self.submit_button.grid(column=14, columnspan=2, row=7, rowspan=1, sticky="nsew")
        self.submit_button.bind("<Button-1>", self.submit_canvas)
        
        self.bring_front()
        self.app.mainloop()

    def on_input(self, event):
        user_input = self.text_entry.get()
        self.text_entry.delete(0, tk.END)
        self.submit_text(user_input)

    def clear_canvas(self, event):
        self.canvas.delete("all")

    def submit_canvas(self, event):
        file_name = './data/handwriting.png'
        x = self.app.winfo_rootx() + self.canvas.winfo_x()
        y = self.app.winfo_rooty() + self.canvas.winfo_y()
        x_end = x + self.canvas.winfo_width()
        y_end = y + self.canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x_end, y_end)).save(file_name)

        self.clear_canvas(event)

        recognized_text = read_text(file_name)
        self.submit_text(recognized_text)
        
    def submit_text(self, text):
        replys = process_input(self, text)
        self.add_output(replys)

    def on_select(self, event):
        self.message_window.selection_clear(0, tk.END)

    def bring_front(self):
        self.app.lift()
        self.app.attributes('-topmost', True)
        self.app.attributes('-topmost', False)

    def get_xy(self, event):
        self.last_x, self.last_y = event.x, event.y

    def draw(self, event):
        self.canvas.create_line((self.last_x, self.last_y, event.x, event.y), width=3)
        self.last_x, self.last_y = event.x, event.y

    def add_output(self, replys):
        for reply in replys:
            self.message_window.insert(0, reply)
    
    def add_input(self, text):
        self.message_window.insert(0, text)

    def get_file(self):
        file_path = filedialog.askopenfilename()
        return file_path