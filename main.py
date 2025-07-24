import tkinter as tk
from tkinter import filedialog, messagebox
import os


def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)
        update_preview()


def update_preview():
    original_listbox.delete(0, tk.END)
    preview_listbox.delete(0, tk.END)

    folder = folder_var.get()
    mode = mode_var.get()
    if not folder or not os.path.isdir(folder):
        return

    for filename in os.listdir(folder):
        if not filename.lower().endswith('.jpg'):
            continue

        parts = filename.split('_')
        if len(parts) < 3:
            continue

        new_name = filename
        # Replace second underscore with '+'
        first = filename.find('_')
        second = filename.find('_', first + 1)
        if second == -1:
            continue
        new_name = filename[:second] + '+' + filename[second + 1:]

        # If "+ e COTAS" is selected
        if mode == "plus_cotas":
            if new_name.endswith('_SCT.jpg'):
                new_name = new_name.replace('_SCT.jpg', '_COTAS.jpg')
            else:
                continue  # Ignore if not ending in _SCT.jpg

        original_listbox.insert(tk.END, filename)
        preview_listbox.insert(tk.END, new_name)


def rename_files():
    folder = folder_var.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Error", "Please select a valid folder.")
        return

    renamed = 0
    for i in range(original_listbox.size()):
        original = original_listbox.get(i)
        new = preview_listbox.get(i)

        old_path = os.path.join(folder, original)
        new_path = os.path.join(folder, new)

        if original != new:
            try:
                os.rename(old_path, new_path)
                renamed += 1
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename {original}:\n{e}")
                return

    messagebox.showinfo("Done", f"{renamed} files renamed.")
    update_preview()


# --- GUI Setup ---
root = tk.Tk()
root.title("Renomear JPGs")
root.geometry("600x400")

folder_var = tk.StringVar()
mode_var = tk.StringVar(value="plus")

# Folder selection
tk.Button(root, text="Browse Folder", command=select_folder).pack(pady=5)
tk.Entry(root, textvariable=folder_var, width=80, state='readonly').pack()

# Radio buttons
frame_radio = tk.Frame(root)
tk.Radiobutton(frame_radio, text="+", variable=mode_var, value="plus", command=update_preview).pack(side=tk.LEFT,
                                                                                                    padx=10)
tk.Radiobutton(frame_radio, text="+ e COTAS", variable=mode_var, value="plus_cotas", command=update_preview).pack(
    side=tk.LEFT, padx=10)
frame_radio.pack(pady=10)

# Listboxes for original and preview
frame_lists = tk.Frame(root)
original_listbox = tk.Listbox(frame_lists, width=40, height=15)
preview_listbox = tk.Listbox(frame_lists, width=40, height=15)
original_listbox.pack(side=tk.LEFT, padx=5)
preview_listbox.pack(side=tk.LEFT, padx=5)
frame_lists.pack()

# Submit button
tk.Button(root, text="Renomear", command=rename_files).pack(pady=10)

root.mainloop()
