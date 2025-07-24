import tkinter as tk
from tkinter import filedialog, messagebox
import os
from datetime import datetime
import shutil


def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)
        update_preview()


def update_preview():
    original_listbox.delete(0, tk.END)
    preview_listbox.delete(0, tk.END)
    original_files.clear()
    renamed_files.clear()

    folder = folder_var.get()
    mode = mode_var.get()
    if not folder or not os.path.isdir(folder):
        return

    for filename in os.listdir(folder):
        if not filename.lower().endswith(('.jpg', '.jpeg')):
            continue

        parts = filename.split('_')
        if len(parts) < 3:
            continue

        new_name = filename
        first = filename.find('_')
        second = filename.find('_', first + 1)
        if second == -1:
            continue
        new_name = filename[:second] + '+' + filename[second + 1:]

        if mode == "plus_cotas":
            if new_name.endswith('_SCT.jpg') or new_name.endswith('_SCT.jpeg'):
                new_name = new_name.rsplit('_SCT', 1)[0] + '_COTAS.jpg'
            else:
                continue  # ignore if not ending in _SCT

        original_files.append(filename)
        renamed_files.append(new_name)
        original_listbox.insert(tk.END, filename)
        preview_listbox.insert(tk.END, new_name)


def rename_files():
    folder = folder_var.get()
    if not folder or not os.path.isdir(folder):
        messagebox.showerror("Erro", "Por favor, selecione uma pasta válida.")
        return

    if not original_files:
        messagebox.showinfo("Nada a fazer", "Nenhum arquivo apropriado para renomear.")
        return

    do_backup = backup_var.get()
    do_log = log_var.get()
    renamed_count = 0

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_folder = os.path.join(folder, f"_backup_{timestamp}") if do_backup else None
    log_path = os.path.join(folder, f"renamed_log_{timestamp}.txt") if do_log else None

    if do_backup:
        os.makedirs(backup_folder, exist_ok=True)

    log_file = open(log_path, "w", encoding="utf-8") if do_log else None

    for original, new in zip(original_files, renamed_files):
        old_path = os.path.join(folder, original)
        new_path = os.path.join(folder, new)

        if original != new:
            try:
                if do_backup:
                    shutil.copy2(old_path, os.path.join(backup_folder, original))
                os.rename(old_path, new_path)
                if log_file:
                    log_file.write(f"{original} → {new}\n")
                renamed_count += 1
            except Exception as e:
                if log_file:
                    log_file.close()
                messagebox.showerror("Erro", f"Falha ao renomear {original}:\n{e}")
                return

    if log_file:
        log_file.close()

    msg = f"{renamed_count} arquivos renomeados."
    if do_backup:
        msg += f"\nBackup criado em:\n{backup_folder}"
    if do_log:
        msg += f"\nLog salvo em:\n{log_path}"
    messagebox.showinfo("Feito", msg)
    update_preview()


# --- GUI Setup ---
root = tk.Tk()
root.title("Renomear JPGs")
root.geometry("850x520")
root.minsize(800, 400)

folder_var = tk.StringVar()
mode_var = tk.StringVar(value="plus")
backup_var = tk.BooleanVar(value=True)
log_var = tk.BooleanVar(value=True)
original_files = []
renamed_files = []

# Folder selection
frame_top = tk.Frame(root)
frame_top.pack(fill=tk.X, padx=10, pady=5)

tk.Button(frame_top, text="Selecionar pasta", command=select_folder).pack(side=tk.LEFT)
tk.Entry(frame_top, textvariable=folder_var, width=80, state='readonly').pack(side=tk.LEFT, padx=10)

# Radio buttons
frame_radio = tk.Frame(root)
frame_radio.pack(pady=5)
tk.Radiobutton(frame_radio, text="+", variable=mode_var, value="plus", command=update_preview).pack(side=tk.LEFT,
                                                                                                    padx=10)
tk.Radiobutton(frame_radio, text="+ e COTAS", variable=mode_var, value="plus_cotas", command=update_preview).pack(
    side=tk.LEFT, padx=10)

# Checkboxes
frame_check = tk.Frame(root)
frame_check.pack(pady=5)
tk.Checkbutton(frame_check, text="Criar backup", variable=backup_var).pack(side=tk.LEFT, padx=20)
tk.Checkbutton(frame_check, text="Gerar log", variable=log_var).pack(side=tk.LEFT, padx=20)

# Listboxes with scrollbars
frame_lists = tk.Frame(root)
frame_lists.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

original_frame = tk.LabelFrame(frame_lists, text="Original")
original_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
original_listbox = tk.Listbox(original_frame)
original_scroll = tk.Scrollbar(original_frame, command=original_listbox.yview)
original_listbox.config(yscrollcommand=original_scroll.set)
original_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
original_scroll.pack(side=tk.RIGHT, fill=tk.Y)

preview_frame = tk.LabelFrame(frame_lists, text="Preview")
preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
preview_listbox = tk.Listbox(preview_frame)
preview_scroll = tk.Scrollbar(preview_frame, command=preview_listbox.yview)
preview_listbox.config(yscrollcommand=preview_scroll.set)
preview_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
preview_scroll.pack(side=tk.RIGHT, fill=tk.Y)

# Rename button
tk.Button(root, text="Renomear", command=rename_files).pack(pady=10)

root.mainloop()
