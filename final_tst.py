import tkinter as tk

# Setup main window
root = tk.Tk()
root.title("Secure File Manager")
root.geometry('400x250')

# Title label
title = tk.Label(root, text="Secure File Operations", font=('Segoe UI', 14, 'bold'))
title.pack(pady=(20, 10))

# Buttons with spacing
btn_1 = tk.Button(root, text="Key Exchange", command=lambda: __import__('ecdh_key_ex').__call__(), bd=5)
btn_1.pack(pady=5, fill='x', padx=50)

btn_2 = tk.Button(root, text="Encrypt / Decrypt", command=lambda: __import__('enc_dec').__call__(), bd=5)
btn_2.pack(pady=5, fill='x', padx=50)

btn_3 = tk.Button(root, text="File Share", command=lambda: __import__('file_share').__call__(), bd=5)
btn_3.pack(pady=5, fill='x', padx=50)

btn_4 = tk.Button(root, text="Exit", command=root.destroy, bd=5)
btn_4.pack(pady=5, fill='x', padx=50)

root.mainloop()



