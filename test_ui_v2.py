import time
import threading
from tkinter import * 
root = Tk()
root.title("Loop Terminate")

time.sleep(0.5)

stop = False

def button_stop_command():
  # If the STOP button is pressed then terminate the loop
  global stop
  stop = True

def button_start_command():
  global stop
  stop = False
  j = 1
  while j <= 20 and not stop:
    print("Loop Index = " + str(j))
    time.sleep(0.1)
    j = j+1

def button_starter():
  t = threading.Thread(target=button_start_command)
  t.start()

# Button START
button_start = Button(root, text="START", padx=30, pady=20, command=button_starter)
button_start.grid(columnspan=1, row=1,column=0)

# Button STOP
button_stop = Button(root, text="STOP", padx=33, pady=20, command=button_stop_command)
button_stop.grid(row=2, column=0)

root.mainloop()