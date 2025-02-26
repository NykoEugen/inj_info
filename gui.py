import tkinter as tk
from tkinter import messagebox
from pdf_generation import save_to_pdf


def run_gui():
    root = tk.Tk()
    root.title("Форма перевірки форсунок")
    root.geometry("600x500")

    # Поля для введення
    frame_item_info = tk.Frame(root)
    frame_item_info.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    label_client_number = tk.Label(frame_item_info, text="Клієнт:")
    label_client_number.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_number = tk.Entry(frame_item_info, width=60)
    entry_number.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    label_inj_number = tk.Label(frame_item_info, text="Номер форсунки:")
    label_inj_number.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_inj_number = tk.Entry(frame_item_info, width=60)
    entry_inj_number.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    inj_chose_box = tk.Frame(root)
    inj_chose_box.grid(row=2, column=0, padx=10, pady=5, sticky="w")

    label_select = tk.Label(inj_chose_box, text="Кількість форсунок:")
    label_select.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    radio_frame = tk.Frame(inj_chose_box)
    radio_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    nozzle_var = tk.IntVar()
    nozzle_var.set(4)

    for i in range(1, 9):
        tk.Radiobutton(radio_frame, text=str(i), variable=nozzle_var, value=i,
                       command=lambda: update_fields()).grid(row=0, column=i-1, padx=5, pady=5, sticky="w")

    entry_inj_data = {}

    frame_inj_info = tk.Frame(root)
    frame_inj_info.grid(row=3, column=0, padx=10, pady=5, sticky="w")

    def update_fields():
        for widget in frame_inj_info.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()

        entry_inj_data.clear()

        headers = ["2.5 мс", "1.0 мс", "1.5 мс авто", "Герм.", "Факел", "Відхил."]
        for col, header in enumerate(headers):
            header_label = tk.Label(frame_inj_info, text=header)
            header_label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

        selected_value = int(nozzle_var.get())

        for row in range(selected_value):
            inj_data = {}

            for col in range(6):
                entry = tk.Entry(frame_inj_info, width=12)
                entry.grid(row=row+1, column=col, padx=10, pady=5, sticky="w")
                inj_data[col] = entry

            entry_inj_data[row] = inj_data

        save_button.grid(row=selected_value + 3, column=1, pady=10)
        clear_button.grid(row=selected_value + 3, column=0, padx=5, pady=10)

    # Кнопка для збереження у PDF
    def save():
        data = {}
        client_number = entry_number.get()
        inj_number = entry_inj_number.get()
        selected_nozzles = nozzle_var.get()

        for row, entries in entry_inj_data.items():
            inj_data = {}
            for col, entry in entries.items():
                value = entry.get()
                if value:
                    inj_data[col] = value
            data[row] = inj_data

        data["client"] = client_number
        data["inj_number"] = inj_number
        data["selected_inj"] = selected_nozzles

        if not client_number or not inj_number:
            messagebox.showwarning("Помилка", "Заповніть поля 'Клієнт' або 'Номер форсунки'")
        else:
            save_to_pdf(data)
            messagebox.showinfo("Успіх", "Дані були збережені")

    def clear_fields():
        for widget in frame_inj_info.grid_slaves():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

        for widget in frame_item_info.grid_slaves():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)

    row_val = nozzle_var.get()
    button_box = tk.Frame(root)
    button_box.grid(row=row_val + 3, column=0, columnspan=5, padx=5, pady=10)

    save_button = tk.Button(button_box, text="Зберегти", command=save)
    clear_button = tk.Button(button_box, text="Видалити все", command=clear_fields)

    update_fields()

    root.mainloop()
