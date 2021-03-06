import os
import sys
import IPython
import pickle
from pathlib import Path
import populate


class Menu:
    """Determines the menu interface shown to the user and allows much better
      mobility and user experience.
    """

    def __init__(self):

        # dictionary containing the relevant function/method mapped to the
        # user's choice

        self.main_options = {
            # generate new schedule
            '1': populate.populate,
            # display previously generated schedules
            '2': self.prev_schedules,
            # enter new menu to deal with staff members.
            '3': self.open_staff_menu,
            # exit program
            '4': sys.exit

        }

    @staticmethod
    def display_menu():
        """The main menu displayed to the user."""

        print("""Schedule Menu

            1. Generate new schedule
            2. View available schedules
            3. Staff Menu
            4. Quit
        """

              )

    def run(self):
        """Display the menu and respond to choices."""

        # continue to show the menu to the user until they want to quit.
        while True:
            self.display_menu()
            choice = input("Enter an option: ")
            # when the user enters a valid input, the corresponding value will
            # saved to the variable 'outcome'.
            outcome = self.main_options.get(choice)
            # as the populate method requires a staff list parameter, it is
            # added to the final function call; whereas the others only require
            # the mandatory brackets for the function call.
            if outcome:
                if choice == '1':
                    with open('current_staff', 'rb') as f:
                        current_staff = pickle.load(f)
                    outcome(current_staff)
                else:
                    outcome()
            # if the user puts in an incorrect input, get() will return None and
            # they will be prompted again for a correct input.
            else:
                print(f"{choice} is not a valid choice")

    @staticmethod
    def prev_schedules():
        """Displays the previously generated schedules and opens them with the
           designated program for handling excel worksheets.
        """
        # find all excel files in the cwd that are not the blank week template.
        results = [file for file in os.listdir(os.getcwd()) if
                   file.endswith('.xlsx') and file != 'blank_week.xlsx']
        if results:
            while True:
                print('Here are the available previous schedules:\n')
                for index, file in enumerate(results):
                    print(f'{index + 1}. {file}')
                choice = input('\nPlease select the number of previous schedule'
                               ' to open (Press "q" to return to main menu) : ')
                # return to the main menu.
                if choice == 'q':
                    return None
                # if the user enters a non-numeric input or a number greater
                # than the number of results they will be prompted again.
                try:
                    if int(choice) - 1 in range(len(results)):
                        # create the full path for the chosen excel file.
                        filename = Path(os.getcwd()) / results[int(choice) - 1]
                        # open the file with designated excel program.
                        os.startfile(filename)
                        # return to main menu.
                        return None
                except ValueError:
                    print('That was not correct. Please select the number '
                          'of previous schedule to open (Press "q" to '
                          'return to main menu) : ')
                else:
                    print('Entry was out of range. Please select the number '
                          'of previous schedule to open (Press "q" to '
                          'return to main menu) : ')

        # if there are no results then there are no saved schedules.
        print('Sorry, there are no saved schedules at the moment.')
        return None

    @staticmethod
    def display_staff_menu():
        """Displays the staff menu to the User to allow them to view and edit
           the current staff members.
        """
        print("""
              1. View/edit/delete colleagues. 
              2. Add colleague. 
              3. Return to main menu.
              """
              )

    @staticmethod
    def print_staff():
        """Prints the current staff members in 3 columnns."""
        with open('current_staff', 'rb') as f:
            current_staff = pickle.load(f)
        # pairs the colleagues with an index for the user to select. Rather than
        # starting at 0, 1 is added to the index.
        members = [f'{index + 1}. {col.name()}' for index, col in
                   enumerate(current_staff.colleagues)]
        # prints the above comprehension in 3 columns for neater viewing.
        columnized = IPython.utils.text.columnize(members)
        print(columnized)

    def open_staff_menu(self):
        """Opens a sub-menu that deals with actions that concern the staff.
           As there are only a few options, rather than use a dictionary, as
           with the main menu, a set of conditionals is used."""
        while True:
            self.display_staff_menu()
            choice = input('Please enter an option to continue : ')
            if choice == '1':
                self.col_menu()
            elif choice == '2':
                self.add_menu()
            elif choice == '3':
                break
            else:
                print('Invalid choice. Please enter the number corresponding to'
                      ' your choice.')

    def col_menu(self):
        """Displays an individual menu for the desired colleague."""
        while True:
            self.print_staff()
            with open('current_staff', 'rb') as f:
                current_staff = pickle.load(f)
            choice = input('Please select the number of a colleague to '
                           'continue (Press "q" to return to previous menu) : ')
            if choice.lower() == "q":
                break
            elif int(choice) in range(len(current_staff.colleagues)
                                      + 1):
                self.col_details(int(choice))
            else:
                print('That was not a correct choice.')

    def col_details(self, index):
        """Displays the details of the selected colleague."""
        with open('current_staff', 'rb') as f:
            current_staff = pickle.load(f)
        col = current_staff.colleagues[index - 1]
        while True:
            print(f'Last name: {col.last_name}', end='\t\t')
            print(f'First name: {col.first_name}', end='\t\t')
            print(f'Department: {col.department}', )
            print(f'Days: {col.days}', end='\t\t')
            print(f'Hours: {col.hours}', end='\t\t')
            if col.prev_wknd != '':
                print('Alternates weekends : Yes\n')
            else:
                print('Alternates weekends : No\n')
            self.display_col_options()
            return None

    @staticmethod
    def display_col_options():
        """Displays the available options with respect to the desired colleague.
        """
        while True:
            print('1. Edit\n2. Delete\n3. Exit menu\n')
            choice = int(input('what would you like to do? '))
            if choice == 1:
                print('foo')  # DISPLAY COLLEAGUE ATTRIBUTES WITH INDEX
            elif choice == 2:
                final_dec = input('Are you sure you want to delete this '
                                  'colleague? It cannot be undone. Y/N : ')
                if final_dec.upper() == 'Y':
                    print('foo')  # REMOVE COL FROM CURRENT_STAFF AND DUMP
                    # REMOVE COL FROM EXCEL AND UPDATE WS_ROWS
            elif choice == 3:
                break
            else:
                print('That was not correct.')
        return None

    @staticmethod
    def add_menu():
        """Presents the user with prompts for the individual attributes of the
           prospective colleague.
        """
        while True:
            # departments for reference to safe guard a correct assignment.
            depts = ['Manager', 'Shopfloor', 'Tills', 'Showroom',
                     'Warehouse',
                     'Eve', 'Weekend']
            first = input('First name: ').title()
            last = input('Last name: ').title()
            dept = input('Department: ').title()
            # prompts user until a valid dept is entered.
            while dept not in depts:
                print('That is not a valid department. Here are your options:')
                print(', '.join(depts))
                dept = input('Department: ').title()
            days = input('Days per week: ')
            # ensures that a correct number of days is entered.
            while not days.isnumeric() or int(days) not in range(1, 6):
                print('That is not valid. It must be between 1 and 5.')
                days = input('Days per week: ')
            days = int(days)
            hours = input('Hours per week: ')
            # ensures a valid number of hours are added.
            while not hours.isnumeric() or int(hours) not in range(4, 40):
                print('That is not valid. It must be between 4 and 39.')
                hours = input('Hours per week: ')
            hours = int(hours)
            wknd = input('Alternate weekends? (y/n): ')
            while wknd.lower() != 'y' and wknd.lower() != 'n':
                print('The value must be either "y" or "n".')
                wknd = input('Alternate weekends? (y/n): ')
            # allows the user to review their inputted details.
            print(f'\nFirst name: {first}\n'
                  f'Last name: {last}\n'
                  f'Department: {dept}\n'
                  f'Days: {days}\n'
                  f'Hours: {hours}\n'
                  f'Alternates weekends: {wknd}')
            info_check = input('Is the information correct? (y/n) ')
            if info_check.lower() == 'y':
                with open('current_staff', 'rb') as cs:
                    current_staff = pickle.load(cs)
                with open('ws_rows', 'rb') as rows:
                    ws_rows = pickle.load(rows)
                if wknd.lower() == 'y':
                    current_staff.add_colleague(ws_rows, last, first, dept,
                                                days, hours, prev_wknd=True)
                else:
                    current_staff.add_colleague(ws_rows, last, first, dept,
                                                days, hours)
                # the updated current_staff and ws_rows are updated and saved.
                with open('current_staff', 'wb') as cs:
                    pickle.dump(current_staff, cs)
                with open('ws_rows', 'wb') as rows:
                    pickle.dump(ws_rows, rows)
                break
        return None


# when the module is ran directly, the main menu will be displayed to the user.
if __name__ == '__main__':
    Menu().run()
