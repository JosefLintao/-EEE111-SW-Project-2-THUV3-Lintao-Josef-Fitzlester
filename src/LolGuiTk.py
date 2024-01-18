from tkinter import *
from tkinter import ttk, filedialog
import tkinter as tk
from tkinter import messagebox
from LolDbSqlite import LolDbSqlite

class LolGuiTk(Tk):
    def __init__(self, dataBase=LolDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('League of Legends Champion Database')
        self.geometry('1500x500')
        self.config(bg='#161C25')
        self.resizable(False, False)

        self.font1 = ('Beaufort for LOL', 20, 'bold')
        self.font2 = ('Beaufort for LOL', 12, 'bold')

        self.title_label = self.newCtkLabel('Title')
        self.title_label.place(x=20, y=40)
        self.title_entryVar = StringVar()
        self.title_entry = self.newCtkEntry(entryVariable=self.title_entryVar)
        self.title_entry.place(x=100, y=40)

        self.name_label = self.newCtkLabel('Name')
        self.name_label.place(x=20, y=100)
        self.name_entryVar = StringVar()
        self.name_entry = self.newCtkEntry(entryVariable=self.name_entryVar)
        self.name_entry.place(x=100, y=100)

        self.role_label = self.newCtkLabel('Role')
        self.role_label.place(x=20, y=160)
        self.role_cboxVar = StringVar()
        self.role_cboxOptions = ['Assassin', 'Fighter', 'Mage', 'Marksman', 'Support', 'Tank']
        self.role_cbox = self.newCtkComboBox(options=self.role_cboxOptions, 
                                    entryVariable=self.role_cboxVar)
        self.role_cbox.place(x=100, y=160)

        self.gender_label = self.newCtkLabel('Gender')
        self.gender_label.place(x=20, y=220)
        self.gender_cboxVar = StringVar()
        self.gender_cboxOptions = ['Male', 'Female', 'Other', 'Not applicable']
        self.gender_cbox = self.newCtkComboBox(options=self.gender_cboxOptions, 
                                    entryVariable=self.gender_cboxVar)
        self.gender_cbox.place(x=100, y=220)

        self.position_label = self.newCtkLabel('Position')
        self.position_label.place(x=20, y=280)
        self.position_cboxVar = StringVar()
        self.position_cboxOptions = ['Top', 'Jungle', 'Mid', 'Bot', 'Support']
        self.position_cbox = self.newCtkComboBox(options=self.position_cboxOptions, 
                                    entryVariable=self.position_cboxVar)
        self.position_cbox.place(x=100, y=280)


        self.add_button = self.newCtkButton(text='Add Champion',
                                onClickHandler=self.add_entry,
                                fgColor='#05A312',
                                hoverColor='#00850B',
                                borderColor='#05A312')
        self.add_button.place(x=50,y=350)

        self.new_button = self.newCtkButton(text='New Champion',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=50,y=400)

        self.update_button = self.newCtkButton(text='Update Champion',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=360,y=400)

        self.delete_button = self.newCtkButton(text='Delete Champion',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=670,y=400)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=980,y=400)

        self.import_button = self.newCtkButton(text='Import CSV',
                                               onClickHandler=self.import_from_csv)
        self.import_button.place(x=1290, y=400)

        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#000',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

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

        self.tree.place(x=360, y=20, width=1095, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_BgColor='#161C25'

        widget = ttk.Label(self, 
                        text=text)
        return widget

    def newCtkEntry(self, text = 'CTK Label', entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25

        widget = ttk.Entry(self, textvariable=entryVariable, width=widget_Width)
        return widget

    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=25
        widget_Options=options

        widget = ttk.Combobox(self, 
                              textvariable=entryVariable,
                              width=widget_Width)
        
        widget['values'] = tuple(options)
        widget.current(1)
        return widget

    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#161C25', hoverColor='#FF5002', bgColor='#161C25', borderColor='#F15704'):
        widget_Font=self.font1
        widget_TextColor='#FFF'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=2
        widget_Cursor='hand2'
        widget_CornerRadius=15
        widget_Width=25
        widget_Function=onClickHandler

        widget = ttk.Button(self,
                            text=text,
                            command=widget_Function,
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
        self.title_entryVar.set('')
        self.name_entryVar.set('')
        self.role_cboxVar.set('Assassin')
        self.gender_cboxVar.set('Male')
        self.position_cboxVar.set('Top')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.title_entryVar.set(row[0])
            self.name_entryVar.set(row[1])
            self.role_cboxVar.set(row[2])
            self.gender_cboxVar.set(row[3])
            self.position_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        title=self.title_entryVar.get()
        name=self.name_entryVar.get()
        role=self.role_cboxVar.get()
        gender=self.gender_cboxVar.get()
        status=self.position_cboxVar.get()

        if not (title and name and role and gender and status):
            messagebox.showerror('Error', 'Enter all fields.')
        elif self.db.title_exists(title):
            messagebox.showerror('Error', 'Title already exists')
        else:
            self.db.insert_champion(title, name, role, gender, status)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been inserted')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose a champion to delete')
        else:
            title = self.title_entryVar.get()
            self.db.delete_champion(title)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success', 'Data has been deleted')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error', 'Choose champion information to update')
        else:
            title=self.title_entryVar.get()
            name=self.name_entryVar.get()
            role=self.role_cboxVar.get()
            gender=self.gender_cboxVar.get()
            status=self.position_cboxVar.get()
            self.db.update_champion(name, role, gender, status, title)
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
            messagebox.showinfo('Info', 'CSV import canceled or no file selected')