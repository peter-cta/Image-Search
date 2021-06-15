def move(delta):
    global current
    if not (0 <= current + delta < len(image_list)):
        tk.tkMessageBox.showinfo('End', 'No more image.')
        return
    current += delta
    image = Image.open(image_list[current]).resize((720,405))
    photo = ImageTk.PhotoImage(image)
    tk.Label(new_windown, image = photo)

def show_result():
    
    new_windown = Toplevel(root)
    current = 0
    label = tk.Label(new_windown, compound=tk.TOP)
    label.pack()

    frame = tk.Frame(new_windown)
    frame.pack()

    
    tk.Button(frame, text='Previous picture', command=lambda: move(-1)).pack(side=tk.LEFT)
    tk.Button(frame, text='Next picture', command=lambda: move(+1)).pack(side=tk.LEFT)
    tk.Button(frame, text='Quit', command=root.quit).pack(side=tk.LEFT)
    move(0)