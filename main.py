import subprocess
import re
import os
import tkinter as tk
from tkinter import messagebox, filedialog

def get_wifi_profiles():
    output = subprocess.check_output("netsh wlan show profiles", shell=True, text=True)
    profiles = re.findall(r"All User Profile\s*:\s(.*)", output)
    return [profile.strip() for profile in profiles]

def get_wifi_password(profile):
    try:
        result = subprocess.check_output(f"netsh wlan show profile name=\"{profile}\" key=clear", shell=True, text=True)
        password = re.search(r"Key Content\s*:\s(.*)", result)
        return password.group(1).strip() if password else "N/A"
    except subprocess.CalledProcessError:
        return "Error retrieving password"

def show_selected_password():
    profile = selected_profile.get()
    if profile:
        password = get_wifi_password(profile)
        output_text.set(f"Password for '{profile}': {password}")
    else:
        output_text.set("Please select a profile.")

def show_all_passwords():
    all_data = ""
    for profile in profiles:
        password = get_wifi_password(profile)
        all_data += f"{profile}: {password}\n"
    output_text.set(all_data)

def save_all_passwords():
    wifi_data = {profile: get_wifi_password(profile) for profile in profiles}
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", title="Save Passwords As", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            for profile, password in wifi_data.items():
                f.write(f"{profile}: {password}\n")
        messagebox.showinfo("Saved", f"Passwords saved to:\n{file_path}")

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(output_text.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")


if os.name != "nt":
    print("❌ This script only runs on Windows.")
    exit()

profiles = get_wifi_profiles()

# GUI Setup
root = tk.Tk()
root.title("Wi-Fi Password Extractor")
root.geometry("500x350")
root.resizable(False, False)

tk.Label(root, text="Select a Wi-Fi Profile:", font=("Arial", 12)).pack(pady=10)
selected_profile = tk.StringVar()
dropdown = tk.OptionMenu(root, selected_profile, *profiles)
dropdown.config(width=50)
dropdown.pack()

tk.Button(root, text="🔍 Show Password", command=show_selected_password, width=20).pack(pady=5)
tk.Button(root, text="📋 Show All Passwords", command=show_all_passwords, width=20).pack(pady=5)
tk.Button(root, text="💾 Save All to File", command=save_all_passwords, width=20).pack(pady=5)
tk.Button(root, text="📋 Copy to Clipboard", command=copy_to_clipboard, width=20).pack(pady=5)

output_text = tk.StringVar()
output_label = tk.Label(root, textvariable=output_text, wraplength=480, justify="left", font=("Courier", 10), bg="white", relief="sunken", bd=1)
output_label.pack(pady=15, padx=10, fill="both", expand=True)

root.mainloop()
