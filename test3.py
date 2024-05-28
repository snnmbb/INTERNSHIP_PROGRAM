from tkinter import *

# Create an instance of tkinter frame
win= Tk()

# Set the size of the Tkinter window
win.geometry("700x350")

# Define a function to print something inside infinite loop
run= True

def print_hello():
   if run:
      Label(win, text="Hello World", font= ('Helvetica 10 bold')).pack()
   # After 1 sec call the print_hello() again
   win.after(1000, print_hello)
def start():
   global run
   run= True

def stop():
   global run
   run= False

# Create buttons to trigger the starting and ending of the loop
start= Button(win, text= "Start", command= start)
start.pack(padx= 10)
stop= Button(win, text= "Stop", command= stop)
stop.pack(padx= 15)

# Call the print_hello() function after 1 sec.
win.after(1000, print_hello)
win.mainloop()