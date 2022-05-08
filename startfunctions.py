import datetime
import random


def valid_input(date_input):
    """Ensures that the correct format of date is supplied by the user;
       The correct format being yyyy-mm-dd.
    """
    # the function will attempt to format the input to the desired format.
    try:
        datetime.datetime.fromisoformat(date_input)
    except ValueError:
        # if not a valid date, the user is informed and the function returns
        # False.
        print(
            'Incorrect date entered. Use format yyyy-mm-dd, i.e. 2022-01-01.')
        return False
    return True


# noinspection PyTypeChecker
def days_calc(work_rota, staff_list, col):
    """returns the days to be worked for the desired colleague."""
    # Weekend colleagues only work weekends.
    if col.department == 'Weekend':
        return ['Saturday', 'Sunday']
    # Eve and warehouse colleagues only work weekdays but we compare
    # colleagues of the same department to fill the gaps of days off for
    # better coverage.
    elif col.department == 'Eve' or col.department == 'Warehouse':
        # check to see if the colleague is the first member of department.
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

    # the remaining departments will then be handled.
    # A check is done to see if the colleague alternates weekends.
    weekend_init = weekend_check(col)
    # the next step is to add remaining days to result list and also handle
    # colleagues who don't work weekends.
    if work_rota.current_dept == col.department:
        return same_dep_calc(work_rota, staff_list, col, weekend_init)
    # the colleague will be the first in the department.
    return new_dep_calc(work_rota, col, weekend_init)


def same_dep_calc(work_rota, staff_list, col, weekend_init=''):
    """Function to generate the weekdays of colleagues who are in the same
       department as the previously iterated colleague.
    """
    # find the index of the current colleague.
    col_index = staff_list.colleagues.index(col)
    # create a dictionary of the previous colleagues days by subtracting
    # 1 from col_index variable.
    prev_col_days = work_rota.colleague_rota(
        staff_list.colleagues[col_index - 1].name())
    # check to see if the previous colleague worked all 5 workdays or not.
    result = [d for d in work_rota.days_list[1:6] if d not in prev_col_days]
    # the result list will be True if the previous colleague didn't work all
    # 5 weekdays and then a check is done to see if a weekend_init argument was
    # supplied.
    if not result:
        if weekend_init:
            weekend_init += random.sample(work_rota.days_list[1:6],
                                          col.days - 1)
            return weekend_init
        return random.sample(work_rota.days_list[1:6], col.days)

    else:
        if weekend_init:
            if col.days - 1 < len(result):
                weekend_init += random.sample(result, col.days - 1)
                return weekend_init
            elif col.days - 1 > len(result):
                result += weekend_init
                result += random.sample(
                    [d for d in work_rota.days_list[1:6] if d not in result],
                    col.days - len(result))
                return result
            else:
                weekend_init += result
                return weekend_init

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
    work_rota.current_dept_update(col)
    if weekend_init:
        weekend_init += random.sample(work_rota.days_list[1:6], col.days - 1)
        return weekend_init
    return random.sample(work_rota.days_list[1:6], col.days)


def weekend_check(col):
    """Function that accepts a colleague and if they have a prev_wknd attribute,
       inverts the value and initialises a list containing the relevant weekend
       day to the returned and added to later on. Returns None if the colleague
       does not have the attribute.
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
    """determines the length of the colleagues' shifts."""
    if col.hours % col.days == 0:
        return [col.hours // col.days for _ in range(col.days)]
    elif col.hours == 39:
        return [8, 8, 8, 8, 7]
    elif col.hours == 30:
        return [8, 8, 7, 7]
    elif col.hours == 16:
        return [8, 4, 4]
