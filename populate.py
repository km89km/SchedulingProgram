import datetime
import pickle
from importlib import reload
import startfunctions as startfunc
import workrotaclass
import shiftfunctions as shifun

# from timeit import default_timer as timer

# load staff list from pickled 'current_staff' file.
with open('current_staff', 'rb') as f:
    current_staff = pickle.load(f)


def populate(current_staff):
    reload(shifun)
    reload(startfunc)
    # retrieve date for previously generated week from external file.
    with open('previous_week.txt', 'r') as f:
        previous_date = f.read()

    # the user is prompted for the date of the week they wish to generate,
    # with the the previously generated week supplied for reference.
    date_input = (input(f'What week would you like to generate? '
                        f'(The previous generated rota was {previous_date}. '
                        f'Press "q" to quit.) : '))

    # start = timer()

    # the input is checked and a while loop is used to verify it.
    while not startfunc.valid_input(date_input):
        date_input = (input(f'What week would you like to generate? '
                            f'(Use format yyyy-mm-dd, i.e. 2022-01-01. '
                            f'Press "q" to quit.) : '))

    # save current week to file to access next time program is run.
    with open('previous_week.txt', 'w') as f:
        f.write(date_input)

    # correctly format inputted date to allow generation of the dates of the
    # week. this will be useful later when adding the date of each day to the
    # excel worksheet.
    week_start = datetime.date.fromisoformat(date_input)
    date_list = [week_start + datetime.timedelta(days=x) for x in range(7)]

    # the dates of each day are added to the blank worksheet.
    output_file = shifun.ex.date_adder('blank_week.xlsx', date_list)

    # sort colleague list in place by department. When determining the
    # days/shifts of each colleague, the outcome will depend on the previous
    # colleague and whether they work in the same department. The idea is to
    # have colleagues cover the day(s) that their previous colleague is
    # absent for better coverage.
    current_staff.colleagues.sort(key=lambda x: x.department)

    # create instance of WorkRota class to store the colleagues and their
    # shifts for the week. The instance will have a initialised dictionary
    # called week_dict that contains an empty sub-dictionary for each day of
    # the week.
    work_rota = workrotaclass.WorkRota()

    # loop through each colleague and create their shifts for the week and
    # add each daily shift to the corresponding day key in the week_dict
    # dictionary. from this point going forward, when possible, the word
    # colleague will be shortened to col to save space.
    for col in current_staff.colleagues:
        # determines what days the col will work and a list of days is saved.
        days = startfunc.days_calc(work_rota, current_staff, col)
        # determines how long the shifts will be. A list of integers
        # representing each shift length is saved.
        lengths = startfunc.length_calc(col)
        # join days and lengths together in a dictionary for easier shift
        # finalisation in next section.
        # Regarding the managers, the days variable above will be a dictionary
        # rather than a list so a list of just the worked days is used.
        if col.department == 'Manager':
            day_lengths = dict(zip(list(days), lengths))
        else:
            day_lengths = dict(zip(days, lengths))

        # the shifts need to be finalised and added first to the week_dict of
        # the work rota instance and then to the worksheet.
        for day in work_rota.days_list:
            # if the colleague is not scheduled for the current day, an 'O'
            # will be placed in place of a shift in the worksheet.
            if day not in days:
                shifun.ex.add_to_worksheet(output_file, col.name(), day)
            else:
                if col.department == 'Manager':
                    shifun.shift_calc(output_file, work_rota, col, day,
                                      day_lengths,
                                      days)
                else:
                    shifun.shift_calc(output_file, work_rota, col, day,
                                      day_lengths)

    # save the staff list to file to ensure that colleagues who worked the
    # weekend will have the following one off.
    with open('current_staff', 'wb') as f:
        pickle.dump(current_staff, f)

    return None


# end = timer()
# print(end - start)
