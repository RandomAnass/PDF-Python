# -*- coding: utf-8 -*-
"""
Created on Fri Aug 20 02:15:40 2021

@author: anass
"""
#from Functions import *
from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageTk

def display1():
    messagebox.showinfo("Xiith.com", "You clicked 1")


def display2():
    messagebox.showinfo("Xiith.com", "You clicked 2")


def display3():
    messagebox.showinfo("Xiith.com", "You clicked 3")


def display4():
    messagebox.showinfo("Xiith.com", "You clicked 4")

"button1.png"




tk = Tk()
tk.title('PDF-functions')
tk.resizable(True, True)
tk['background']='#8c52ff'
tk.iconbitmap('icon.ico')
#tk.geometry("600x500")



#Import the image using PhotoImage function
#Let us create a label for button event

WIDTH, HEIGHT = 300, 300
img1 = Image.open("button1.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn1 = ImageTk.PhotoImage(img1)
img_label1= Label(image=click_btn1)

img2 = Image.open("button2.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn2= ImageTk.PhotoImage(img2)
img_label2= Label(image=click_btn2)

img3 = Image.open("button3.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn3= ImageTk.PhotoImage(img3)
img_label3= Label(image=click_btn3)

img4 = Image.open("button4.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn4= ImageTk.PhotoImage(img4)
img_label4= Label(image=click_btn4)

img5 = Image.open("button5.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn5= ImageTk.PhotoImage(img5)
img_label5= Label(image=click_btn5)

img6 = Image.open("button6.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn6= ImageTk.PhotoImage(img6)
img_label6= Label(image=click_btn6)

img7 = Image.open("button7.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn7= ImageTk.PhotoImage(img7)
img_label7= Label(image=click_btn7)

img8 = Image.open("button8.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn8= ImageTk.PhotoImage(img8)
img_label8= Label(image=click_btn8)

img9 = Image.open("button9.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn9= ImageTk.PhotoImage(img9)
img_label9= Label(image=click_btn9)

img10 = Image.open("button10.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn10= ImageTk.PhotoImage(img10)
img_label10= Label(image=click_btn10)

img11 = Image.open("button11.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn11= ImageTk.PhotoImage(img11)
img_label1= Label(image=click_btn11)

img12 = Image.open("button12.png").resize((WIDTH, HEIGHT), Image.ANTIALIAS)
click_btn12= ImageTk.PhotoImage(img12)
img_label2= Label(image=click_btn12)




b1 = Button(tk, text="Information extraction", image=click_btn1, command=display1)
b1.grid(row=1,column=0)
b2 = Button(tk, text="Text extraction",image=click_btn2, command=display2)
b2.grid(row=1,column=2)
b3 = Button(tk, text="Tables extraction",image=click_btn3, command=display3)
b3.grid(row=1,column=4)
b4 = Button(tk, text="Links extraction",image=click_btn4, command=display4)
b4.grid(row=1,column=6)
b5 = Button(tk, text="Watermark",image=click_btn5, command=display1)
b5.grid(row=3,column=0)
b6 = Button(tk, text="Merge",image=click_btn6, command=display2)
b6.grid(row=3,column=2)
b7 = Button(tk, text="Split",image=click_btn7, command=display3)
b7.grid(row=3,column=4)
b8 = Button(tk, text="Images extraction",image=click_btn8, command=display4)
b8.grid(row=3,column=6)
b9 = Button(tk, text="Encryption",image=click_btn9, command=display1)
b9.grid(row=5,column=0)
b10 = Button(tk, text="Decryption",image=click_btn10, command=display2)
b10.grid(row=5,column=2)
b11 = Button(tk, text="Advanced OCR",image=click_btn11,  command=display3)
b11.grid(row=5,column=4)
b12 = Button(tk, text="Conversions",image=click_btn12,  command=display4)
b12.grid(row=5,column=6)

#b13 = Button(tk, text="Duplicate detection",image=click_btn11, command=display3).place(x=500, y=300)

tk.mainloop()
