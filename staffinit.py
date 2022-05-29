# staffinit.py - a program that is ran once to initialise the current staff list
# to prevent adding colleagues everytime main program is ran.

import pickle
import openpyxl
from staffcolleagueclasses import Staff

# an instance of the staff class is created to store the colleagues.
staff = Staff()

# each colleague is added using the add_colleague method.
staff.add_colleague('Ball', 'Tommy', 'Shopfloor', 5, 39, prev_wknd=False)
staff.add_colleague('Barnet', 'Annie', 'Eve', 5, 20)
staff.add_colleague('Cunningham', 'Devontay', 'Eve', 5, 20)
staff.add_colleague('Chalmers', 'Ritchie', 'Shopfloor', 4, 30)
staff.add_colleague('Cooper', 'Simon', 'Weekend', 2, 8)
staff.add_colleague('Carter', 'Ovince', 'Weekend', 2, 8)
staff.add_colleague('Doone', 'Perry', 'Manager', 5, 39, prev_wknd=True)
staff.add_colleague('Farmer', 'Elizabeth', 'Shopfloor', 3, 12, prev_wknd=True)
staff.add_colleague('Fortuna', 'Mika', 'Warehouse', 5, 39)
staff.add_colleague('Gravely', 'Tina', 'Manager', 5, 39, prev_wknd=False)
staff.add_colleague('Juniper', 'Sia', 'Tills', 4, 16)
staff.add_colleague('Krabb', 'Casey', 'Weekend', 2, 8)
staff.add_colleague('Moon', 'Jaqui', 'Tills', 3, 12)
staff.add_colleague('McPhelan', 'Jon', 'Manager', 5, 39)
staff.add_colleague('McAleer', 'George', 'Eve', 2, 8)
staff.add_colleague('McElrea', 'Sean', 'Warehouse', 2, 16)
staff.add_colleague('McClintock', 'Greg', 'Showroom', 5, 39, prev_wknd=True)
staff.add_colleague('McKinty', 'Cara', 'Weekend', 2, 8)
staff.add_colleague('McKinty', 'Saoirse', 'Tills', 3, 12)
staff.add_colleague('Montgomery', 'Annie', 'Shopfloor', 5, 20)
staff.add_colleague('Montgomery', 'Cara', 'Eve', 5, 20)
staff.add_colleague('Montgomery', 'Lisa', 'Manager', 5, 39, prev_wknd=True)
staff.add_colleague('Moorehouse', 'Alan', 'Shopfloor', 5, 39)
staff.add_colleague("O'Hanlon", 'Neil', 'Warehouse', 2, 16)
staff.add_colleague('Roberts', 'Alexandra', 'Shopfloor', 5, 39, prev_wknd=True)
staff.add_colleague('Rune', 'Jackson', 'Manager', 5, 39, prev_wknd=False)
staff.add_colleague('Snell', 'Gabby', 'Showroom', 5, 39, prev_wknd=False)

# initialise dictionary to store the row number of the cell values.
insert_dict = {}
# track the department of the iterated colleagues.
current_dept = None
# open blank worksheet that contains only the department names in column A and
# the day name headers.
wb = openpyxl.load_workbook('blank_week.xlsx')
sheet = wb.active
# iterate through the previously added colleagues to add them to the
# spreadsheet
for col in staff.colleagues:
    # if the colleague has a different department from the previous the dict
    # will be refreshed to prevent overwriting cells.
    if current_dept != col.department:
        for cell in list(sheet.columns)[0]:
            insert_dict[cell.value] = cell.row
    # the column values for the colleague name and their hours are saved to
    # variables.
    name_column = 'A'
    hrs_column = 'B'
    # the row value for the new colleague will be the corresponding value of the
    # department in the dict + 1.
    new_row = insert_dict[col.department] + 1
    # a blank row is inserted at the previously determined value.
    sheet.insert_rows(new_row)
    # the value for the department is updated
    insert_dict[col.department] += 1
    # the relevant info is added to the worksheet.
    sheet[name_column + str(new_row)] = col.name()
    sheet[hrs_column + str(new_row)] = col.hours
# after all colleagues and their hours have been added the file is saved.
wb.save('testy.xlsx')
wb.close()

# the staff object containing all the above colleagues is saved to a file
# called 'current_staff' using the pickle module.
with open('current_staff', 'wb') as f:
    pickle.dump(staff, f)
