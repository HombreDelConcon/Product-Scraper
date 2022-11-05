import tkinter
import customtkinter

"""
class ExampleApp(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.set_appearance_mode('system')
        self.geometry("500x400")
        self.button = customtkinter.CTkButton(self, text="Create Toplevel", command=self.create_toplevel, fg_color=('royalblue4'), hover_color='black')
        self.button.pack(side=('left'), padx=5, pady=5)
        self.button2 = customtkinter.CTkButton(self, text='SomethingElse', border_width=2, border_color='snow', command=self._print_HW)
        self.button2.pack(side=('left'), padx=5, pady=5)
        photo_image = tkinter.PhotoImage(file='C:\\Users\\megah\\Documents\\Scraper\\shots\\Shot1.png')
        self.frame = customtkinter.CTkFrame(master=self, width=200, height=200, corner_radius=10)
        self.frame.pack(side='right', padx=20, pady=20)#, sticky='nsew')
        #self.frame.button3 = customtkinter.CTkButton(master=self.frame, text='SomethingElse', border_width=2, border_color='snow', image=photo_image, command=self._print_HW)
        #self.frame.button3.pack(side=('left'), padx=30, pady=30)
        self.frame.place(relx=0.5, rely=.5, anchor=tkinter.SW)
        self.scrollbar = customtkinter.CTkScrollbar(self)

    def create_toplevel(self):
        window = customtkinter.CTkToplevel(self)
        window.geometry("400x200")
        window.configure(bg='slate blue')
        # create label on CTkToplevel window
        label = customtkinter.CTkLabel(window, text="CTkToplevel window")
        label.pack(side="top", fill="both", expand=True, padx=40, pady=40)
    def _print_HW(self):
        print('Lorem Ipsum dolor sit amet')

if __name__ == '__main__':
    app = ExampleApp()
    app.mainloop()
"""
"""
app = customtkinter.CTk()
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# create scrollable textbox
tk_textbox = tkinter.Text(app, highlightthickness=0)
tk_textbox.grid(row=0, column=0, sticky="nsew")

# create CTk scrollbar
ctk_textbox_scrollbar = customtkinter.CTkScrollbar(app, command=tk_textbox.yview)
ctk_textbox_scrollbar.grid(row=0, column=1, sticky="ns")

# connect textbox scroll event to CTk scrollbar
tk_textbox.configure(yscrollcommand=ctk_textbox_scrollbar.set)

app.mainloop()
"""

root_tk = customtkinter.CTk()
root_tk.geometry(f"{600}x{500}")
root_tk.title("CTk example")
"""
def button_event():
    print("button pressed")
button = customtkinter.CTkButton(master=root_tk,
                                 width=120,
                                 height=32,
                                 border_width=0,
                                 corner_radius=8,
                                 text="CTkButton",
                                 command=button_event)
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
"""
text_var = tkinter.StringVar(value="CTkLabel")
photo_image = tkinter.PhotoImage(file='shots\\Shot1.png')
label = customtkinter.CTkLabel(master=root_tk,
                               textvariable=text_var,
                               width=120,
                               height=25,
                               fg_color=("white", "gray75"),
                               corner_radius=8,
                               image=photo_image)
label.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
root_tk.attributes('-fullscreen', True)
root_tk.mainloop()



















