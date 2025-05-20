import os
import sys
import subprocess
import tkinter as tk

def launch_in_terminal():
    script_path = os.path.abspath(sys.argv[0])
    command = f'"{script_path}" --in-terminal'
    
    #trying launching in gnome-terminal first
    terminal_cmd = ["gnome-terminal", "--", "bash", "-c", f"{command}; exec bash"]
    
    #fallback to lxterminal if GNOME isn't available
    if not subprocess.call(["which", "gnome-terminal"], stdout=subprocess.PIPE, stderr=subprocess.PIPE):
        subprocess.Popen(terminal_cmd)
    else:
        #if gnome-terminal is not found, try lxterminal
        terminal_cmd = ["lxterminal", "-e", f"bash -c '{command}; exec bash'"]
        subprocess.Popen(terminal_cmd)

#only launch terminal on Linux and not already inside one
if sys.platform.startswith("linux") and "--in-terminal" not in sys.argv:
    launch_in_terminal()
    sys.exit(0)

#setup main window
root = tk.Tk()
root.title("Secure File Manager")
root.geometry('400x300')

#title label
title = tk.Label(root, text="Secure File Operations", font=('Segoe UI', 14, 'bold'))
title.pack(pady=(20, 10))

#function to dynamically import and execute a module's main function
def run_module(module_name):
    try:
        module = __import__(module_name)
        if hasattr(module, "main"):
            module.main()  #calls the main function in the module
        else:
            print(f"Module '{module_name}' does not have a main() function.")
    except Exception as e:
        print(f"Error running module '{module_name}': {e}")

#buttons with proper function calls
btn_1 = tk.Button(root, text="Key Exchange", command=lambda: run_module('ecdh_key_ex'), bd=5)
btn_1.pack(pady=5, fill='x', padx=50)

btn_2 = tk.Button(root, text="Encrypt / Decrypt", command=lambda: run_module('enc_dec'), bd=5)
btn_2.pack(pady=5, fill='x', padx=50)

btn_3 = tk.Button(root, text="File Share", command=lambda: run_module('file_share'), bd=5)
btn_3.pack(pady=5, fill='x', padx=50)

btn_4 = tk.Button(root, text="Install Requirements", command=lambda: run_module('requirements_installer'), bd=5)
btn_4.pack(pady=5, fill='x', padx=50)

btn_5 = tk.Button(root, text="Exit", command=root.destroy, bd=5)
btn_5.pack(pady=5, fill='x', padx=50)

root.mainloop()
