import tkinter as tk
from tkinter import ttk




# Window setting
window = tk.Tk()
window.title('PID TUNING')
window.geometry('600x400')

# Title
title_label_kp = ttk.Label(master=window, text='Kp = ', font='Calibri 12')
title_label_kp.place(x = 50 , y = 100)
title_label_ki = ttk.Label(master=window, text='Ki = ', font='Calibri 12')
title_label_ki.place(x = 50 , y = 150)
title_label_kd = ttk.Label(master=window, text='Kd = ', font='Calibri 12')
title_label_kd.place(x = 50 , y = 200)
title_label_pos = ttk.Label(master=window, text='First Position = ', font='Calibri 12')
title_label_pos.place(x = 50 , y = 250)

# Input field
entry_kp = ttk.Entry(master=window)
entry_kp.place(x = 150 , y = 100)
entry_ki = ttk.Entry(master=window)
entry_ki.place(x = 150 , y = 150)
entry_kd = ttk.Entry(master=window)
entry_kd.place(x = 150 , y = 200)
entry_pos = ttk.Entry(master=window)
entry_pos.place(x = 150 , y = 250)

def button_func():
    global KP
    global KI
    global KD
    global POS
    KP = entry_kp.get()
    KI  = entry_ki.get()
    KD = entry_kd.get()
    POS = entry_pos.get()
    print("Kp : " + entry_kp.get())
    print("Ki : " + entry_ki.get())
    print("Kd : " + entry_kd.get())
    print("First Position : " + entry_pos.get())
    
# Button
button = ttk.Button(master=window, text='Enter', command=button_func)
button.place(x = 400 , y = 100)

# Run the application
window.mainloop()

print(KP)
print(KI)
print(KD)
print(POS)