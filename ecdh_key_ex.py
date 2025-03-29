#importing required modules here
import tkinter as tk
from ecdsa import SigningKey, SECP256k1, VerifyingKey
from hashlib import sha256
from ecdsa.ellipticcurve import Point

#the main window opens here
root = tk.Tk()
root.title("Diffie-Hellman")
root.geometry('350x150')

lbl_1= tk.Label(root, text="\nClick the button to start!", font= ("Arial",17))
lbl_1.pack()

#this is the start of the main function
def start_algo():
    #setting global variables
    global a, pa, pa_kp, ka_hashed

    #destroyed main window to open individual screens
    root.destroy()

    #A's screen generation
    result_a=tk.Tk()
    result_a.title("A's Screen")
    result_a.geometry('1200x600')

    #randomly generating A's private key(a) using the eliptic curve and showing
    a=SigningKey.generate(curve=SECP256k1)
    lbl_2=tk.Label(result_a, text="\nPrivate Key is selected for A", font=('Arial',15))
    lbl_2.pack()

    lbl_6=tk.Label(result_a, text=''+str(a.to_string().hex()), font=('Arial',15))
  
    def toggle_lbl_6():
        if not lbl_6.winfo_viewable():
            lbl_6.pack(after=lbl_2)
        else:
            lbl_6.pack_forget()


    toggle_btn_1 = tk.Button(result_a, text="Toggle Show", bd=5 , command=toggle_lbl_6)
    toggle_btn_1.pack()

    #calculating public key for A then showing 
    pa=a.get_verifying_key()
    pa_kp= pa.pubkey.point

    lbl_3=tk.Label(result_a, text="\nPublic key is formed by A's private key", font=('Arial',15))
    lbl_3.pack()

    frame_x1 = tk.Frame(result_a)
    frame_x1.pack()

    lbl_7 = tk.Label(frame_x1, text=f"x point: {hex(pa_kp.x())}", font=('Arial', 10))
    lbl_7.pack(side="left")

    def cp_bt1():
        result_a.clipboard_clear()
        result_a.clipboard_append(hex(pa_kp.x()))
    
    cp_btn = tk.Button(frame_x1, text="Copy", bd=5, command=cp_bt1)
    cp_btn.pack(side="left", padx=5)



    frame_y1 =tk.Frame(result_a)
    frame_y1.pack()

    lbl_9=tk.Label(frame_y1, text=f"y point: {hex(pa_kp.y())}", font=('Arial', 10))
    lbl_9.pack(side="left")

    def cp_bt2():
        result_a.clipboard_clear()
        result_a.clipboard_append(hex(pa_kp.y()))

    cp_btn_2 = tk.Button(frame_y1, text="Copy", bd=5, command=cp_bt2)
    cp_btn_2.pack(side="left", padx=5)

    lbl_4=tk.Label(result_a, text="\nEnter the public key received from B", font=('Arial',15))
    lbl_4.pack()

    frame_x2 = tk.Frame(result_a)
    frame_x2.pack()

    lbl_8=tk.Label(frame_x2, text="x point: ", font=('Arial', 10))
    lbl_8.pack(side="left")

    entry_x2 = tk.Entry(frame_x2, width=40)
    entry_x2.pack(side="left")

    cp_bt1 = tk.Button(frame_x2, text="Paste", bd=5, command=lambda: entry_x2.insert(tk.END, result_a.clipboard_get()))
    cp_bt1.pack(side="left", padx=5)

    frame_y2 = tk.Frame(result_a)
    frame_y2.pack()

    lbl_10 = tk.Label(frame_y2, text="y point: ", font=('Arial', 10))
    lbl_10.pack(side="left")

    entry_y2 = tk.Entry(frame_y2, width=40)
    entry_y2.pack(side="left")


    cp_bt2 = tk.Button(frame_y2, text="Paste", bd=5, command=lambda: entry_y2.insert(tk.END, result_a.clipboard_get()))
    cp_bt2.pack(side="left", padx=5)

    def ok_bt():
        global ka_hashed
        entry_x2_value=entry_x2.get()
        entry_y2_value=entry_y2.get()

        # Convert hex values to integers
        x_int= int(entry_x2_value,16)
        y_int= int(entry_y2_value,16)

        # Recreate the elliptic curve point
        pb_point = Point(SECP256k1.curve, x_int, y_int)

        # Generate the verifying key (public key) from the point
        pb= VerifyingKey.from_public_point(pb_point, curve=SECP256k1)
        

        #calculating the final key for both and showing
        def ecdh_shared_secret(private_key, public_key):
        # Perform scalar multiplication of the private key with the public key
            shared_point = private_key.privkey.secret_multiplier * public_key.pubkey.point
        # We only use the x-coordinate of the resulting point as the shared secret
            shared_secret = shared_point.x()
            return shared_secret

        ka= ecdh_shared_secret(a,pb)
        ka_hashed= sha256(ka.to_bytes(32,'big')).hexdigest()

        frame_z=tk.Frame(result_a)
        frame_z.pack()

        lbl_5=tk.Label(frame_z, text="\nThe final is calculated", font=('Arial',15))
        lbl_5.pack()
        
        lbl_9=tk.Label(frame_z, text=""+str(ka_hashed), font=('Arial', 15)) 

        def toggle_lbl_9():
            if not lbl_9.winfo_viewable():
                lbl_9.pack(after=lbl_5, side="left")
            else:
                lbl_9.pack_forget()  

        def cp_bt3():
            result_a.clipboard_clear()
            result_a.clipboard_append(ka_hashed)

        cp_bt3 = tk.Button(frame_z, text="Copy", bd=5, command=cp_bt3)
        cp_bt3.pack(side="left", padx=5)

        toggle_btn_4= tk.Button(frame_z, text="Toggle Show", bd=5 , command=toggle_lbl_9)
        toggle_btn_4.pack()       

        # Quit buttons
        quit_btn_a = tk.Button(result_a, text="Quit", bd=5 ,command=result_a.destroy)
        quit_btn_a.pack(pady=10)

        return(pa)
    
    ok_btn= tk.Button(result_a, text="OK", bd=5, command=ok_bt)
    ok_btn.pack()


btn_1= tk.Button(root, text= "Start", bd=5 ,command=start_algo, font=('Arial',12))
btn_1.pack()
root.mainloop()

print(ka_hashed)