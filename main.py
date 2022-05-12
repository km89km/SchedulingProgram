import datetime
import pickle
import startfunctions as startfunc
import workrotaclass
import shiftfunctions as shifun

# retrieve date for previously generated week from external file.
with open('previous_week.txt', 'r') as f:
    previous_date = f.read()

# the user is prompted for the date of the week they wish to generate, with the
# the previously generated week supplied for reference.
date_input = (input(f'What week would you like to generate? '
                    f'(The previous generated rota was {previous_date}) : '))

# the input is checked and a while loop is entered until a valid date is.
while not startfunc.valid_input(date_input):
    date_input = (input(f'What week would you like to generate? '
                        f'(Use format yyyy-mm-dd, i.e. 2022-01-01) : '))

# save current week to file to access next time program is ran.
with open('previous_week.txt', 'w') as f:
    f.write(date_input)

# correctly format inputted date to allow generation of the dates of the week.
# this will be useful later when adding the date of each day to the excel
# spreadsheet.
week_start = datetime.date.fromisoformat(date_input)
date_list = [week_start + datetime.timedelta(days=x) for x in range(7)]
day_names = [day.strftime('%A') for day in date_list]

# load staff list from pickled 'current_staff' file.
with open('current_staff', 'rb') as f:
    current_staff = pickle.load(f)

# sort colleague list in place by department. When determining the days/shifts
# of each colleague, the outcome will depend on the previous colleague and
# whether they work in the same department. The idea is to have colleagues cover
# the day(s) that their previous colleague is absent for better coverage.
current_staff.colleagues.sort(key=lambda x: x.department)

# create instance of WorkRota class to store the colleagues and their shifts
# for the week. The instance will have a initialised dictionary called week_dict
# that contains an empty sub-dictionary for each day of the week.
work_rota = workrotaclass.WorkRota()

# loop through each colleague and create their shifts for the week and
# add each daily shift to the corresponding day key in the week_dict dictionary.
# from this point going forward, when possible, the word colleague will be
# shortened to col to save space.
for col in current_staff.colleagues:
    # determines what days the colleague will work and a list of days is saved.
    days = startfunc.days_calc(work_rota, current_staff, col)
    # determines how long the shifts will be. A list of integers representing
    # each shift length is saved.
    lengths = startfunc.length_calc(col)
    # add colleagues to each day in dictionary with their name as key and
    # the shift length as value for later expansion.
    work_rota.add_to_week(col, days, lengths)

# with each day dictionary of week_dict now filled with the chosen colleagues
# and their shift lengths, the next step is to use this information to determine
# the final shifts of the colleagues.

# group departments together for easy access in functions.
mgrs = current_staff.group_by_dep('Manager')
shwrm = current_staff.group_by_dep('Showroom')
tills = current_staff.group_by_dep('Tills')
wknd = current_staff.group_by_dep('Weekend')
eve = current_staff.group_by_dep('Eve')
shpflr = current_staff.group_by_dep('Shopfloor')
wrhse = current_staff.group_by_dep('Warehouse')

for day in work_rota.days_list:
    # all scheduled colleagues are determined for the day.
    daily_coverage = work_rota.day_rota(current_staff, day)
    # colleagues_off = [col for col in staff.colleagues if
    # col not in daily_coverage]
    # for col in colleagues_off:
    # exc.add_to_spread(self.output_file, col.name(), day)
    # weekend staff are finalised first and the calculating method is only
    # ran on weekend days.
    if day == 'Saturday' or day == 'Sunday':
        shifun.weekend_shift_calc(work_rota, day, daily_coverage, wknd)
    # next are the departments that only work weekdays.
    if day in work_rota.days_list[1:6]:
        shifun.eve_shift_calc(work_rota, day, daily_coverage, eve)
        shifun.warehouse_shift_calc(work_rota, day, daily_coverage, wrhse)
        # TILLS SHIFT CALC FUNCTION
    # the remaining departments work throughout the entire week and are
    # calculated last.
    # MANAGER SHIFT CALC FUNCTION
    shifun.showroom_shift_calc(work_rota, day, daily_coverage, shwrm)
    shifun.shopfloor_shift_calc(work_rota, day, daily_coverage, shpflr)

# Display updated week_dict.
for day in work_rota.week_dict:
    print(day)
    for col, shift in work_rota.week_dict[day].items():
        print(f'{col.name()} : {shift}')
