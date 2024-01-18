import customtkinter
from tkinter import *
from tkinter import ttk, filedialog, font
import tkinter as tk
from tkinter import messagebox
from LolDbSqlite import LolDbSqlite
import PIL
from PIL import ImageTk
from PIL import Image

class LolGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=LolDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('League of Legends Champion Database')
        self.iconbitmap('C:\SP2\SimpleDb\LeagueIcon.ico')
        self.geometry('1250x500')
        self.config(bg='#091428')
        self.resizable(False, False)

        self.custom_font1 = customtkinter.CTkFont(family='Beaufort for LOL', size=22, weight='bold')
        self.custom_font2 = customtkinter.CTkFont(family='Beaufort for LOL', size=12)
        self.custom_font3 = customtkinter.CTkFont(family='Beaufort for LOL', size=18)

        self.logo1_label = self.newCtkLabel('League of Legends')
        self.logo1_label.place(x=100, y=40)
        self.logo2_label = self.newCtkLabel('Champion Database')
        self.logo2_label.place(x=95, y=65)

        self.id_label = self.newCtkLabel('Title')
        self.id_label.place(x=20, y=160)
        self.id_entry = self.newCtkEntry()
        self.id_entry.place(x=120, y=160)

        self.name_label = self.newCtkLabel('Name')
        self.name_label.place(x=20, y=220)
        self.name_entry = self.newCtkEntry()
        self.name_entry.place(x=120, y=220)

        self.role_label = self.newCtkLabel('Role')
        self.role_label.place(x=20, y=280)
        self.role_cboxVar = StringVar()
        self.role_cboxOptions = ['Assassin', 'Fighter', 'Mage', 'Marksman', 'Support', 'Tank']
        self.role_cbox = self.newCtkComboBox(options=self.role_cboxOptions, 
                                    entryVariable=self.role_cboxVar)
        self.role_cbox.place(x=120, y=280)

        self.gender_label = self.newCtkLabel('Gender')
        self.gender_label.place(x=20, y=340)
        self.gender_cboxVar = StringVar()
        self.gender_cboxOptions = ['Male', 'Female', 'Other', 'Not applicable']
        self.gender_cbox = self.newCtkComboBox(options=self.gender_cboxOptions, 
                                    entryVariable=self.gender_cboxVar)
        self.gender_cbox.place(x=120, y=340)

        self.position_label = self.newCtkLabel('Position')
        self.position_label.place(x=20, y=400)
        self.position_cboxVar = StringVar()
        self.position_cboxOptions = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']
        self.position_cbox = self.newCtkComboBox(options=self.position_cboxOptions, 
                                    entryVariable=self.position_cboxVar)
        self.position_cbox.place(x=120, y=400)


        self.add_button = self.newCtkButton(text='Add Champion',
                                onClickHandler=self.add_entry,
                                fgColor='#80ACB9',
                                textcolor='#FFF',
                                hoverColor='#785A28',
                                borderColor='#0397AB')
        self.add_button.place(x=415,y=350)

        self.new_button = self.newCtkButton(text='New Champion',
                                
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=415,y=400)

        self.update_button = self.newCtkButton(text='Update Champion',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=710,y=400)

        self.delete_button = self.newCtkButton(text='Delete Champion',
                                    onClickHandler=self.delete_entry,
                                    textcolor='#FFF',
                                    fgColor='#FFBA02',
                                    hoverColor='#B36618',
                                    borderColor='#FFBA02')
        self.delete_button.place(x=710,y=350)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=1015,y=400)

        self.import_button = self.newCtkButton(text='Import CSV',
                                               onClickHandler=self.import_from_csv)
        self.import_button.place(x=1015, y=350)

        self.style = ttk.Style(self)
        self.style.configure('Treeview', 
                    font=self.custom_font2, 
                    foreground='#313837',
                    background='#fff',
                    fieldbackground='#0397AB',
                    padding=(10, 5),
                    borderwidth=2,
                    selectbackground='#0397AB',
                    selectforeground='#fff',
                    rowheight=30)

        self.style.map('Treeview', background=[('selected', '#0397AB')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Title', 'Name', 'Role', 'Gender', 'Position')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Title', anchor=tk.CENTER, width=100)
        self.tree.column('Name', anchor=tk.CENTER, width=100)
        self.tree.column('Role', anchor=tk.CENTER, width=100)
        self.tree.column('Gender', anchor=tk.CENTER, width=10)
        self.tree.column('Position', anchor=tk.CENTER, width=10)

        self.tree.heading('Title', text='Title')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Role', text='Role')
        self.tree.heading('Gender', text='Gender')
        self.tree.heading('Position', text='Position')


        self.tree.place(x=410, y=50, width=810, height=280)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.custom_font1
        widget_TextColor='#C8AA6E'
        widget_BgColor='#091428'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.custom_font3
        widget_TextColor='#785A28'
        widget_FgColor='#FFF'
        widget_BorderColor='#0397AB'
        widget_BgColor='#091428'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    bg_color=widget_BgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.custom_font3
        widget_TextColor='#785A28'
        widget_FgColor='#FFF'
        widget_BgColor='#091428'
        widget_DropdownHoverColor='#0397AB'
        widget_DropdownFgColor='#FFF'
        widget_DropdownTextColor='#785A28'
        widget_ButtonColor='#0397AB'
        widget_ButtonHoverColor='#0397AB'
        widget_BorderColor='#0397AB'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        bg_color=widget_BgColor,
                                        dropdown_hover_color=widget_DropdownHoverColor,
                                        dropdown_fg_color=widget_DropdownFgColor,
                                        dropdown_text_color=widget_DropdownTextColor,
                                        button_color=widget_ButtonColor,
                                        button_hover_color=widget_ButtonHoverColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        widget.set(options[0])
        return widget

    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#FFF', hoverColor='#F0E6D2', bgColor='#091428', borderColor='#0397AB', textcolor='#C89B3C'):
        widget_Font=self.custom_font1
        widget_TextColor=textcolor
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=200
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width)
       
        return widget

    def add_to_treeview(self):
        champions = self.db.fetch_champions()
        self.tree.delete(*self.tree.get_children())
        for champion in champions:
            print(champion)
            self.tree.insert('', END, values=champion)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.id_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.role_cboxVar.set('Assassin')
        self.gender_cboxVar.set('Male')
        self.position_cboxVar.set('Top')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.id_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.role_cboxVar.set(row[2])
            self.gender_cboxVar.set(row[3])
            self.position_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        title=self.id_entry.get()
        name=self.name_entry.get()
        role=self.role_cboxVar.get()
        gender=self.gender_cboxVar.get()
        position=self.position_cboxVar.get()

        if not (title and name and role and gender and position):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.id_exists(title):
            messagebox.showerror('Error', 'Title already exists')
        else:
            self.db.insert_champion(title, name, role, gender, position)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a champion to delete')
        else:
            title = self.id_entry.get()
            self.db.delete_champion(title)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a champion to update')
        else:
            title=self.id_entry.get()
            name=self.name_entry.get()
            role=self.role_cboxVar.get()
            gender=self.gender_cboxVar.get()
            position=self.position_cboxVar.get()
            self.db.update_champion(name, role, gender, position, title)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been updated')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success', f'Data exported to {self.db.dbName}.csv')

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(title='Select CSV file',
                                           filetypes=[('CSV files', '*.csv')])
        if file_path:
                self.db.import_csv(file_path)
                self.add_to_treeview()
                messagebox.showinfo('Success', 'Data imported from CSV')
        else:
            # Error: User cancels file selection or closes the dialog box
            messagebox.showinfo('Info', 'CSV import canceled or no file selected')
  

        