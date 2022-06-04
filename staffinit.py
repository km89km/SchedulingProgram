# staffinit.py - a program that is ran once to initialise the current staff list
# to prevent adding colleagues everytime main program is ran.

import pickle
import openpyxl

from staffcolleagueclasses import Staff

# open blank worksheet that contains only the department names in column A and
# the day name headers.
wb = openpyxl.load_workbook('blank_week.xlsx')
sheet = wb.active

# initialise dictionary to store the row number of departments, then later,
# colleagues.
ws_rows = {}

# add row numbers for department names in blank_week worksheet.
for cell in list(sheet.columns)[0]:
    ws_rows[cell.value] = cell.row


# wb.save('new_blank.xlsx') to keep copy of empty worksheet.
wb.close()


# an instance of the staff class is created to store the colleagues.
staff = Staff()

# each colleague is added using the add_colleague method.
staff.add_colleague(ws_rows, 'Ball', 'Tommy', 'Shopfloor', 5, 39,
                    prev_wknd=False)
staff.add_colleague(ws_rows, 'Barnet', 'Annie', 'Eve', 5, 20)
staff.add_colleague(ws_rows, 'Cunningham', 'Devontay', 'Eve', 5, 20)
staff.add_colleague(ws_rows, 'Chalmers', 'Ritchie', 'Shopfloor', 4, 30)
staff.add_colleague(ws_rows, 'Cooper', 'Simon', 'Weekend', 2, 8)
staff.add_colleague(ws_rows, 'Carter', 'Ovince', 'Weekend', 2, 8)
staff.add_colleague(ws_rows, 'Doone', 'Perry', 'Manager', 5, 39, prev_wknd=True)
staff.add_colleague(ws_rows, 'Farmer', 'Elizabeth', 'Shopfloor', 3, 12,
                    prev_wknd=True)
staff.add_colleague(ws_rows, 'Fortuna', 'Mika', 'Warehouse', 5, 39)
staff.add_colleague(ws_rows, 'Gravely', 'Tina', 'Manager', 5, 39,
                    prev_wknd=False)
staff.add_colleague(ws_rows, 'Juniper', 'Sia', 'Tills', 4, 16)
staff.add_colleague(ws_rows, 'Krabb', 'Casey', 'Weekend', 2, 8)
staff.add_colleague(ws_rows, 'Moon', 'Jaqui', 'Tills', 3, 12)
staff.add_colleague(ws_rows, 'McPhelan', 'Jon', 'Manager', 5, 39)
staff.add_colleague(ws_rows, 'McAleer', 'George', 'Eve', 2, 8)
staff.add_colleague(ws_rows, 'McElrea', 'Sean', 'Warehouse', 2, 16)
staff.add_colleague(ws_rows, 'McClintock', 'Greg', 'Showroom', 5, 39,
                    prev_wknd=True)
staff.add_colleague(ws_rows, 'McKinty', 'Cara', 'Weekend', 2, 8)
staff.add_colleague(ws_rows, 'McKinty', 'Saoirse', 'Tills', 3, 12)
staff.add_colleague(ws_rows, 'Montgomery', 'Annie', 'Shopfloor', 5, 20)
staff.add_colleague(ws_rows, 'Montgomery', 'Cara', 'Eve', 5, 20)
staff.add_colleague(ws_rows, 'Montgomery', 'Lisa', 'Manager', 5, 39,
                    prev_wknd=True)
staff.add_colleague(ws_rows, 'Moorehouse', 'Alan', 'Shopfloor', 5, 39)
staff.add_colleague(ws_rows, "O'Hanlon", 'Neil', 'Warehouse', 2, 16)
staff.add_colleague(ws_rows, 'Roberts', 'Alexandra', 'Shopfloor', 5, 39,
                    prev_wknd=True)
staff.add_colleague(ws_rows, 'Rune', 'Jackson', 'Manager', 5, 39,
                    prev_wknd=False)
staff.add_colleague(ws_rows, 'Snell', 'Gabby', 'Showroom', 5, 39,
                    prev_wknd=False)

# With the colleagues all added to the staff object, their details added to the
# excel file and their respective rows mapped to a dictionary, the dictionary
# is pickled to allow access by main program to add generated shifts to the
# worksheet.
with open('ws_rows', 'wb') as f:
    pickle.dump(ws_rows, f)

# the staff object containing all the above colleagues is also pickled.
with open('current_staff', 'wb') as f:
    pickle.dump(staff, f)
