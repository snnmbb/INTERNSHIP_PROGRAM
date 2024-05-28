import tkinter as tk

def on_entry_click(event):
   if entry.get() == "KP...":
      entry.delete(0, tk.END)
      entry.configure(foreground="black")

def on_focus_out(event):
   if entry.get() == "":
      entry.insert(0, "KP...")
      entry.configure(foreground="gray")

root = tk.Tk()
entry = tk.Entry(root, foreground="gray")
entry.insert(0, "KP...")

entry.bind("<FocusIn>", on_entry_click)
entry.bind("<FocusOut>", on_focus_out)
entry.pack()

root.mainloop()