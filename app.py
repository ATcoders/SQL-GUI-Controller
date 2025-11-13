from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter.ttk import Treeview, Style
from PIL import ImageTk, Image
import mysql.connector

mydb = None
cursor = None
login_win = None


login_window = Tk()
login_window.title("SQL Controller Login")
login_window.geometry("450x350")
login_window.resizable(False, False)
login_window.configure(bg="#0f172a")


def create_table_window(main_window):
    selected_db = "Placeholder_DB" 
    table_win = Toplevel(main_window)
    table_win.title("Create Table")
    table_win.geometry("620x680")
    table_win.resizable(False, False)
    table_win.configure(bg="#0f172a")

    header_frame = Frame(table_win, bg="#1e293b")
    header_frame.pack(fill=X, pady=(0, 20))
            
    Label(header_frame, text="Create New Table", font=("Arial", 18, "bold"),bg="#1e293b", fg="white").pack(pady=15)
    Label(header_frame, text=f"Database: {selected_db}", font=("Arial", 10),bg="#1e293b", fg="#94a3b8").pack(pady=(0, 10))
            
    name_frame = Frame(table_win, bg="#0f172a")
    name_frame.pack(padx=30, pady=10, fill=X)

    Label(name_frame, text="Table Name", font=("Arial", 11, "bold"), bg="#0f172a", fg="white").pack(anchor=W, pady=(0, 5))
    table_name_entry = Entry(name_frame, font=("Arial", 13), bg="#1e293b",fg="white", bd=0, width=40, insertbackground="white")
    table_name_entry.pack(fill=X, ipady=8)
            
    columns_header_frame = Frame(table_win, bg="#0f172a")
    columns_header_frame.pack(anchor=W, padx=30, pady=(15, 5), fill=X)
            
    Label(columns_header_frame, text="Table Columns", font=("Arial", 11, "bold"),bg="#0f172a", fg="white").pack(side=LEFT)
            
    container = Frame(table_win, bg="#0f172a")
    container.pack(padx=30, fill=BOTH, expand=True)
            
    canvas = Canvas(container, bg="#0f172a", height=280, highlightthickness=0)
    scrollbar = Scrollbar(container, orient="vertical", command=canvas.yview,bg="#334155", troughcolor="#0f172a")
    scrollable_frame = Frame(canvas, bg="#0f172a")

    scrollable_frame.bind(
         "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
            
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
            
    # --- CORRECTED PACKING ORDER ---
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.pack(side=LEFT, fill=BOTH, expand=True)
    # -----------------------------
            
    column_widgets = []
    data_types = ["INT", "VARCHAR(255)", "TEXT", "DATE", "BOOLEAN", "FLOAT"]

    def add_column_field():
        column_frame = Frame(scrollable_frame, bg="#1e293b", relief="flat")
        column_frame.pack(pady=8, fill=X, padx=(0, 40))
                
        header = Frame(column_frame, bg="#334155")
        header.pack(fill=X)
                
        column_label = Label(header, text=f"  Column {len(column_widgets) + 1}", font=("Arial", 9, "bold"), bg="#334155", fg="#cbd5e1")
        column_label.pack(side=LEFT, pady=4)

        def remove_column():
            nonlocal column_widgets
            column_widgets = [w for w in column_widgets if w[0] != column_frame]
            column_frame.destroy()
                    
            for i, widget_tuple in enumerate(column_widgets):
                header_widget = widget_tuple[0].winfo_children()[0] 
                label_widget = header_widget.winfo_children()[0]  
                label_widget.config(text=f"  Column {i + 1}")
                    
            canvas.update_idletasks()
            canvas.config(scrollregion=canvas.bbox("all"))
        
        remove_btn = Button(header, text="X", font=("Arial", 8, "bold"), bg="#ef4444", fg="white", activebackground="#dc2626", activeforeground="white", relief="flat", bd=0, width=3, command=remove_column)
        remove_btn.pack(side=RIGHT, padx=5, pady=2)
        
        input_frame = Frame(column_frame, bg="#1e293b", padx=10, pady=10)
        input_frame.pack(fill=X)
        
        Label(input_frame, text="Name:", font=("Arial", 10), bg="#1e293b", fg="white").pack(side=LEFT, padx=(0, 5))
        name_entry = Entry(input_frame, font=("Arial", 11), bg="#334155", fg="white", bd=0, insertbackground="white", width=15)
        name_entry.pack(side=LEFT, ipady=5, padx=(0, 20))
        
        Label(input_frame, text="Type:", font=("Arial", 10), bg="#1e293b", fg="white").pack(side=LEFT, padx=(0, 5))
        data_type_var = StringVar(input_frame)
        data_type_var.set(data_types[0])
        
        type_menu = OptionMenu(input_frame, data_type_var, *data_types)
        type_menu.config(font=("Arial", 10), bg="#334155", fg="white", activebackground="#475569", bd=0, relief="flat")
        type_menu["menu"].config(bg="#334155", fg="white", activebackground="#475569", bd=0)
        type_menu.pack(side=LEFT, padx=(0, 20))
        
        is_pk_var = BooleanVar()
        pk_check = Checkbutton(input_frame, text="Primary Key", variable=is_pk_var, font=("Arial", 10), bg="#1e293b", fg="white", selectcolor="#1e293b", activebackground="#1e293b", activeforeground="white")
        pk_check.pack(side=LEFT)

        column_widgets.append((column_frame, name_entry, data_type_var, is_pk_var))
        
        canvas.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))


    add_col_btn = Button(table_win, text="+ Add Column", font=("Arial", 10, "bold"), bg="#64748b", fg="white", activebackground="#475569", activeforeground="white", relief="flat", bd=0, command=add_column_field)
    add_col_btn.pack(pady=(10, 20))


    button_frame = Frame(table_win, bg="#0f172a")
    button_frame.pack(pady=10)

    Button(button_frame, text="Create Table", font=("Arial", 12, "bold"),bg="#10b981", fg="white", padx=20, pady=30, relief="flat", bd=0, activebackground="#059669", activeforeground="white").pack(side=LEFT, padx=10) 
    
    Button(button_frame, text="Cancel", font=("Arial", 12, "bold"),bg="#ef4444", fg="white", padx=20, pady=8, relief="flat", bd=0, activebackground="#dc2626", activeforeground="white",command=table_win.destroy).pack(side=LEFT, padx=10)
    
    add_column_field()

# -------------------------------       Choose Existing DB     ---------------------------------------------------------------
def choose_existing(main_window):



    win = Toplevel(main_window)
    win.title("Choose Existing Database")
    win.geometry("750x550")
    win.resizable(False, False)
    win.configure(bg="#0f172a")


    title_label = Label(win, text="Select Database & Table", font=("Arial", 20, "bold"),bg="#0f172a", fg="white")
    title_label.pack(pady=20)

    main_container = Frame(win, bg="#0f172a")
    main_container.pack(pady=10, padx=20, fill=BOTH, expand=True)

    db_frame = Frame(main_container, bg="#1e293b", relief="flat", bd=0)
    db_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

    db_header = Label(db_frame, text="📁 Select Database", font=("Arial", 13, "bold"),bg="#334155", fg="white", pady=10)
    db_header.pack(fill=X)
    db_scroll_frame = Frame(db_frame, bg="#1e293b")
    db_scroll_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
    db_scrollbar = Scrollbar(db_scroll_frame, bg="#334155", troughcolor="#1e293b")
    db_scrollbar.pack(side=RIGHT, fill=Y)
    db_listbox = Listbox(db_scroll_frame, bg="#1e293b", fg="white", font=("Arial", 11), selectbackground="#3b82f6",selectforeground="white", bd=0, highlightthickness=0,yscrollcommand=db_scrollbar.set, relief="flat")
    db_listbox.pack(side=LEFT, fill=BOTH, expand=True)
    db_scrollbar.config(command=db_listbox.yview)

    # --- TABLE COLUMN ---
    table_frame = Frame(main_container, bg="#1e293b", relief="flat", bd=0)
    table_frame.pack(side=LEFT, fill=BOTH, expand=True)
    table_header = Label(table_frame, text="📋 Select Table", font=("Arial", 13, "bold"), bg="#334155", fg="white", pady=10)
    table_header.pack(fill=X)
    table_scroll_frame = Frame(table_frame, bg="#1e293b")
    table_scroll_frame.pack(fill=BOTH, expand=True, padx=5, pady=5)
    table_scrollbar = Scrollbar(table_scroll_frame, bg="#334155", troughcolor="#1e293b")
    table_scrollbar.pack(side=RIGHT, fill=Y)
    table_listbox = Listbox(table_scroll_frame, bg="#1e293b", fg="white", font=("Arial", 11), selectbackground="#10b981",selectforeground="white", bd=0, highlightthickness=0,yscrollcommand=table_scrollbar.set, relief="flat")
    table_listbox.pack(side=LEFT, fill=BOTH, expand=True)
    table_scrollbar.config(command=table_listbox.yview)

    # --- FINAL BUTTONS ---
    button_frame = Frame(win, bg="#0f172a")
    button_frame.pack(pady=20)

    Button(button_frame, text="Select Database", font=("Arial", 12, "bold"),bg="#10b981", fg="white", padx=20, pady=8, relief="flat", bd=0,activebackground="#059669", activeforeground="white").pack(side=LEFT, padx=10)
    Button(button_frame, text="Create Table", font=("Arial", 12, "bold"),bg="#3b82f6", fg="white", padx=20, pady=8, relief="flat", bd=0,activebackground="#2563eb", activeforeground="white",command=lambda:create_table_window(win)).pack(side=LEFT, padx=10)
    Button(button_frame, text="Cancel", font=("Arial", 12, "bold"),bg="#64748b", fg="white", padx=20, pady=8, relief="flat", bd=0,activebackground="#475569", activeforeground="white",command=win.destroy).pack(side=LEFT, padx=10)


# --------------------------------      Create Db window     ---------------------------------------------------------------- 
def create_db(main_window):
    new_db_win = Toplevel(main_window)
    new_db_win.title("Create Database")
    new_db_win.geometry("380x260")
    new_db_win.resizable(False, False)
    new_db_win.configure(bg="#0f172a")

    label2 = Label(new_db_win,text="Create New Database",font=("Arial",15,"bold"),bg="#0f172a",fg="white")
    label2.place(x=10,y=20)

    label3 = Label(new_db_win,text="Enter Name for your Database",font=("Arial",10),bg="#0f172a",fg="white")
    label3.place(x=20,y=60)

    db_name = Text(new_db_win, width=20, height=1, font=("Arial", 18),bg="#202e50",bd=0,fg="white")
    db_name.place(x=20, y=90)

    create_btn = Button(new_db_win,text = "Create",font=("Arial",13,"bold"),bg="#27b66f",fg="White",padx=130,pady=2,relief="flat",bd=0,activebackground="#28d07b", activeforeground="white")
    create_btn.place(x = 20 , y= 150)

    cancel_btn = Button(new_db_win,text="Cancel",font=("Arial",10),bg="#0f172a",fg="grey",bd=0,relief="flat",activebackground="#0f172a",command=new_db_win.destroy)
    cancel_btn.place(x=160,y=220)
    

# -----------------------------------     Main Window     -------------------------------------------------------------------
def main_window():
    win = Toplevel(login_window)
    win.title("SQL-GUI Controller")
    win.geometry("900x600")
    win.resizable(False, False)
    win.configure(bg="#0f172a")

    L1 = Label(win,text="SQL-GUI Controller",font=("Arial",32,"bold"),fg="White",bg="#0f172a")
    L1.place(x=210,y=40)

    img = Image.open("Mysql.jpg")
    img = img.resize((450, 400))
    sql_img = ImageTk.PhotoImage(img)

    label = Label(win, image=sql_img, bg="#0f172a")
    label.image = sql_img 
    label.place(x=220, y=100)


    img = Image.open("select.png")
    img = img.resize((30, 30))
    select_img = ImageTk.PhotoImage(img)

    b1 = Button(win,image=select_img,text="Select Existing Database",compound=LEFT,bg="#10b981",fg="white",activebackground="#10b981",activeforeground="white",relief="flat",bd=0,padx=15,pady=8,font=("Roboto", 12, "bold"),command=lambda: choose_existing(win))
    b1.image = select_img
    b1.place(x=100,y=470)


    img2 = Image.open("add.png")
    img2 = img2.resize((30 , 30))
    add_img = ImageTk.PhotoImage(img2)
    
    b2 = Button(win, image=add_img, text="Create New Database", compound=LEFT,bg="#3b82f6",fg="white",activebackground="#3b82f6",activeforeground="white",relief="flat",bd=0,padx=15,pady=8,font=("Roboto", 12, "bold"),command=lambda: create_db(win))
    b2.image = add_img
    b2.place(x=500, y=470)


# ------------------------------------      Login Window      ---------------------------------------------------
Login_label = Label(login_window,text="My-SQL Connection", font=("Arial", 22, "bold"),fg="#3b82f6", bg="#0f172a").pack(pady=(25, 10))

usr_name = Label(login_window,text="Username (e.g., root)", font=("Arial", 12, "bold"),fg="#ffffff", bg="#0f172a").place(x=25,y=110)
usr_name_input = Entry(login_window, font=("Arial", 15), bg="#1e293b", fg="white", bd=0, insertbackground="white", relief="flat").place(x=25,y=145,width=400)

password_label = Label(login_window,text="Password", font=("Arial", 12, "bold"),fg="#ffffff", bg="#0f172a").place(x=25,y=190)
password_label_input = Entry(login_window, font=("Arial", 15), bg="#1e293b", fg="white", bd=0, show="*",insertbackground="white", relief="flat").place(x=25,y=225,width=400)

Button(login_window, text="CONNECT", font=("Arial", 14, "bold"), bg="#0da270", fg="white", padx=10, pady=5, relief="flat", activebackground="#059669", cursor="hand2",command=main_window).place(x=140,y=270)

login_window.mainloop()