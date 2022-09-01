import datetime
import random

# options for manager early/late shifts. Two lists have been opted for rather
# than having one list and saving the chosen days in another array.
early_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
late_options = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']


def valid_input(date_input):
    """Ensures that the correct format of date is supplied by the user;
       The correct format being yyyy-mm-dd.
    """
    try:
        datetime.datetime.fromisoformat(date_input)
    except ValueError:
        # if not a valid date, the user is informed and the function returns
        # False.
        if date_input.lower() == 'q':
            return None
        print(
            'Incorrect date entered. Use format yyyy-mm-dd, i.e. 2022-01-01.')
        return False
    return True

def pre_populate():
    # retrieve date for previously generated week from external file.
    with open('previous_week.txt', 'r') as f:
        previous_date = f.read()

    # the user is prompted for the date of the week they wish to generate,
    # with the the previously generated week supplied for reference.
    date_input = (input(f'What week would you like to generate? '
                        f'(The previous generated rota was {previous_date}. '
                        f'Press "q" to return to main menu.) : '))
    if date_input.lower() == 'q':
        return None

    # the input is checked and a while loop is used to verify it.
    while not valid_input(date_input):
        date_input = (input(f'What week would you like to generate? '
                            f'(Use format yyyy-mm-dd, i.e. 2022-01-01. '
                            f'Press "q" to quit.) : '))
    return date_input


def days_calc(work_rota, staff_list, col):
    """returns the days to be worked for the desired colleague."""
    # Weekend colleagues only work weekends.
    if col.department == 'Weekend':
        return ['Saturday', 'Sunday']

    # There must be 2 members of Till staff during the weekdays, and as Saoirse
    # is the last till member, she will work the 3 days that are not worked by
    # the other till members.
    elif col.name() == 'McKinty, Saoirse':
        # initialise dictionary to store days and total number of working till
        # members.
        day_totals = {}
        # find the totals for each day and save to dictionary.
        for day in work_rota.days_list[1:6]:
            daily_tills = work_rota.day_rota(staff_list, day, 'Tills')
            day_totals[day] = len(daily_tills)
        # sort the totals by lowest number of staff.
        sorted_tills = sorted(day_totals.items(), key=lambda i: i[1])
        # return the first three results. As sorted returns a list of tuples,
        # the day from the first three results are returned in a list.
        return [day_tup[0] for day_tup in sorted_tills[:3]]

    # the remaining departments will then be handled.
    # A check is done to see if the colleague alternates weekends.
    weekend_init = weekend_check(col)
    # if colleague works weekends.
    if weekend_init:
        if work_rota.current_dept == col.department:
            return same_dep_calc(work_rota, staff_list, col, weekend_init)
        # the colleague will be the first in the department.
        return new_dep_calc(work_rota, col, weekend_init)

    # if colleague doesn't work weekends.
    if work_rota.current_dept == col.department:
        # if not, check to see if previous colleague worked the 5 weekdays.
        # using this method rather than simply colleague.days is more
        # beneficial as it allows for holidays taken by the previous
        # colleague.
        return same_dep_calc(work_rota, staff_list, col)

    # if the department of the current colleague is different from the
    # current_dept we know that they are the first member of that
    # department.
    return new_dep_calc(work_rota, col)


def same_dep_calc(work_rota, staff_list, col, weekend_init=''):
    """Function to generate the weekdays of colleagues who are in the same
       department as the previously iterated colleague.
    """
    # find the index of the current colleague.
    col_index = staff_list.colleagues.index(col)
    # create a dictionary of the previous colleagues days by subtracting
    # 1 from col_index variable.
    prev_col_days = work_rota.colleague_rota(
        staff_list.colleagues[col_index - 1])
    # check to see if the previous colleague worked all 5 workdays or not.
    result = [d for d in work_rota.days_list[1:6] if d not in prev_col_days]
    # the result list will be True if the previous colleague didn't work all
    # 5 weekdays and then a check is done to see if a weekend_init argument was
    # supplied.
    if not result:
        if weekend_init:
            # Managers will be processed differently to allow designation of
            # different types of shift, saved in a dictionary.
            if col.department == 'Manager':
                mgr_days = mgr_days_setup(weekend_init)
                return mgr_days_add(col, mgr_days, work_rota.days_list[1:6])
            # the col's remaining number of days will be randomly selected and
            # added to their designated weekend day.
            weekend_init += random.sample(work_rota.days_list[1:6],
                                          col.days - 1)
            return weekend_init
        # if manager doesn't work weekends (Jon)
        if col.department == 'Manager':
            mgr_days = mgr_days_setup()
            return mgr_days_add(col, mgr_days, work_rota.days_list[1:6])
        # if col not manager and doesn't work weekends.
        return random.sample(work_rota.days_list[1:6], col.days)

    # if previous colleague didn't work all 5 weekdays.
    else:
        if weekend_init:
            if col.department == 'Manager':
                mgr_days = mgr_days_setup(weekend_init)
                # if the weekday not worked by previous manager isn't already
                # selected as an early or late shift, it is added.
                if result[0] not in mgr_days:
                    mgr_days[result[0]] = None
                return mgr_days_add(col, mgr_days, work_rota.days_list[1:6])

            # if col works fewer days than the non-worked days of previous col.
            if col.days - 1 < len(result):
                weekend_init += random.sample(result, col.days - 1)
                return weekend_init
            # if col works more days.
            elif col.days - 1 > len(result):
                result += weekend_init
                result += random.sample(
                    [d for d in work_rota.days_list[1:6] if d not in result],
                    col.days - len(result))
                return result
            # if the col requires the same number of days than non-worked days.
            else:
                weekend_init += result
                return weekend_init

        # if col doesn't work weekends and the prev col didn't work 5 weekdays.
        if col.department == 'Manager':
            mgr_days = mgr_days_setup()
            if result[0] not in mgr_days:
                mgr_days[result[0]] = None
            return mgr_days_add(col, mgr_days, work_rota.days_list[1:6])

        if col.days < len(result):
            return random.sample(result, col.days)
        elif col.days > len(result):
            result += random.sample(
                [d for d in work_rota.days_list[1:6] if d not in result],
                col.days - len(result))
            return result
        else:
            return result


def new_dep_calc(work_rota, col, weekend_init=''):
    """Function to determine the weekdays worked by a colleague if they are the
       first colleague in a department.
    """
    # update the current_dept variable to that of the current col.
    work_rota.current_dept_update(col)
    # if colleague works weekends.
    if weekend_init:
        if col.department == 'Manager':
            mgr_days = mgr_days_setup(weekend_init)
            return mgr_days_add(col, mgr_days, work_rota.days_list[1:6])
        # non-manager colleagues.
        weekend_init += random.sample(work_rota.days_list[1:6], col.days - 1)
        return weekend_init

    # if col doesn't work weekends.
    if col.department == 'Manager':
        mgr_days = mgr_days_setup()
        return mgr_days_add(col, mgr_days, work_rota.days_list[1:6])

    return random.sample(work_rota.days_list[1:6], col.days)


def weekend_check(col):
    """Function that accepts a colleague and if they have a prev_wknd attribute,
       inverts the value and initialises a list containing the relevant weekend
       day to the returned and added to later on. Returns None if the colleague
       has an empty attribute.
    """
    if col.prev_wknd:
        # change value so that following weekend is worked.
        col.prev_wknd = False
        # return a list containing only saturday to be added to later on.
        return ['Saturday']

    elif col.prev_wknd is False:
        # change value so that following weekend is not worked.
        col.prev_wknd = True
        # return a list containing only sunday to be added to later on.
        return ['Sunday']

    # if colleague has no prev_wknd attribute return None.
    else:
        return None


def length_calc(col):
    """returns the length of the colleagues' shifts."""
    # if the total hours can be spread evenly over the number of days then a
    # list containing the same shift length will be returned.
    if col.hours % col.days == 0:
        return [col.hours // col.days for _ in range(col.days)]
    # if this is not the case, there will be 3 outlying possibilities.
    # as the weekend day of specific colleagues is added first to their days
    # variable, the shorter shift is placed at the end to avoid a shorter day
    # being worked on the weekend when staff numbers are lighter.
    elif col.hours == 39:
        return [8, 8, 8, 8, 7]
    elif col.hours == 30:
        return [8, 8, 7, 7]
    elif col.hours == 16:
        return [8, 4, 4]


def mgr_days_setup(wknd_init=''):
    # a dictionary is initialised to store days.
    # rather than a list, a dictionary is employed to distinguish
    # which days of the week each manager will work early/late.
    mgr_days = {}
    # a day is selected from early options and late options and then removed to
    # avoid other managers being allocated the same day.
    e_choice = random.choice(early_options)
    # choice is given value of early to distinguish it when finalising shifts
    # later
    mgr_days[e_choice] = 'early'
    early_options.remove(e_choice)

    # to avoid possibility of having the same day being the final option of both
    # early and late lists, after the penultimate early shift is chosen, the
    # last late option that is not the remaining early one is chosen.
    if len(early_options) == 1 and early_options[0] in late_options:
        l_choice = early_options[0]
        mgr_days[l_choice] = 'late'
        late_options.remove(l_choice)
    else:
        l_choice = random.choice(late_options)
        # a while loop is used to avoid the same day being chosen for early and
        # late shifts for the same manager.
        while l_choice == e_choice:
            l_choice = random.choice(late_options)
        mgr_days[l_choice] = 'late'
        late_options.remove(l_choice)
    # weekend working managers will have their chosen weekend day
    # added to the dictionary with None value as it is non-early/late.
    if wknd_init:
        mgr_days[wknd_init[0]] = None
    return mgr_days


def mgr_days_add(col, mgr_days, days_list):
    """Adds the remaining number of weekdays to mgr_days dictionary."""
    # the desired number of days is found by subtracting the number of picked
    # days from the days worked per week.
    for i in range(col.days - len(mgr_days)):
        next_day = random.choice([day for day in days_list if day not in
                                  mgr_days])
        mgr_days[next_day] = None
    return mgr_days
