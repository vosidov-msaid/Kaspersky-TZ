import xlsxwriter

def export_to_excel(data, filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()

    headers = ["word", "count_total", "line_counts"]
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    for row, (word, info) in enumerate(data.items(), start=1):
        worksheet.write(row, 0, word)
        worksheet.write(row, 1, info["total_count"])
        worksheet.write(row, 2, ", ".join(str(count) for count in info["line_counts"]))

    workbook.close()