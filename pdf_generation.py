from datetime import datetime

from fpdf import FPDF


def save_to_pdf(data):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.add_font("DejaVu", "", "fonts/ttf/DejaVuSans.ttf", uni=True)
    pdf.set_font("DejaVu", size=14)

    col_width = [27, 27, 27, 27, 27, 27, 27]
    row_height = 10

    current_date = datetime.now().strftime("%H:%M, %d.%m.%Y")

    pdf.cell(200, 10, txt=f"{current_date}", ln=True)
    pdf.cell(200, 10, txt=f"Клієнт: {data["client"]}", ln=True)
    pdf.cell(200, 10, txt=f"Двигун: {data["engine"]}", ln=True)
    pdf.cell(200, 10, txt=f"Номер форсунки: {data["inj_number"]}, {data["alt_inj_number"]}", ln=True)

    pdf.cell(200, 15, txt="Форсунки:", ln=True)

    if data["inj_type"] == "PIEZO":
        headers = ["#", "0.5 мс", "0.7 мс", "1.5 мс", "Герм.", "Факел", "Відхил."]
    else:
        headers = ["#", "2.5 мс", "1.0 мс", "1.5 мс", "Герм.", "Факел", "Відхил."]

    for i, header in enumerate(headers):
        pdf.cell(col_width[i], row_height, txt=header, border=1, align="C")
    pdf.ln(row_height)

    for index in range(data["selected_inj"]):
        params = data[index]
        pdf.cell(col_width[0], row_height, txt=f"Форс. {str(index + 1)}", border=1, align='C')
        for key in range(6):
            pdf.cell(col_width[key], row_height, txt=params[key], border=1, align="C")
        pdf.ln(row_height)

    date = datetime.now().timestamp()
    file_name = f"{int(date)}_{data['client']}"
    pdf.output(f"clients/{file_name}.pdf")

