import openpyxl
from openpyxl.worksheet.table import Table, TableStyleInfo

workbook = openpyxl.Workbook()
sheet = workbook.active

sheet.title = f"Exhibitors IoT Expo China Hall {i}"

for row in xlsx_data:
    sheet.append(row)

table_range = f"A1:F{len(xlsx_data)}"

table = Table(displayName="ExhibitorTable", ref=table_range)

style = TableStyleInfo(
    name="TableStyleMedium9",
    showFirstColumn=False,
    showLastColumn=False,
    showRowStripes=True,
    showColumnStripes=True,
)
table.tableStyleInfo = style

sheet.add_table(table)

for row in range(2, len(xlsx_data) + 1):
    cell = sheet.cell(row=row, column=5)
    cell.hyperlink = cell.value
    cell.style = "Hyperlink"

xlsx_data = [header_row]

workbook.save(f"exhibitors-{i}.xlsx")
