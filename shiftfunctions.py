import random


def weekend_shift_calc(work_rota, day, daily_coverage, wknd):
    """determines the shifts of the weekend staff scheduled on the provided
       day. The isolated weekend members are checked against a daily_coverage
       dictionary of the desired day. As these members cover the tills on
       Saturday and Sunday, their shifts need to be staggered to have continual
       coverage.
    """
    daily_staff = [col for col in wknd if col in daily_coverage]
    if day == 'Saturday':
        options = [9, 11, 13, 15]
        for col in daily_staff:
            start = random.choice(options)
            options.remove(start)
            shift_result(work_rota, col, day, start,
                         work_rota.week_dict[day][col])

    # if not Saturday then the day will be Sunday.
    else:
        options = [13, 13, 14, 14]
        for col in daily_staff:
            start = random.choice(options)
            options.remove(start)
            shift_result(work_rota, col, day, start,
                         work_rota.week_dict[day][col])


def warehouse_shift_calc(work_rota, day, daily_coverage, wrhse):
    """determines the shifts of the warehouse staff scheduled on the provided
       day. The isolated warehouse members are checked against a daily_coverage
       dictionary of the desired day. Mika Fortuna starts at 8 everyday to
       allow for completion of cash office checks in morning and the others
       begin at 10 and finish at 7 to cover the remaining open hours after
       Mika has finished.
    """
    daily_staff = [col for col in wrhse if col in daily_coverage]
    for col in daily_staff:
        if col == 'Fortuna, Mika':
            start = 8
        else:
            start = 10
        shift_result(work_rota, col, day, start, work_rota.week_dict[day][col])


def eve_shift_calc(work_rota, day, daily_coverage, eve):
    """determines the shifts of the evening staff scheduled on the provided
       day. The isolated evening members are checked against a daily_coverage
       dictionary of the desired day. As all members work 6 - 10, it is quite
       simple.
    """
    daily_staff = [col for col in eve if col in daily_coverage]
    for col in daily_staff:
        shift_result(work_rota, col, day, 18, work_rota.week_dict[day][col])


def showroom_shift_calc(work_rota, day, daily_coverage, shwrm):
    """determines the shifts of the showroom staff scheduled on the provided
       day. The isolated showroom members are checked against a daily_coverage
       dictionary of the desired day. Both members work 10 - 7 all days apart
       from sunday when they work 9 - 6.
    """
    daily_staff = [col for col in shwrm if col in daily_coverage]
    if day == 'Sunday':
        start = 9
    else:
        start = 10
    for col in daily_staff:
        shift_result(work_rota, col, day, start, work_rota.week_dict[day][col])


def shopfloor_shift_calc(work_rota, day, daily_coverage, shpflr):
    """determines the shifts of the shopfloor staff scheduled on the provided
       day. The isolated shopfloor members are checked against a daily_coverage
       dictionary of the desired day. All members apart from Andrew and Amanda
       start when the store opens, who start at 10 and 9 respectively, and
       everyone starts at 9 on Sunday regardless.
    """
    daily_staff = [col for col in shpflr if col in daily_coverage]
    if day == 'Saturday':
        open_time = 8
    else:
        open_time = 7
    for col in daily_staff:
        if day == 'Sunday':
            start = 9
        elif col == 'Moore, Andrew':
            start = 10
        elif col == 'Robinson, Amanda':
            start = 9
        else:
            start = open_time
        shift_result(work_rota, col, day, start, work_rota.week_dict[day][col])


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
