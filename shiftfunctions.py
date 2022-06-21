import random
import excel_feature as ex

# options for managers working on saturday.
saturday_options = [8, 10]
# options for weekend till staff.
wknd_options = {'Saturday': [9, 11, 13, 15],
                'Sunday': [13, 13, 14, 14]
                }
# options for weekday till staff.
till_options = {'Monday': [11, 15],
                'Tuesday': [11, 15],
                'Wednesday': [11, 15],
                'Thursday': [11, 15],
                'Friday': [11, 15],
                }


def shift_calc(output_file, work_rota, col, day, lengths, mgr_days=''):
    """Finalises shift to be added to week_dict and worksheet. Depending on the
       dept, day and length, the shift start time is decided and the shift is
       finalised."""
    if col.department == 'Weekend':
        # a start time from wknd_options is randomly selected and then removed
        # to avoid another colleague being allocated the same.
        start = random.choice(wknd_options[day])
        wknd_options[day].remove(start)

    elif col.department == 'Warehouse':
        # Mika starts at 8 everyday, whilst the others start at 10.
        if col.name() == 'Fortuna, Mika':
            start = 8
        else:
            start = 10

    elif col.department == 'Eve':
        # all eve cols start at 6pm.
        start = 18

    elif col.department == 'Showroom':
        # showroom staff start at 9 on Sunday and 10 every other day.
        if day == 'Sunday':
            start = 9
        else:
            start = 10

    elif col.department == 'Shopfloor':
        # all cols will start whenever the store opens, apart from Alan and
        # Alexandra, who start at 10 and 9, respectively.
        if day == 'Saturday':
            open_time = 8
        elif day == 'Sunday':
            open_time = 9
        else:
            open_time = 7

        if col.name() == 'Moorehouse, Alan':
            start = 10
        elif col.name() == 'Roberts, Alexandra':
            start = 9
        else:
            start = open_time

    elif col.department == 'Tills':
        # 2 till members work each day during the week, one starting at 11am and
        # the other at 3pm. Which one it will be is selected randomly and then
        # the following col will work the remaining shift.
        start = random.choice(till_options[day])
        till_options[day].remove(start)

    # the col must be a manager.
    else:
        if day == 'Sunday':
            start = 9
        elif day == 'Saturday':
            start = random.choice(saturday_options)
            saturday_options.remove(start)
        elif mgr_days[day] == 'early':
            start = 7
        elif mgr_days[day] == 'late':
            length = lengths[day]
            if length == 7:
                start = 14
            else:
                start = 13
        else:
            start = 9

    # the length of the shift is value associated with the current day in the
    # supplied length dictionary.
    length = lengths[day]
    # the relevant arguments are passed to the shift result function and the
    # resulting shift is added to the week_dict dictionary, and then the
    # add_to_worksheet function to be added to the worksheet.
    result = shift_result(work_rota, col, day, start, length)
    ex.add_to_worksheet(output_file, col.name(), day, result)


def shift_result(work_rota, col, day, start, length):
    """Creates final shift to be inputted to week_dict for each colleague."""
    # If shift longer than 6 hours then break hour needs to be
    # accounted for.
    if length > 6:
        result = f'{start} - {start + length + 1}'
        work_rota.week_dict[day][col] = result
    else:
        result = f'{start} - {start + length}'
        work_rota.week_dict[day][col] = result
    # returns resulting shift to allow easier implementation into excel output.
    return result
