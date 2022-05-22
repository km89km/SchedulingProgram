# staffinit.py - a program that is ran once to initialise the current staff list
# to prevent adding colleagues everytime main program is ran.

import pickle
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

# the staff object containing all the above colleagues is saved to a file
# called 'current_staff' using the pickle module.
with open('current_staff', 'wb') as f:
    pickle.dump(staff, f)
