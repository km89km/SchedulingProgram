import random

early_picks = []
late_picks = []


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

def manager_shift_calc(work_rota, day, daily_coverage, mgrs, staff_list):
    """determines the shifts of the managers scheduled on the provided
       day. The isolated managers are checked against a daily_coverage
       dictionary of the desired day. There must always be a manager in
       early during the week + saturday to open the store and one in later
       to close the store.
    """
    # find the managers that are working the provided day.
    # On the weekend, only 2 managers will be working. On Sundays, both
    # will work 9-6 and on Saturday, 1 will start at 8am and the other 10am.
    daily_mgrs = [man for man in mgrs if man in daily_coverage]
    if day == 'Sunday':
        for mgr in daily_mgrs:
            work_rota.week_dict['Sunday'][mgr] = '9 - 18'
        return None
    if day == 'Saturday':
        options = [8, 10]
        for mgr in daily_mgrs:
            start = random.choice(options)
            options.remove(start)
            shift_result(work_rota, mgr, day, start,
                         work_rota.week_dict[day][mgr])
        return None
    # For the weekdays, it is necessary to have one manager opening the store
    # and one closing it. This method ensures that each manager does one early
    # and one late shift and the rest will be 9 - 6.
    # First, determine the managers that haven't already been selected for an
    # early shift.
    early_options = [man for man in daily_mgrs if man not in early_picks]
    # likewise, for a late shift.
    late_options = [man for man in daily_mgrs if man not in late_picks]
    # by using the previous list comprehensions, we can make sure that every
    # manageris doing at least one early and late shift each week. As a manager
    # is selected to do either of these shifts their name will be added to the
    # picked lists and therefore the choices will diminish.
    # A check is done to see if there are available managers to fufill
    # the opening shift.
    if early_options:
        e_choice = random.choice(early_options)
        early_update(e_choice)
        # the arguments passed to this function are: colleague, day,
        # start time (7am)and shift length which is the current value associated
        # with the colleague as previously determined by the length_calc
        # function.
        shift_result(work_rota, e_choice, day, 7,
                     work_rota.week_dict[day][e_choice])
        # this manager is then removed from the choice pool.
        daily_mgrs.remove(e_choice)
    # if this clause is reached, it indicates that at least one early shift
    # needs to be fufilled but there are no available managers on that day
    # perhaps due to be scheduled a later day. The manager who hasn't done
    # an early shift is identified and their day off is switched by passing
    # them to the day_off_switch() function.
    else:
        # find the manager who hasn't done an early yet.
        missing_man = [man for man in mgrs if man not in early_picks]
        e_choice = missing_man[0]
        # change their day off and put them in as the early manager on the
        # current day. The day_off_swicth function removes the colleague from a
        # scheduled day wherecthe mgr is not already doing a early/late and
        # returns the length of that shift.
        shift_length = day_off_switch(work_rota, e_choice, staff_list)
        shift_result(work_rota, e_choice, day, 7, shift_length)

    # the same process as above is then carried out to find who will do the late
    # shifts during the weekdays.
    # if the previously chosen manager doing the early shift is in the late
    # options list, we remove them to avoid them being chosen again.
    if e_choice in late_options:
        late_options.remove(e_choice)
    if late_options:
        l_choice = random.choice(late_options)
        late_update(l_choice)
        length = work_rota.week_dict[day][l_choice]
        # if the chosen manager is doing their shorter shift, they will start
        # at 1pm or 2pm if not.
        if length == 7:
            start = 14
        else:
            start = 13
        shift_result(work_rota, l_choice, day, start,
                     work_rota.week_dict[day][l_choice])
        daily_mgrs.remove(l_choice)

    else:
        # find the manager who hasn't done a late yet.
        missing_man = [man for man in mgrs if man not in late_picks]
        l_choice = missing_man[0]
        # change their day off and put them in as the early manager on the
        # current day.
        shift_length = day_off_switch(work_rota, l_choice, staff_list)
        shift_result(work_rota, l_choice, day, 7, shift_length)

    # with the early and late shifts determined, the remaining managers will
    # work a mid shift, 9 - 6.
    for mgr in daily_mgrs:
        length = work_rota.week_dict[day][mgr]
        # if they are doing a shorter shift they will finish an hour early at
        # 5pm rather than 6pm.
        if length == 8:
            work_rota.week_dict[day][mgr] = '9 - 18'
        else:
            work_rota.week_dict[day][mgr] = '9 - 17'
    return None


def early_update(colleague):
    early_picks.append(colleague)
    return None


def late_update(colleague):
    late_picks.append(colleague)
    return None


def day_off_switch(work_rota, chosen_mgr, staff_list):
    """this function is called whenever a manager hasn't been selected
       for an early or late shift yet but is not scheduled for the desired
       day. The aim of the method is to find the day that the manager is
       scheduled for where there are the highest number of other managers
       and the manager is not already scheduled for an early or late shift
       and remove them.
    """
    # initialise dictionary to store daily manager totals.
    mgr_day_count = {}
    # iterate through days and determine total managers per day.
    for day in work_rota.days_list[1:6]:
        daily_mgrs = work_rota.day_rota(staff_list, day, 'Manager')
        # save length of daily mgrs to dictionary with day as key.
        mgr_day_count[day] = len(daily_mgrs)
    # sort dict by highest number of mgrs.
    most_mgrs = sorted(mgr_day_count.items(), key=lambda x: x[1], reverse=True)
    # find day with highest mgrs where missing man is not doing early or late
    # and remove. the function returns the length of the deleted shift to allow
    # easier reinsertion to new required day.
    for pair in most_mgrs:
        day, number = pair
        if chosen_mgr in work_rota.week_dict[day]:
            # to ensure manager not doing early or late, we check for the only
            # other options, 9 - 6 or 9 - 5.
            if work_rota.week_dict[day][chosen_mgr] == '9 - 18':
                del work_rota.week_dict[day][chosen_mgr]
                return 8
            elif work_rota.week_dict[day][chosen_mgr] == '9 - 17':
                del work_rota.week_dict[day][chosen_mgr]
                return 7


