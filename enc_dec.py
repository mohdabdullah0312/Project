#importing required modules
import tkinter as tk
from tkinter import END, filedialog as fd, messagebox
from tkinter.messagebox import showinfo
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

# Defining the main application window
root = tk.Tk()
root.title("File Encryption and Decryption")
root.geometry('500x175')

# Function to check if a key is entered
def validate_key():
    key_value = key.get().strip()
    if not key_value:
        messagebox.showerror("Error", "No key provided! Exiting...")
        root.destroy()  # Shut down the program
        return False
    return True

# Function to handle encryption button click
def encrypt1():
    if not validate_key():
        return  # Stop if key is missing
    root.withdraw()  # Hide the main window
    enc1 = tk.Toplevel(root)  # Create encryption window
    enc1.title("Encrypt a File")
    enc1.geometry('300x175')

    def go_back():
        enc1.destroy()
        root.deiconify()

    tk.Label(enc1, text="Encryption window").pack()
    lbl1 = tk.Label(enc1, text="Choose the file to Encrypt", font=('Arial', 13))
    lbl1.pack() # Show the label

    def select_file_enc():
        global fileloc_enc
        filetypes = (
            ('all files', '*.*'),
            ('text files', '*.txt')
        )

        filename = fd.askopenfilename(
            title="Open the file",
            initialdir='C:\\',
            filetypes=filetypes)

        global fileloc_enc
        fileloc_enc = filename

        lbl3=tk.Label(enc1, text='Selected File: '+fileloc_enc, font=('Arial',13))
        lbl3.pack() # Show the label

        def encrypt_file(filename, key):
            # Generate a random nonce (16 bytes)
            cipher = AES.new(key, AES.MODE_GCM)
            nonce = cipher.nonce

            # Read file data
            with open(filename, "rb") as f:
                file_data = f.read()

            # Encrypt data
            ciphertext, tag = cipher.encrypt_and_digest(file_data)

            # Overwrite the original file
            with open(filename, "wb") as f:
                f.write(nonce + tag + ciphertext)

            print(f"🔒 File encrypted: {filename}")
            showinfo("Success", "File encrypted successfully!")

        enc_button = tk.Button(enc1, text='Encrypt', command=lambda: encrypt_file(fileloc_enc, get_key(key.get().strip())))  # Encrypt the file
        enc_button.pack()  # Show the button 


           

    btn_enc = tk.Button(enc1, text='Open the File', command=select_file_enc)
    btn_enc.pack()  # Show the button  

   
    # Example Usage
      


    tk.Button(enc1, text="Back", command=go_back).pack(side='bottom', padx=5, pady=5)



# Function to handle decryption button click
def decrypt1():
    if not validate_key():
        return  # Stop if key is missing
    root.withdraw()  # Hide the main window
    dec1 = tk.Toplevel(root)  # Create decryption window
    dec1.title("Decrypt a File")
    dec1.geometry('300x175')

    tk.Label(dec1, text="Decryption window").pack()


    lbl2=tk.Label(dec1, text="Choose the file to Decrypt", font=('Arial', 13))
    lbl2.pack() # Show the label

    def select_file_dec():
        filetypes = (
            ('text files', '*.txt'),
            ('all files', '*.*')
        )

        filename = fd.askopenfilename(
            title="Open the file",
            initialdir='C:\\',
            filetypes=filetypes)

        global fileloc_dec
        fileloc_dec = filename

        lbl4=tk.Label(dec1, text='Selected File: '+fileloc_dec, font=('Arial',13))
        lbl4.pack()

        def decrypt_file(filename, key):
            # Read encrypted file
            with open(filename, "rb") as f:
                file_data = f.read()

            # Extract nonce, tag, and ciphertext
            nonce = file_data[:16]
            tag = file_data[16:32]
            ciphertext = file_data[32:]

            # Decrypt
            cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
            decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)

            # Overwrite with decrypted data
            with open(filename, "wb") as f:
                f.write(decrypted_data)

            print(f"🔓 File decrypted: {filename}")
            showinfo("Success", "File decrypted successfully!")

        dec_button = tk.Button(dec1, text='Decrypt',command=lambda: decrypt_file(fileloc_dec, get_key(key.get().strip())))  # Decrypt the file
        dec_button.pack()  # Show the button 


    btn_dec = tk.Button(dec1, text='Open the File', command=select_file_dec)
    btn_dec.pack()  # Show the button

    def go_back():
        dec1.destroy()
        root.deiconify()

    tk.Button(dec1, text="Back", command=go_back).pack(side='bottom', padx=5, pady=5)

# Frame for entering key
frame_key = tk.Frame(root)
frame_key.pack()

key = tk.Entry(frame_key, bd='3', width='50')
key.pack(side='left')

paste_btn = tk.Button(frame_key, text='Paste', bd='3', command=lambda: key.insert(END, root.clipboard_get()))
paste_btn.pack(side='left', padx=5)

def get_key(key):
    #Convert user input into a 32-byte AES key using SHA-256
    hasher = SHA256.new(key.encode('utf-8'))
    return hasher.digest()  # Returns 32 bytes

# Buttons for encryption and decryption
btn1 = tk.Button(root, text='Encrypt a File', bd='3', font=('Arial'), command=encrypt1)
btn1.pack(side='top', padx=5, pady=5)

btn2 = tk.Button(root, text='Decrypt a File', bd='3', font=('Arial'), command=decrypt1)
btn2.pack(side='top', padx=5, pady=5)

# Start the main event loop
root.mainloop()
