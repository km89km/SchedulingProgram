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


def tills_shift_calc(work_rota, day, daily_coverage, tills, staff):
    """determines the shifts of the tills staff scheduled on the provided
       day. The isolated tills members are checked against a daily_coverage
       dictionary of the desired day. 2 members are scheduled every weekday
       to allow for full coverage from 11 to close (Andrea or other shopfloor
       member will cover desk from 9 to 11). If there is not 2 members scheduled
       for a day, the till_shuffle method will correct this issue.
    """
    daily_staff = [col for col in tills if col in daily_coverage]
    if len(daily_staff) != 2:
        till_shuffle(work_rota, staff)
        daily_coverage = work_rota.day_rota(staff, day, 'Tills')
        daily_staff = [col for col in tills if col in daily_coverage]
    options = [11, 15]
    for col in daily_staff:
        start = random.choice(options)
        options.remove(start)
        shift_result(work_rota, col, day, start,
                     work_rota.week_dict[day][col])


def till_shuffle(work_rota, staff):
    """method that is called if there is not an even distribution of
       till staff throughout the week. After going through the week
       days and tallying the total number of till staff in each day, the
       totals are sorted and one is removed from the day with most and
       added to the day with least.
    """
    # initialise dict to store totals.
    day_totals = {}
    for day in work_rota.days_list[1:6]:
        # Find the till staff present for each day.
        daily_tills = work_rota.day_rota(staff, day, 'Tills')
        # save number of till staff to dictionary with day as key.
        day_totals[day] = len(daily_tills)
    # sort dict by highest number of colleagues.
    most_tills = sorted(day_totals.items(), key=lambda i: i[1], reverse=True)
    # the day with most will be the first member and the least will be the last.
    daymost, x = most_tills[0]
    dayleast, y = most_tills[-1]
    # find the colleagues not scheduled for the day with least colleagues.
    most_coverage = work_rota.day_rota(staff, daymost, 'Tills')
    least_coverage = work_rota.day_rota(staff, dayleast, 'Tills')
    difference = [col for col in most_coverage if col not in least_coverage]
    # the first colleague will be removed from the day with most.
    chosen_till = difference[0]
    del work_rota.week_dict[daymost][chosen_till]
    # the next step is to then add the same colleague to the day with least.
    work_rota.week_dict[dayleast][chosen_till] = 4


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
