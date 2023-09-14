import psutil
import tkinter as tk

def kill_process():
    selection = process_listbox.curselection()
    if selection:
        pid = int(process_listbox.get(selection[0]).split()[0])
        p = psutil.Process(pid)
        p.terminate()
        update_process_list()

def update_cpu_usage():
    cpu_percent = psutil.cpu_percent()
    cpu_label.config(text="CPU Usage: {}%".format(cpu_percent))
    cpu_label.after(1000, update_cpu_usage)

def update_process_list():
    process_listbox.delete(0, tk.END)
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        try:
            pid, name, username = proc.info['pid'], proc.info['name'], proc.info['username']
            process_listbox.insert(tk.END, "{} {} {}".format(pid, name, username))
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

root = tk.Tk()
root.title("Task Manager")

# CPU usage label
cpu_label = tk.Label(root, text="CPU Usage: ")
cpu_label.pack()

# Process listbox
process_frame = tk.Frame(root)
process_frame.pack()
process_label = tk.Label(process_frame, text="Processes")
process_label.pack(side=tk.TOP)
process_listbox = tk.Listbox(process_frame, width=50)
process_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
process_scrollbar = tk.Scrollbar(process_frame, orient=tk.VERTICAL, command=process_listbox.yview)
process_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
process_listbox.config(yscrollcommand=process_scrollbar.set)

# Kill button
kill_button = tk.Button(root, text="Kill", command=kill_process)
kill_button.pack()

# Update CPU usage and process list every second
update_cpu_usage()
update_process_list()

root.mainloop()
