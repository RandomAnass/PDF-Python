# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 02:15:40 2021

@author: anass
"""
from Functions import get_info ,  extract_text , extract_table , extract_table_tabula , extract_links, extract_images
from PyPDF2 import PdfFileReader
import tkinter.filedialog
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pathlib import Path
import os
from webbrowser import open_new

def display1():
    messagebox.showinfo("Xiith.com", "You clicked 1")

global filepathforinfo


# on a button click
def Open_Information_Window():
    filetypes=[('PDF files', '*.pdf')]
    filepathforinfo = tk.filedialog.askopenfilename(  title='Open a file to extract information from',initialdir='/', filetypes=filetypes)
    Info_list=get_info(filepathforinfo)
    
    style = ttk.Style()
    style.theme_use('alt')
    #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

	# be treated as a new window
    Information_Window = tk.Toplevel(main_window)
    Information_Window.title("PDF-functions             Information extracted from : " +Path(filepathforinfo).stem+".pdf")
    Information_Window.resizable(True, True)
    Information_Window['background']='#8c52ff'
    Information_Window.iconbitmap('icon.ico')
    #info_button = tk.Button(Information_Window, text="Give the pdf file to extract information from", activebackground='purple',activeforeground='purple' ,command=get_pdf_file)
    #info_button.grid(row=0,column=0)
    # Add a Treeview widget
    tree = tk.ttk.Treeview(Information_Window, column=("Title" , "Number of pages", "Author", "Creator","Producer","Subject"), show='headings', height=5)
    tree.column("# 1", anchor=tk.CENTER)
    tree.heading("# 1", text="Title")
    tree.column("# 2", anchor=tk.CENTER)
    tree.heading("# 2", text="Number of pages")
    tree.column("# 3", anchor=tk.CENTER)
    tree.heading("# 3", text="Author")
    tree.column("# 4", anchor=tk.CENTER)
    tree.heading("# 4", text="Creator")
    tree.column("# 5", anchor=tk.CENTER)
    tree.heading("# 5", text="Producer")
    tree.column("# 6", anchor=tk.CENTER)
    tree.heading("# 6", text="Subject")
    
    # Insert the data in Treeview widget
    tree.insert('', 'end', text="1", values=(Info_list[5], Info_list[0], Info_list[1],Info_list[2],Info_list[3],Info_list[4]))

    tree.pack()
    #get_pdf_info(filepathforinfo)
    


    tk.Label(Information_Window, text ="Information extraction")

# on a button click
def Open_Text_Window():
    def open_file():
        """Open a file for editing."""
        filepath = tk.filedialog.askopenfilename(title='Open a file to extract text from',
            filetypes=[('PDF files', '*.pdf'),("Text Files", "*.txt"),("All Files", "*.*")]
        )
        if not filepath:
            return
        txt_edit.delete(1.0, tk.END)
        if os.path.splitext(str(filepath))[-1].lower() == '.pdf'  :
             text = extract_text(filepath)
             txt_edit.insert(tk.END, text)
        else:
            with open(filepath, "r") as input_file:
                text = input_file.read()
                txt_edit.insert(tk.END, text)
        Text_Window.title(f"Text Editor Application - {filepath}")
        Text_Window.lift()
        #or Text_Window.attributes("-topmost", True)
    def save_file():
        """Save the current file as a new file."""
        filepath = tk.filedialog.asksaveasfilename(
            defaultextension="txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = txt_edit.get(1.0, tk.END)
        
            output_file.write(text)
        Text_Window.title(f"Text Editor Application - {filepath}")
    #filetypes=[('PDF files', '*.pdf')]
    #filepathforinfo = tk.filedialog.askopenfilename(  title='Open a file to extract text from',initialdir='/', filetypes=filetypes)
    #text=get_info(filepathforinfo)
    
    style = ttk.Style()
    style.theme_use('alt')
    #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')

	# be treated as a new window
    Text_Window = tk.Toplevel(main_window)
    
    #Text_Window.title("PDF-functions             Information extracted from : " +Path(filepathforinfo).stem+".pdf")
    Text_Window.resizable(True, True)
    Text_Window['background']='#8c52ff'
    Text_Window.iconbitmap('icon.ico')
   
    
    #info_button = tk.Button(Information_Window, text="Give the pdf file to extract information from", activebackground='purple',activeforeground='purple' ,command=get_pdf_file)
    #info_button.grid(row=0,column=0)
   
    tk.Label(Text_Window, text ="Text extraction")
    
  
    
    Text_Window.rowconfigure(0, minsize=900, weight=1)
    Text_Window.columnconfigure(1, minsize=900, weight=1)
    
    
    txt_edit = tk.Text(Text_Window)
    fr_buttons = tk.Frame(Text_Window,bg='purple', relief=tk.RAISED, bd=2)
    btn_open = tk.Button(fr_buttons, text="Open", command=open_file)
    btn_save = tk.Button(fr_buttons, text="Save As...", command=save_file)
    
    btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
    btn_save.grid(row=1, column=0, sticky="ew", padx=5)
    
    fr_buttons.grid(row=0, column=0, sticky="ns")
    txt_edit.grid(row=0, column=1, sticky="nsew")
    scrollb =  tk.Scrollbar(Text_Window, orient="vertical", command = txt_edit.yview)
    txt_edit['yscrollcommand'] = scrollb.set
    scrollb.grid(row=0, column=2, sticky='nsew') #sticky='ns'
    scrollb.config( command = txt_edit.yview )  

# on a button click
def Open_tables_Window():
    """dont show the buttons if cancelled"""
    filetypes=[('PDF files', '*.pdf')]
    global filepathfortables
    filepathfortables = tk.filedialog.askopenfilename(  title='Open a file to extract tables from',initialdir='/', filetypes=filetypes)
    
    #Info_list=get_info(filepathforinfo)
    def fast_extraction():
        extract_table_tabula(filepathfortables)    
        messagebox.showinfo("Tables extracted successfully", "Extracted Tables are saved in : " + os.path.splitext(filepathfortables)[0] +".xlsx")
    
    
    def advanced_options_extraction():
        """there is a problem with messagebox for long  textes"""
        #messagebox.showinfo("Xiith.com", "You clicked 4")
        
        pdf = PdfFileReader(filepathfortables)
        
        
        WIDTH, HEIGHT = 300, 300
        img13 = Image.open("button13.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        click_btn13= ImageTk.PhotoImage(img13)
        
        img14 = Image.open("button14.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        click_btn14= ImageTk.PhotoImage(img14)

        frame1 = tk.Label(Tables_Window,width=300, bg='#8c52ff')
       
        frame1.grid(row=2,column=2)
        frame2 = tk.LabelFrame(frame1,bg='#ae85ff',  width=300 , text='Save the tables as :                                       ')

        def selection():
            choice = var.get()
            #[json, xlsx, html, markdown, sqlite]
            if choice == 1:
                options = 'xlsx'
            elif choice == 2:
                options = 'csv'
            elif choice == 3:
                options = 'markdown'
            elif choice == 4:
                options = 'sqlite'
            elif choice == 5:
                options = 'json'
            elif choice == 6:
                options = 'html'
            elif choice == 7:
                options = 'compressed'
            return options

        def submit():
            try:
                m = selection()
                if(pdf.isEncrypted):
                    password = passwooord.get()
                else :
                    password = None   
                the_pages ='all'
                if CheckVar1.get() == 1 :
                    pages =  getpages.get()
                    try :
                        #pages =[int(i) for i in pages.split(',')]
                        the_pages = pages
                    except : 
                        the_pages ='all'
                 
                if CheckVar2.get() == 1:
                    printing= True
                    text = extract_table(filepathfortables,options=m,printing=printing,the_password=password,the_pages=the_pages)
                    messagebox.showinfo("Extraction report", text)
                else :
                    printing = False
                    extract_table(filepathfortables,options=m,printing=printing,the_password=password,the_pages=the_pages)
                    messagebox.showinfo("Tables extracted successfully", "Extracted Tables are saved in : " + os.path.splitext(filepathfortables)[0] +"."+m)
    

            except Exception :
                return messagebox.showwarning('Tables extraction', 'Please provide valid input')
        

        var = tk.IntVar()
    
        passwooord = tk.StringVar()
        getpages = tk.StringVar()  

        if(pdf.isEncrypted):
            tk.Label(frame1, text='The pdf is encrypted',bg='#8c52ff').grid(row=0, column=0, padx=5, pady=5)
            tk.Label(frame1,text="Enter the Password :",bg='#8c52ff', font='Helvetica').grid(row=1, column=0, padx=5, pady=5)
            tk.Entry(frame1, show="*",textvariable=passwooord , width=37).grid(row=2, column=0) #
        def activateCheck():
            if CheckVar1.get() == 1:          #whenever checked
                e.config(state= tk.NORMAL)
                l.config(state= tk.NORMAL)
            elif CheckVar1.get() == 0:        #whenever unchecked
                e.config(state= tk.DISABLED)
                l.config(state= tk.DISABLED)
        CheckVar1 = tk.IntVar()


        tk.Checkbutton(frame1, text = "select specific pages \n (all by default - If not clicked)",bg='#8c52ff',activebackground='#8c52ff', variable = CheckVar1, onvalue = 1, offvalue = 0,command=activateCheck).grid(row=3, column=0)


        l = tk.Label( frame1, text = "Give the list of pages you want to extract from:" +'\n'+"In this form : 1, 5, 6 ,...",bg='#8c52ff')
        l.grid( row=4, column=0 )
        e = tk.Entry( frame1, textvariable = getpages, width=37)
        e.grid( row=5, column=0 )
        e.config(state= tk.DISABLED)
        l.config(state= tk.DISABLED)
        CheckVar2 = tk.IntVar()
        tk.Checkbutton(frame1, text = "Get Extraction report",bg='#8c52ff',activebackground='#8c52ff', variable = CheckVar2, onvalue = 1, offvalue = 0).grid(row=6, column=0)
        tk.Radiobutton(frame2, text='Excel', bg='#ae85ff',  activebackground='#ae85ff', variable=var, value=1,command=selection).pack()
        tk.Radiobutton(frame2, text='CSV',bg='#ae85ff',  activebackground='#ae85ff', variable=var, value=2,command=selection).pack()#anchor=tk.W
        tk.Radiobutton(frame2, text='Markdown', bg='#ae85ff',  activebackground='#ae85ff',variable=var, value=3,command=selection).pack()
        tk.Radiobutton(frame2, text='Sqlite',bg='#ae85ff',  activebackground='#ae85ff', variable=var, value=4,command=selection).pack()
        tk.Radiobutton(frame2, text='JSON', bg='#ae85ff',  activebackground='#ae85ff',variable=var, value=5,command=selection).pack()
        tk.Radiobutton(frame2, text='Html',bg='#ae85ff',  activebackground='#ae85ff', variable=var, value=6,command=selection).pack()
        tk.Radiobutton(frame2, text='Compressed csv',bg='#ae85ff',  activebackground='#ae85ff' ,variable=var, value=7,command=selection).pack()
        #tk.Radiobutton(frame2, text='Male', variable=var, value=2,command=selection).pack()
        #tk.Radiobutton(frame2, text='Others', variable=var, value=3,command=selection).pack()

        frame2.grid(row=8, columnspan=3)
      
        imgsubmit = Image.open("submit.PNG").resize((150, 50), Image.ANTIALIAS)
        click_btnsubmit= ImageTk.PhotoImage(imgsubmit)
     
        
        
        
        #change cursors

       
        submit_btn = tk.Button(frame1, text="Submit",image=click_btnsubmit, command=submit)
        submit_btn.image = click_btnsubmit#
        submit_btn.grid(row=9, columnspan=4)

        
        
        
        
    if filepathfortables:
        style = ttk.Style()
        style.theme_use('alt')
        #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    
    	# be treated as a new window
        Tables_Window = tk.Toplevel(main_window)
        Tables_Window.attributes("-topmost", True)
        Tables_Window.title("PDF-functions             Tables extracted from : " +Path(filepathfortables).stem+".pdf")
        Tables_Window.resizable(True, True)
        Tables_Window['background']='#8c52ff'
        Tables_Window.iconbitmap('icon.ico')
        #info_button = tk.Button(Information_Window, text="Give the pdf file to extract information from", activebackground='purple',activeforeground='purple' ,command=get_pdf_file)
        #info_button.grid(row=0,column=0)
        WIDTH, HEIGHT = 300, 300
        img13 = Image.open("button13.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        click_btn13= ImageTk.PhotoImage(img13)
        
        img14 = Image.open("button14.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
        click_btn14= ImageTk.PhotoImage(img14)
    
        b13 = tk.Button(Tables_Window, text="Fast Extraction",image=click_btn13,  command=fast_extraction)
        b13.image = click_btn13#
        b13.grid(row=0,column=0)
        b14 = tk.Button(Tables_Window, text="Advanced Options",image=click_btn14,  command=advanced_options_extraction) #
        b14.image = click_btn14#
        b14.grid(row=0,column=2)
    
        
       
        #get_pdf_info(filepathforinfo)
        
    
    
        tk.Label(Tables_Window, text ="Tables extraction")
        
    
def Open_Links_Window():
    filetypes=[('PDF files', '*.pdf')]
    pdfpath = tk.filedialog.askopenfilename(  title='Open a file to extract information from',initialdir='/', filetypes=filetypes)
    urls_extraction = extract_links(pdfpath)
    def callback(url):
        open_new(url)

    
    
    if len(urls_extraction)==0 :
        messagebox.showinfo('Links extraction', "No link was found in this pdf")
    else :
        style = ttk.Style()
        style.theme_use('alt')
        #('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative')
    
    	# be treated as a new window
        Links_Window = tk.Toplevel(main_window)
        Links_Window.title("PDF-functions             Links extracted from : " +Path(pdfpath).stem+".pdf")
        Links_Window.resizable(True, True)
        Links_Window['background']='#ffde59'
        Links_Window.iconbitmap('icon.ico')
        
        s = ttk.Style()
        s.configure('TFrame', background='#ffde59')
        s.configure('Frame1.TFrame', background='#ffde59')
        container = ttk.Frame(Links_Window,  style='Frame1.TFrame')

        container.pack( expand=True,fill =tk.BOTH )
        canvas = tk.Canvas(container)
        canvas.configure(bg='#ffde59')
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas,  style='Frame1.TFrame')
        scrollable_frame.pack(anchor=tk.CENTER)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor=tk.CENTER)
        
        canvas.configure(yscrollcommand=scrollbar.set)
        


        for a_link in list(set(urls_extraction)) :
    
            link = tk.Label(scrollable_frame, text=str(a_link),font='Helveticabold', fg="blue", cursor="hand2", bg='#ffde59')
            link.pack()
            link.bind("<Button-1>",lambda e: callback(a_link))


        container.pack(anchor=tk.CENTER)
        canvas.pack(side="left", anchor=tk.CENTER,fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
     

    
        tk.Label(Links_Window, text ="Links extraction")
 
    #get_pdf_info(filepathforinfo)

    

# on a button click
def Open_images_Window():
    """dont show the buttons if cancelled"""
    filetypes=[('PDF files', '*.pdf')]

    filepath = tk.filedialog.askopenfilename(  title='Open a file to extract Images from',initialdir='/', filetypes=filetypes)

    text = extract_images(filepath)    
    messagebox.showinfo("Images extracted successfully \n", text + "Extracted Images are saved in : " + os.path.dirname(filepath) )




   
def display2():
    messagebox.showinfo("Xiith.com", "You clicked 2")


def display3():
    messagebox.showinfo("Xiith.com", "You clicked 3")


def display4():
    messagebox.showinfo("Xiith.com", "You clicked 4")





main_window = tk.Tk()
main_window.title('PDF-functions')
main_window.resizable(True, True)
main_window['background']='#8c52ff'
main_window.iconbitmap('icon.ico')
#main_window.geometry("600x500")



#Import the image using PhotoImage function
#Let us create a label for button event

WIDTH, HEIGHT = 300, 300
img1 = Image.open("button1.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn1 = ImageTk.PhotoImage(img1)
img_label1= tk.Label(image=click_btn1)

img2 = Image.open("button2.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn2= ImageTk.PhotoImage(img2)
img_label2= tk.Label(image=click_btn2)

img3 = Image.open("button3.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn3= ImageTk.PhotoImage(img3)
img_label3= tk.Label(image=click_btn3)

img4 = Image.open("button4.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn4= ImageTk.PhotoImage(img4)
img_label4= tk.Label(image=click_btn4)

img5 = Image.open("button5.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn5= ImageTk.PhotoImage(img5)
img_label5= tk.Label(image=click_btn5)

img6 = Image.open("button6.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn6= ImageTk.PhotoImage(img6)
img_label6= tk.Label(image=click_btn6)

img7 = Image.open("button7.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn7= ImageTk.PhotoImage(img7)
img_label7= tk.Label(image=click_btn7)

img8 = Image.open("button8.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn8= ImageTk.PhotoImage(img8)
img_label8= tk.Label(image=click_btn8)

img9 = Image.open("button9.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn9= ImageTk.PhotoImage(img9)
img_label9= tk.Label(image=click_btn9)

img10 = Image.open("button10.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn10= ImageTk.PhotoImage(img10)
img_label10= tk.Label(image=click_btn10)

img11 = Image.open("button11.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn11= ImageTk.PhotoImage(img11)
img_label1= tk.Label(image=click_btn11)

img12 = Image.open("button12.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn12= ImageTk.PhotoImage(img12)
img_label2= tk.Label(image=click_btn12)



#change cursors
b1 = tk.Button(main_window, text="Information extraction",cursor='plus' , image=click_btn1,command=Open_Information_Window)
b1.grid(row=1,column=0)
b2 = tk.Button(main_window, text="Text extraction",image=click_btn2, command=Open_Text_Window)
b2.grid(row=1,column=2)
b3 = tk.Button(main_window, text="Tables extraction",image=click_btn3, command=Open_tables_Window)
b3.grid(row=1,column=4)
b4 = tk.Button(main_window, text="Links extraction",image=click_btn4, command=Open_Links_Window)
b4.grid(row=1,column=6)
b5 = tk.Button(main_window, text="Watermark",image=click_btn5, command=display1)
b5.grid(row=3,column=0)
b6 = tk.Button(main_window, text="Merge",image=click_btn6, command=display2)
b6.grid(row=3,column=2)
b7 = tk.Button(main_window, text="Split",image=click_btn7, command=display3)
b7.grid(row=3,column=4)
b8 = tk.Button(main_window, text="Images extraction",image=click_btn8, command=Open_images_Window)
b8.grid(row=3,column=6)
b9 = tk.Button(main_window, text="Encryption",image=click_btn9, command=display1)
b9.grid(row=5,column=0)
b10 = tk.Button(main_window, text="Decryption",image=click_btn10, command=display2)
b10.grid(row=5,column=2)
b11 = tk.Button(main_window, text="Advanced OCR",image=click_btn11,  command=display3)
b11.grid(row=5,column=4)
b12 = tk.Button(main_window, text="Conversions",image=click_btn12,  command=display4)
b12.grid(row=5,column=6)

#b13 = Button(tk, text="Duplicate detection",image=click_btn11, command=display3).place(x=500, y=300)

main_window.mainloop()

############################################################################################

