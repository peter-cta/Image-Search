from os import path
from tkinter.constants import NO, NONE
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import Toplevel, filedialog
import UseHistogram


IMAGE_PATH = 'icons/eiffle.jpg'
WIDTH, HEIGTH = 720, 405

root = tk.Tk()
root.title('Image Search')
root.geometry('{}x{}'.format(WIDTH, HEIGTH))

canvas = tk.Canvas(root, width=WIDTH, height=HEIGTH)
canvas.pack()

# Hàm Upload File và hiển thị đường dẫn 
filename = ''
def UploadAction(event=None):
    canvas.delete('path')
    global filename
    filename = filedialog.askopenfilename()
    canvas.create_text(350, 165, text=filename, anchor='w', tag='path', fill="#515486",font=("Arial-BoldMT",int(11.0)))

#Trích xuất đặc trưng và tìm kiếm
image_list = []
def Search_implement():
    global image_list
    UseHistogram.features_extract('data.csv','dataset')
    UseHistogram.search(filename,'data.csv')


# Xử lý giao diện

img = ImageTk.PhotoImage(Image.open(IMAGE_PATH).resize((WIDTH, HEIGTH), Image.ANTIALIAS))
imglogo = ImageTk.PhotoImage(Image.open('icons/gogo.png'))
imgTextBox = ImageTk.PhotoImage(Image.open('icons/textBox.png').resize((345,30), Image.ANTIALIAS))
imgSearch = ImageTk.PhotoImage(Image.open('icons/search.png').resize((25,25), Image.ANTIALIAS))
imgUpload = ImageTk.PhotoImage(Image.open('icons/camera.png').resize((28,22), Image.ANTIALIAS))

canvas.background = img  
bg = canvas.create_image(0, 0, anchor=tk.NW, image=img)


button = tk.Button(root, image=imgSearch, borderwidth=0, command=Search_implement)
button_window = canvas.create_window(670, 152, anchor=tk.NW, window=button)

button_upload = tk.Button(root, image=imgUpload, borderwidth=0, bd=0,bg="#F6F7F9",command=UploadAction)
button_upload_window = canvas.create_window(620, 152, anchor=tk.NW, window=button_upload)

canvas.create_image(350, 10, anchor=tk.NW, image=imglogo)
canvas.create_image(320, 150, anchor=tk.NW, image=imgTextBox)


root.mainloop()