import openpyxl

# function to increase relevant row numbers by 1 after insertion of col into
# worksheet.
def row_updater(row, row_dict):
    for key, value in row_dict.items():
        if value >= row:
            row_dict[key] += 1


def col_to_excel(excel_file, col, row_dict):
    wb = openpyxl.load_workbook(excel_file)
    sheet = wb.active
    new_row = row_dict[col.department] + 1
    # the values for the relevant rows are increased by 1.
    row_updater(new_row, row_dict)
    # a blank row is inserted at the previously determined value.
    sheet.insert_rows(new_row)
    # the relevant info is added to the worksheet. Column A contains
    # the dept headings and therefore, the col's are placed under
    # the corresponding one. B is for the colleague hours.
    sheet['A' + str(new_row)] = col.name()
    sheet['B' + str(new_row)] = col.hours
    wb.save(excel_file)
    wb.close()
    return new_row
