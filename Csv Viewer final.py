import pandas as pd
import tkinter as tk
from tkinter import filedialog, ttk, simpledialog, messagebox

df = pd.DataFrame()  
file_path = ""  

def open_file(): #Öffnet CSV-Datei und lädt Daten ins DataFrame
    global df, file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            df = pd.read_csv(file_path, delimiter=";", on_bad_lines="skip", encoding="utf-8")  
            df.fillna("-", inplace=True)  
            display_data()
        except Exception as e:
            error_label.config(text=f"Fehler beim Laden: {e}")

def display_data(): #Zeigt die daten aus df im treeview an
    for widget in frame.winfo_children():
        widget.destroy()
    
    frame_scroll = tk.Frame(frame)
    frame_scroll.pack(fill="both", expand=True)

    tree = ttk.Treeview(frame_scroll)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"

    vsb = ttk.Scrollbar(frame_scroll, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame_scroll, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")

    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=max(100, len(col) * 8))  

    for index, row in df.iterrows():
        tree.insert("", "end", iid=index, values=list(row))

    tree.pack(fill="both", expand=True)

    # Buttons für Bearbeiten, Hinzufügen, Löschen und Speichern
    btn_edit = tk.Button(frame, text="Bearbeiten", command=lambda: edit_record(tree))
    btn_edit.pack(side="left", padx=5, pady=5)

    btn_add = tk.Button(frame, text="Hinzufügen", command=lambda: add_record(tree))
    btn_add.pack(side="left", padx=5, pady=5)

    btn_delete = tk.Button(frame, text="Löschen", command=lambda: delete_record(tree))
    btn_delete.pack(side="left", padx=5, pady=5)

    btn_save = tk.Button(frame, text="Speichern", command=save_file)
    btn_save.pack(side="left", padx=5, pady=5)

def edit_record(tree): #bearbeitet einen ausgewählten Datensatz
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warnung", "Bitte wählen Sie eine Zeile zum Bearbeiten aus.")
        return

    index = int(selected_item[0])  
    row_values = df.loc[index].tolist()

    edit_window = tk.Toplevel(root)
    edit_window.title("Datensatz bearbeiten")

    entries = []
    for i, col in enumerate(df.columns):
        tk.Label(edit_window, text=col).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(edit_window)
        entry.insert(0, row_values[i])
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    def save_changes():
        for i, entry in enumerate(entries):
            df.at[index, df.columns[i]] = entry.get()
        display_data()
        edit_window.destroy()

    tk.Button(edit_window, text="Speichern", command=save_changes).grid(row=len(df.columns), column=0, columnspan=2, pady=10)

def add_record(tree): #hinzufügen eines neuen Datensatzes
    add_window = tk.Toplevel(root)
    add_window.title("Neuen Datensatz hinzufügen")

    entries = []
    for i, col in enumerate(df.columns):
        tk.Label(add_window, text=col).grid(row=i, column=0, padx=5, pady=5)
        entry = tk.Entry(add_window)
        entry.grid(row=i, column=1, padx=5, pady=5)
        entries.append(entry)

    def save_new_record():
        new_data = [entry.get() for entry in entries]
        global df
        df.loc[len(df)] = new_data
        display_data()
        add_window.destroy()

    tk.Button(add_window, text="Hinzufügen", command=save_new_record).grid(row=len(df.columns), column=0, columnspan=2, pady=10)

def delete_record(tree): #Löscht einen ausgewählten Datensatz
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Warnung", "Bitte wählen Sie eine Zeile zum Löschen aus.")
        return

    index = int(selected_item[0])
    confirm = messagebox.askyesno("Bestätigung", "Möchten Sie diesen Datensatz wirklich löschen?")
    if confirm:
        global df
        df = df.drop(index).reset_index(drop=True)
        display_data()

def save_file(): #speichert die ausgewählte CSV-Datei
    global file_path
    if not file_path:
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    
    if file_path:
        df.to_csv(file_path, sep=";", index=False, encoding="utf-8")
        messagebox.showinfo("Gespeichert", "Die Datei wurde erfolgreich gespeichert.")

#GUI erstellen
root = tk.Tk()
root.title("CSV Editor von Julian")
root.geometry("800x600")

btn_open = tk.Button(root, text="CSV Datei öffnen", command=open_file)
btn_open.pack()

error_label = tk.Label(root, text="", fg="red")
error_label.pack()

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

root.mainloop()
