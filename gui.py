import tkinter as tk
from tkinter import messagebox

from db_handler import search_inj_db
from deviation_calc import deviation_inj
from pdf_generation import save_to_pdf


def run_gui(conn):
    # Main frame
    root = tk.Tk()
    root.title("Форма перевірки форсунок")
    root.geometry("600x650")

    # Item info frame
    frame_item_info = tk.Frame(root)
    frame_item_info.grid(row=0, column=0, padx=10, sticky="w")

    label_client_number = tk.Label(frame_item_info, text="Клієнт:")
    label_client_number.grid(row=0, column=0, padx=10, pady=5, sticky="w")
    entry_number = tk.Entry(frame_item_info, width=60)
    entry_number.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    label_engine_number = tk.Label(frame_item_info, text="Двигун:")
    label_engine_number.grid(row=1, column=0, padx=10, pady=5, sticky="w")
    entry_engine_number = tk.Entry(frame_item_info, width=60)
    entry_engine_number.grid(row=1, column=1, padx=10, pady=5, sticky="w")

    label_inj_number = tk.Label(frame_item_info, text="Номер форсунки:")
    label_inj_number.grid(row=2, column=0, padx=10, pady=5, sticky="w")
    entry_inj_number = tk.Entry(frame_item_info, width=60)
    entry_inj_number.grid(row=2, column=1, padx=10, pady=5, sticky="w")
    entry_alt_inj_number = tk.Entry(frame_item_info, width=60)
    entry_alt_inj_number.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Type and amount inj
    inj_type_frame = tk.Frame(root)
    inj_type_frame.grid(row=6, column=0, padx=10, pady=5, sticky="w")

    label_inj_type = tk.Label(inj_type_frame, text="Тип форсунки:")
    label_inj_type.grid(row=0, column=0, padx=10, sticky="w")

    type_var = tk.StringVar()
    type_var.set("FSI")

    inj_type_radio = tk.Frame(inj_type_frame)
    inj_type_radio.grid(row=0, column=1, padx=10, sticky="w")

    inj_chose_box = tk.Frame(root)
    inj_chose_box.grid(row=7, column=0, padx=10, pady=5, sticky="w")

    label_select = tk.Label(inj_chose_box, text="Кількість форсунок:")
    label_select.grid(row=0, column=0, padx=10, pady=5, sticky="w")

    radio_frame = tk.Frame(inj_chose_box)
    radio_frame.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    nozzle_var = tk.IntVar()
    nozzle_var.set(4)

    inj_param = None

    for i in range(1, 9):
        tk.Radiobutton(radio_frame, text=str(i), variable=nozzle_var, value=i,
                       command=lambda: update_fields()).grid(row=0, column=i-1, padx=5, pady=5, sticky="w")

    entry_inj_data = {}

    # Dynamic row info inj
    frame_inj_info = tk.Frame(root)
    frame_inj_info.grid(row=8, column=0, padx=10, pady=5, sticky="w")

    # Update fields by inj type
    def inj_type_change():
        update_fields()

    def update_fields():
        nonlocal inj_param
        for widget in frame_inj_info.grid_slaves():
            if int(widget.grid_info()["row"]) > 1:
                widget.grid_forget()

        entry_inj_data.clear()

        if type_var.get() == "PIEZO":
            headers = ["0.5 мс", "0.7 мс", "1.5 мс", "Герм.", "Факел", "Відхил."]
        else:
            headers = ["2.5 мс", "1.0 мс", "1.5 мс", "Герм.", "Факел", "Відхил."]
        for col, header in enumerate(headers):
            header_label = tk.Label(frame_inj_info, text=header)
            header_label.grid(row=0, column=col, padx=10, pady=5, sticky="w")

        selected_value = int(nozzle_var.get())

        # Calculate deviation inj
        def deviation_calc(row):
            if entry_inj_data[row][0].get() and entry_inj_data[row][1].get() and entry_inj_data[row][2].get():
                try:
                    param_1 = float(entry_inj_data[row][0].get())
                    param_2 = float(entry_inj_data[row][1].get())
                    param_3 = float(entry_inj_data[row][2].get())
                    if not inj_param:
                        entry_inj_data[row][5].delete(0, tk.END)
                        entry_inj_data[row][5].insert(0, "0")
                        return

                    result_div = deviation_inj(inj_param, param_1, param_2, param_3)

                    entry_inj_data[row][5].delete(0, tk.END)
                    entry_inj_data[row][5].insert(0, str(result_div))
                except ValueError:
                    messagebox.showwarning("Помилка","Введені некоректні значення параметрів форсунки.\n"
                                             "Перевірте правильність введених даних")

        for row in range(selected_value):
            inj_data = {}

            for col in range(6):
                entry = tk.Entry(frame_inj_info, width=12)
                entry.grid(row=row+1, column=col, padx=10, pady=5, sticky="w")
                inj_data[col] = entry
                if col < 3:
                    entry.bind("<KeyRelease>", lambda event, r=row: deviation_calc(r))

            entry_inj_data[row] = inj_data


        save_button.grid(row=selected_value + 3, column=1, pady=10)
        clear_button.grid(row=selected_value + 3, column=0, padx=5, pady=10)

    # Function save to pdf
    def save():
        data = {}
        inj_type = type_var.get()
        client_number = entry_number.get()
        inj_number = entry_inj_number.get()
        alt_inj_number = entry_alt_inj_number.get()
        engine_number = entry_engine_number.get()
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
        data["alt_inj_number"] = alt_inj_number
        data["engine"] = engine_number
        data["selected_inj"] = selected_nozzles
        data["inj_type"] = inj_type

        if not client_number or not inj_number:
            messagebox.showwarning("Помилка", "Заповніть поля 'Клієнт' або 'Номер форсунки'")
        else:
            save_to_pdf(data)
            messagebox.showinfo("Успіх", "Дані були збережені")
    # Clear all fields
    def clear_fields():
        for widget in frame_inj_info.grid_slaves():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                nonlocal inj_param
                inj_param = None

        for widget in frame_item_info.grid_slaves():
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
    # Search data by inj number
    def search_inj():
        nonlocal inj_param
        inj_number = entry_inj_number.get().strip()
        alt_inj_number = entry_alt_inj_number.get().strip()
        search_number = inj_number if inj_number else alt_inj_number
        if search_number:
            param = search_inj_db(conn, search_number)
            if param:
                label_search_inj.config(text="Форсунку знайдено, відхилення будуть рахуватись автоматично")
                inj_param = param
            else:
                label_search_inj.config(text="Форсунку не знайдено")
        else:
            label_search_inj.config(text="Введіть номер форсунки")

    # Buttons
    row_val = nozzle_var.get()
    button_box = tk.Frame(root)
    button_box.grid(row=row_val + 5, column=0, columnspan=5, padx=5, pady=10)
    save_button = tk.Button(button_box, text="Зберегти", command=save)
    clear_button = tk.Button(button_box, text="Видалити все", command=clear_fields)
    search_button = tk.Button(frame_item_info, text="Знайти форсунку", command=search_inj)
    search_button.grid(row=5, column=1, pady=5)
    label_search_inj = tk.Label(frame_item_info, text="")
    label_search_inj.grid(row=4, column=1, padx=10, pady=5, sticky="w")
    type_button_1 = tk.Radiobutton(inj_type_radio, text="FSI", variable=type_var, value="FSI", command=inj_type_change)
    type_button_1.grid(row=0, column=0, padx=10, sticky="w")

    type_button_2 = tk.Radiobutton(inj_type_radio, text="PIEZO", variable=type_var, value="PIEZO",
                                   command=inj_type_change)
    type_button_2.grid(row=0, column=1, padx=10, sticky="w")

    update_fields()

    root.mainloop()
