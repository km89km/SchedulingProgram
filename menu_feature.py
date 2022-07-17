import os
import sys
import IPython
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
                if choice == '1':  # or choice == '3':
                    outcome(populate.current_staff)
                else:
                    outcome()
            # if the user puts in an incorrect input, get() will return None and
            # they will be prompted again for a correct input.
            else:
                print(f"{choice} is not a valid choice")

    @staticmethod
    def prev_schedules():
        """Displays the previously generated shedules and opens them with the
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

    def display_staff_menu(self):
        print("""
              1. View/edit/delete colleagues. 
              2. Add colleague. 
              3. Return to main menu.
              """
              )

    def print_staff(self):
        members = [f'{index + 1}. {col.name()}' for index, col in
                   enumerate(populate.current_staff.colleagues)]
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
                # add method
                pass
            elif choice == '3':
                break
            else:
                print('Invalid choice. Please enter the number corresponding to'
                      ' your choice.')

    def col_menu(self):
        while True:
            self.print_staff()
            choice = input('Please select the number of a colleague to '
                           'continue (Press "q" to return to previous menu) : ')
            if choice.lower() == "q":
                break
            elif int(choice) in range(len(populate.current_staff.colleagues)
                                      + 1):
                self.col_details(int(choice))
            else:
                print('That was not a correct choice.')

    def col_details(self, index):
        col = populate.current_staff.colleagues[index - 1]
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
            # attrs = [atr for atr in dir(col) if not atr.startswith('__')]

    def display_col_options(self):
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


# when the module is ran directly, the main menu will be displayed to the user.
if __name__ == '__main__':
    Menu().run()
