import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font
import threading



def main() :
    
    status = False
    
    try :
        #window setup
        window = tk.Tk()
        window.geometry("600x400") 
        window.title("Translation stage control 2024 V.0.1")
        
        bg = PhotoImage(file = 'C://Users//Asus//Desktop//INTERNSHIP_PROGRAM//BG_UI.png')
        canvas1 = Canvas( window, width = 600, height = 400)  
        canvas1.pack(fill = "both", expand = True) 
        canvas1.create_image( 0, 0, image = bg,anchor = "nw") 

        rectangle = canvas1.create_rectangle(50, 90, 350, 140, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)
        rectangle = canvas1.create_rectangle(50, 150, 350, 200, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)
        rectangle = canvas1.create_rectangle(50, 210, 350, 260, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)
        rectangle = canvas1.create_rectangle(50, 270, 350, 320, outline = "gray89", fill = "gray89") #(x1,y1,x2,y2)

        # Title
        title_label_kp = ttk.Label(master=window, text='KP', background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_kp.place(x = 60 , y = 90)
        title_label_ki = ttk.Label(master=window, text='KI',background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_ki.place(x = 60 , y = 150)
        title_label_kd = ttk.Label(master=window, text='KD',background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_kd.place(x = 60 , y = 210)
        title_label_pos = ttk.Label(master=window, text='FIRST POSITION',background ="gray89", font='CenturyGothic 10 bold' , foreground ="gray")
        title_label_pos.place(x = 60 , y = 270)

        # Input field
        entry_kp = ttk.Entry(master=window , background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center")
        entry_kp.place(x = 60 , y = 105 , width= 280, height=30)
        entry_ki = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center" )
        entry_ki.place(x = 60 , y = 165, width= 280, height=30)
        entry_kd = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center")
        entry_kd.place(x = 60 , y = 225 , width= 280, height=30)
        entry_pos = ttk.Entry(master=window, background = "lightsteelblue4", foreground ="dodgerblue4" , justify= "center" )
        entry_pos.place(x = 60 , y = 285 , width= 280, height=30)
        
        
        def stop() :
            global status
            status = True
            print("stop")
            
        def default() :
            global status 
            status = False
            while(status == False) :
                print("default")
                
        def default_app() :
            t = threading.Thread(target=default)
            t.start()          
                            
        def enter():
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
        
        def  start() :
            global status 
            status = False
            while(status == False) :
                print("start")
            
        def start_app() :
            t = threading.Thread(target=start)
            t.start()
                
            
        # Button
        
        button = tk.Button(master=window, text="DEFAULT", 
                        command=default_app,
                        activebackground="dodgerblue4", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="slategray3",
                        cursor="hand2",
                        disabledforeground="lightsteelblue1",
                        fg="black",
                        font=("CenturyGothic", 12),
                        height=1,
                        highlightbackground="white",
                        highlightcolor="lightgray",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100 )
        button.place(x = 400 , y = 100)
        
        button = tk.Button(master=window, text="ENTER", 
                        command=enter,
                        activebackground="dodgerblue4", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="slategray3",
                        cursor="hand2",
                        disabledforeground="lightsteelblue1",
                        fg="black",
                        font=("CenturyGothic", 12),
                        height=1,
                        highlightbackground="white",
                        highlightcolor="lightgray",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100 )
        button.place(x = 400 , y = 150)

        button = tk.Button(master=window, text="START", 
                        command=start_app,
                        activebackground="dodgerblue4", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="slategray3",
                        cursor="hand2",
                        disabledforeground="lightsteelblue1",
                        fg="black",
                        font=("CenturyGothic", 12),
                        height=1,
                        highlightbackground="white",
                        highlightcolor="lightgray",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100 )
        button.place(x = 400 , y = 200)

        button = tk.Button(master=window, text="STOP", 
                        command=stop,
                        activebackground="dodgerblue4", 
                        activeforeground="white",
                        anchor="center",
                        bd=3,
                        bg="slategray3",
                        cursor="hand2",
                        disabledforeground="lightsteelblue1",
                        fg="black",
                        font=("CenturyGothic", 12),
                        height=1,
                        highlightbackground="white",
                        highlightcolor="lightgray",
                        highlightthickness=2,
                        justify="center",
                        overrelief="raised",
                        padx=10,
                        pady=5,
                        width=15,
                        wraplength=100 )
        button.place(x = 400 , y = 250)
        
        # Run the application
        window.mainloop()
        
    except Exception as e:
        print("ERROR:", e)
        
if __name__ == "__main__":
    main()   