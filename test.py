import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Injectors result blank")
root.geometry("700x600")
entry_fields = []
selected_value = 4

nozzle_var = tk.IntVar()
nozzle_var.set(1)

radio_frame = tk.Frame(root)
radio_frame.grid(row=2, column=0, padx=10, pady=5)

def on_radio_button_select(value):
    # Ця функція буде викликана при виборі радіокнопки
    nozzle_var.set(value)  # Змінює значення змінної nozzle_var
    update_fields()  # Викликає функцію для оновлення полів

for i in range(1, 9):
    tk.Radiobutton(radio_frame, text=str(i), variable=nozzle_var, value=i,
                   command=lambda val=i: on_radio_button_select(val)).grid(row=0, column=i-1, padx=5, pady=5, sticky="w")
table_frame = tk.Frame(root)
table_frame.grid(row=3, column=0, padx=10, pady=10, sticky="w")

def update_fields():
    for widget in table_frame.winfo_children():
        widget.destroy()

    entry_fields.clear()

    headers = ["2.5 ms", "1.0 ms", "1.5 ms auto", "Fakel", "Tech", "Norma"]
    for col, header in enumerate(headers):
        header_label = tk.Label(root, text=header)
        header_label.grid(row=3, column=col, padx=10, pady=5, sticky="w")

    for row in range(selected_value):
        for col in range(6):
            entry = tk.Entry(root, width=12)
            entry.grid(row=row + 5, column=col, padx=10, pady=5, sticky="w")
            entry_fields.append(entry)

root.mainloop()