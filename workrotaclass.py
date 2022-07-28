class WorkRota:
    """Contains the shifts of the colleagues for the desired week."""

    def __init__(self):
        # simple list of the days of the week. The first day is Sunday rather
        # than Monday as the company's week starts on Sunday.
        self.days_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday',
                          'Thursday', 'Friday', 'Saturday']
        # A nested dictionary is created containing a dictionary for each day
        # of the week. This will be populated with the colleagues' shifts.
        self.week_dict = {day: {} for day in self.days_list}
        # An attribute to keep track of the current department when iterating
        # through the colleagues for shift generation.
        self.current_dept = None

    def day_rota(self, staff, day, dept=''):
        """returns the staff coverage for the desired day. An optional
           dept parameter allows for isolating the desired department.
        """
        # initialise dictionary to store day/shift pairs.
        result = {}
        # if a department is supplied, we isolate the relevant scheduled
        # colleagues by creating a list of all members in the department using
        # the group_by_dep method, checking to see which members are scheduled
        # for that day and returning their name and shift in a dictionary.
        if dept:
            dept_members = staff.group_by_dep(dept)
            avail_members = {}
            for col, shift in self.week_dict[day].items():
                if col in dept_members:
                    avail_members[col] = shift
            return avail_members
        # if no dept passed, all colleagues will be ordered by
        # earliest start time.
        day_result = sorted(self.week_dict[day].items(), key=lambda x: x[1],
                            reverse=True)
        # as sorted() function returns list of tuples, we loop through each
        # tuple, unpack them and save the result to the result dictionary.
        for colleague in day_result:
            name, shift = colleague
            result[name] = shift
        return result

    def colleague_rota(self, colleague):
        """returns the shifts for the week for each colleague."""

        # initialise dictionary to store day/shift pairs.
        result = {}
        # if colleague is scheduled for current day, the day and shift
        # are added to result dictionary.
        for day, colleagues in self.week_dict.items():
            if colleague in colleagues:
                result[day] = self.week_dict[day][colleague]
        return result

    def current_dept_update(self, colleague):
        """Sets the current department to that of the supplied colleague.
           This is called when the colleague is the first of their department.
        """
        self.current_dept = colleague.department
        return None
