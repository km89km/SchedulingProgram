import os
import sys
import IPython
import pickle
import openpyxl
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
        """Prints the current staff members in 3 columns."""
        with open('current_staff', 'rb') as f:
            current_staff = pickle.load(f)
        # pairs the colleagues with an index for the user to select. Rather than
        # starting at 0, 1 is added to the index.
        members = [f'{index + 1}. {col.name()}' for index, col in
                   enumerate(current_staff.colleagues)]
        # prints the above comprehension in 3 columns for neater viewing.
        columnized = IPython.utils.text.columnize(members, displaywidth=110)
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
            print()
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
            print()
            print(f'Last name: {col.last_name}', end='\t\t')
            print(f'First name: {col.first_name}', end='\t\t')
            print(f'Department: {col.department}', )
            print(f'Days: {col.days}', end='\t\t')
            print(f'Hours: {col.hours}', end='\t\t')
            if col.prev_wknd != '':
                print('Alternates weekends : Yes\n')
            else:
                print('Alternates weekends : No\n')
            self.display_col_options(col, current_staff)
            return None

    def display_col_options(self, col, staff):
        """Displays the available options with respect to the desired colleague.
        """
        while True:
            print('1. Edit\n2. Delete\n3. Exit menu\n')
            # CATCH EXCEPTIONS
            choice = int(input('what would you like to do? '))
            if choice == 1:
                self.edit_menu(col,
                               staff)  # DISPLAY COLLEAGUE ATTRIBUTES WITH INDEX
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
    def edit_menu(col, staff):
        # have the col attrs for convenience
        options = ['last_name', 'first_name', 'department', 'hours', 'days',
                   'prev_wknd']
        # save col name to variable now as it will make finding the col's row in
        # worksheet easier, especially if changes will be made to their name.
        col_name = col.name()
        while True:
            # display the attrs for the user to see along with a number for them
            # to choose.
            print()
            for index, value in enumerate(options):
                # any attr that contains an underscore will have it removed
                # and the full name will be presented in title case.
                if '_' in value:
                    print(f'{index + 1}. {value.replace("_", " ").title()}')
                elif value == 'prev_wknd':
                    print(f'{index + 1}. Alternates Weekends')
                else:
                    print(f'{index + 1}. {value.title()}')
            choice = input('\nPlease select the number of attribute to edit '
                           '(press "q" to quit): ')
            # if user wants to go back to previous menu.
            if choice == 'q':
                break
            # if the user correctly enter a valid number we format the choice to
            # present to them so that they know they are editing the chosen
            # attribute.
            try:
                if int(choice) in range(len(options) + 1):
                    # minus 1 to have the correct index with respect
                    # to the options.
                    choice = int(choice) - 1
                    if choice == 0 or choice == 1:
                        result = options[choice].replace("_", " ").title()
                    elif choice == 5:
                        result = 'Alternates Weekends'
                    else:
                        result = options[choice].title()

                    # the user is prompted for their desired new value.
                    new_value = input(f'Please enter new value for '
                                      f'"{result}" or press "q" to exit: ')
                    if new_value == 'q':
                        break
                    elif choice == 3 or choice == 4:
                        new_value = int(new_value)
                    # the user is prompted to confirm the change.
                    check = input('Are you happy with this value ("y/n") : ')
                    if check == "y":
                        # using the setattr function, the col object has the
                        # chosen attribute changed to the new value.
                        setattr(col, options[choice], new_value)
                        # the current_staff file is modified to reflect the
                        # change.
                        with open('current_staff', 'wb') as f:
                            pickle.dump(staff, f)
                        # the row of the colleague is needed to update the blank
                        # worksheet.
                        with open('ws_rows', 'rb') as g:
                            rows = pickle.load(g)
                        # open the spreadsheet to allow modification.
                        wb = openpyxl.load_workbook('blank_week.xlsx')
                        sheet = wb.active
                        # find the col's row from the opened row dictionary
                        # based on the key being the col name.
                        col_row = rows[col_name]
                        # if the change is to the name of the col the worksheet
                        # and the ws_rows need to be modified and saved.
                        if options[choice] == 'first_name' or \
                                              options[choice] == 'last_name':
                            # Column 'A' contains the colleague names.
                            column = 'A'
                            # combine the column and row for the cell value and
                            # set it to the new name value.
                            sheet[column + str(col_row)] = col.name()
                            wb.save('blank_week.xlsx')
                            wb.close()
                            # create a new key in the row dict with the modified
                            # name, saving the previous row value.
                            rows[col.name()] = rows.pop(col_name)
                            with open('ws_rows', 'wb') as g:
                                pickle.dump(rows, g)
                        # A change to the hours value another value that
                        # requires updating the worksheet.
                        elif options[choice] == 'hours':
                            # Column 'B' contains the col's hours.
                            column = 'B'
                            sheet[column + str(col_row)] = new_value
                            wb.save('blank_week.xlsx')
                            wb.close()
                        # with a change in department, the current row of the
                        # colleague is found, deleted and then the
                        # col_to_excel() function will add the colleague to
                        # their new department.
                        elif options[choice] == 'department':
                            # find the current row of col.
                            row = rows[col_name]
                            # remove from old dept.
                            sheet.delete_rows(row)
                            wb.save('blank_week.xlsx')
                            # add col to new department. Function returns new
                            # row number and also saves the worksheet.
                            new_row = populate.shifun.ex.col_to_excel(
                                'blank_week.xlsx',
                                col, rows, row)
                            # update row_dict in ws_rows.
                            rows[col_name] = new_row
                            for key, value in rows.items():
                                print(f'{key} : {value}')
                            # save to file.
                            with open('ws_rows', 'wb') as g:
                                pickle.dump(rows, g)
                    return None
            # if a non_numeric value is entered, the exception is caught.
            except ValueError:
                print('That is not a correct value. Please try again.')
            # likewise, a number out of range will also be dealt with.
            else:
                print('That number is out of range. Please try again.')

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
