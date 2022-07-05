import os
import sys
from pathlib import Path
import populate


class Menu:
    """Determines the menu interface shown to the user and allows much better
      mobility and user experience.
    """

    def __init__(self):

        # dictionary containing the relevant function/method mapped to the
        # user's choice

        self.options = {
            # generate new schedule
            '1': populate.populate,
            # display previously generated schedules
            '2': self.prev_schedules,
            # enter new menu to deal with staff members.
            '3': [],  # MAKE MENU FOR DEALING WITH STAFF LIST, I.E VIEW/ADD/EDIT
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
            outcome = self.options.get(choice)
            # as the populate method requires a staff list parameter, it is
            # added to the final function call; whereas the others only require
            # the mandatory brackets for the function call.
            if outcome:
                if choice == '1':
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
            print('Here are the available previous schedules:\n')
            for index, file in enumerate(results):
                print(f'{index + 1}. {file}')
            choice = input('\nPlease select the number of previous schedule to '
                           'open (Press to q to quit) : ')
            # return to the main menu.
            if choice == 'q':
                return None
            # if the user enters a non-numeric input or a number greater than
            # the number of results they will be prompted again.
            while not choice.isnumeric() or int(choice) - 1 > len(results):
                choice = input('That was not correct. Please select the number '
                               'of previous schedule to open (Press to q to '
                               'quit) : ')
                if choice == 'q':
                    return None
            # create the full path for the chosen excel file.
            filename = Path(os.getcwd()) / results[int(choice) - 1]
            # open the file with designated excel program.
            os.startfile(filename)
            # return to main menu.
            return None
        # if there are no results then there are no saved schedules.
        print('Sorry, there are no saved schedules at the moment.')
        return None


# when the module is ran directly, the main menu will be displayed to the user.
if __name__ == '__main__':
    Menu().run()
