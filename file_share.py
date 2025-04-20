import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import paramiko
import pyperclip
import threading
import socket
from paramiko import ServerInterface, AUTH_SUCCESSFUL, OPEN_SUCCEEDED
import getpass
import secrets
import string


def ssh_connect(host, port, username, password):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, port=port, username=username, password=password)
    return ssh

def sftp_connect(ssh):
    return ssh.open_sftp()

def upload_file():
    cfg = get_inputs()
    try:
        ssh = ssh_connect(cfg['host'], cfg['port'], cfg['username'], cfg['password'])
        sftp = sftp_connect(ssh)

        file_path = filedialog.askopenfilename(title="Select local file to upload")
        if not file_path:
            return

        remote_path = simple_input("Enter remote file path to save to (e.g., /home/username/upload.txt):")
        if not remote_path:
            return

        sftp.put(file_path, remote_path)
        log("✅ File uploaded successfully")

        sftp.close()
        ssh.close()
    except Exception as e:
        log(f"❌ Upload failed: {e}")

def download_file():
    cfg = get_inputs()
    try:
        ssh = ssh_connect(cfg['host'], cfg['port'], cfg['username'], cfg['password'])
        sftp = sftp_connect(ssh)

        remote_path = simple_input("Enter remote file path to download (e.g., /home/username/file.txt):")
        if not remote_path:
            return

        local_path = filedialog.asksaveasfilename(title="Save as on your PC")
        if not local_path:
            return

        sftp.get(remote_path, local_path)
        log("✅ File downloaded successfully")

        sftp.close()
        ssh.close()
    except Exception as e:
        log(f"❌ Download failed: {e}")

def share_clipboard():
    cfg = get_inputs()
    try:
        clipboard_data = pyperclip.paste()
        ssh = ssh_connect(cfg['host'], cfg['port'], cfg['username'], cfg['password'])

        command = f"echo '{clipboard_data}' > ~/clipboard_shared.txt"
        ssh.exec_command(command)
        log("📋 Clipboard shared to device as 'clipboard_shared.txt'")

        ssh.close()
    except Exception as e:
        log(f"❌ Clipboard share failed: {e}")

def connect_ssh():
    cfg = get_inputs()
    try:
        ssh = ssh_connect(cfg['host'], cfg['port'], cfg['username'], cfg['password'])
        log("✅ SSH connection successful!")
        ssh.close()
        connect_btn.config(state=tk.DISABLED)
    except Exception as e:
        log(f"❌ SSH connection failed: {e}")

def get_inputs():
    return {
        'host': host_entry.get(),
        'port': int(port_entry.get()),
        'username': user_entry.get(),
        'password': pass_entry.get()
    }

def simple_input(prompt):
    return simpledialog.askstring("Remote File Path", prompt)

def log(message):
    log_box.config(state=tk.NORMAL)
    log_box.insert(tk.END, message + "\n")
    log_box.see(tk.END)
    log_box.config(state=tk.DISABLED)

# GUI Setup
root = tk.Tk()
root.title("IoT SSH File Manager")
root.geometry("500x500")
root.configure(bg="#f0f0f0")

frame = tk.Frame(root, padx=20, pady=20, bg="#f0f0f0")
frame.pack(fill=tk.BOTH, expand=True)

entry_width = 30
label_opts = {'bg': '#f0f0f0', 'anchor': 'e', 'padx': 5, 'pady': 5}

# Input Fields
tk.Label(frame, text="Hostname/IP:", **label_opts).grid(row=0, column=0, sticky='e')
host_entry = tk.Entry(frame, width=entry_width)
host_entry.grid(row=0, column=1, sticky='w')

tk.Label(frame, text="Port:", **label_opts).grid(row=1, column=0, sticky='e')
port_entry = tk.Entry(frame, width=entry_width)
port_entry.insert(0, "22")
port_entry.grid(row=1, column=1, sticky='w')

tk.Label(frame, text="Username:", **label_opts).grid(row=2, column=0, sticky='e')
user_entry = tk.Entry(frame, width=entry_width)
user_entry.grid(row=2, column=1, sticky='w')

tk.Label(frame, text="Password:", **label_opts).grid(row=3, column=0, sticky='e')
pass_entry = tk.Entry(frame, show="*", width=entry_width)
pass_entry.grid(row=3, column=1, sticky='w')

# Buttons
connect_btn = tk.Button(frame, text="🔌 Connect", width=entry_width + 6, command=connect_ssh, bg="#4CAF50", fg="white")
connect_btn.grid(row=4, column=0, columnspan=2, pady=(10, 5))

upload_btn = tk.Button(frame, text="⬆️ Upload File", width=20, command=upload_file)
upload_btn.grid(row=5, column=0, pady=5)

download_btn = tk.Button(frame, text="⬇️ Download File", width=20, command=download_file)
download_btn.grid(row=5, column=1, pady=5)

clipboard_btn = tk.Button(frame, text="📋 Share Clipboard", width=entry_width + 6, command=share_clipboard)
clipboard_btn.grid(row=6, column=0, columnspan=2, pady=10)

# Log Box
log_label = tk.Label(frame, text="Logs:", **label_opts)
log_label.grid(row=7, column=0, columnspan=2, sticky='w', pady=(10, 0))

log_box = tk.Text(frame, height=10, state=tk.DISABLED, bg="#ffffff", relief=tk.SUNKEN, bd=1)
log_box.grid(row=8, column=0, columnspan=2, pady=(0, 10), sticky='nsew')

# Make log box expand with window
frame.grid_rowconfigure(8, weight=1)
frame.grid_columnconfigure(1, weight=1)

username = getpass.getuser()
password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))

class SimpleSSHServer(ServerInterface):
    def __init__(self, authorized_user, authorized_password):
        self.authorized_user = authorized_user
        self.authorized_password = authorized_password

    def check_auth_password(self, username, password):
        if username == self.authorized_user and password == self.authorized_password:
            return AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    
    def check_channel_pty_request(self, channel, term, width, height, pixwidth, pixheight, modes):
        return True  # Allow PTY requests

    def check_channel_shell_request(self, channel):
        return True

def start_ssh_server():
    port = 2222

    try:
        host_key = paramiko.RSAKey.generate(2048)
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('', port))
        server_socket.listen(100)

        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)

        print(f"🚀 SSH server running!")
        print(f"🖥️ Hostname/IP: {ip}")
        print(f"👤 Username: {username}")
        print(f"🔐 Password: {password}")
        print(f"📡 Port: {port}")
        print("🛠️ You can now connect to this device using the GUI from another computer.")
        log(f"🚀 SSH server started on {ip}:{port}")
        log(f"👤 Username: {username}")
        log(f"🔐 Password: {password}")
        log("🛠️ Ready to accept connections from other devices.")


        def handle_client(client_socket):
            transport = paramiko.Transport(client_socket)
            transport.add_server_key(host_key)
            server = SimpleSSHServer(username, password)
            try:
                transport.start_server(server=server)
                channel = transport.accept(20)
                if channel is None:
                    return

                # Send welcome message
                channel.send(channel.send("\n✅ Connected to IoT SSH Server!\nType something and press Enter:\n".encode())
)

                # Keep the channel open and echo messages
                while True:
                    data = channel.recv(1024)
                    if not data:
                        break
                    message = data.decode().strip()
                    response = f"Echo: {message}\n"
                    channel.send(response.encode())

                channel.close()
            except Exception as e:
                print(f"⚠️ SSH server error: {e}")
            finally:
                transport.close()


        def server_loop():
            while True:
                client, _ = server_socket.accept()
                threading.Thread(target=handle_client, args=(client,), daemon=True).start()

        threading.Thread(target=server_loop, daemon=True).start()

    except Exception as e:
        print(f"❌ Failed to start SSH server: {e}")

# Start the SSH server in background
start_ssh_server()

root.mainloop()
