import excel_feature as ex


class Staff:
    """A class to represent the collective staff comprised of
       colleague objects.
    """

    def __init__(self):
        # list of colleagues making up the staff.
        self.colleagues = []

    # search for colleague

    def add_colleague(self, row_dict, last_name, first_name, dept, days, hours,
                      prev_wknd=''):
        col = Colleague(last_name, first_name, dept, days, hours, prev_wknd)
        row = ex.col_to_excel('blank_week.xlsx', col, row_dict)
        row_dict[col.name()] = row
        self.colleagues.append(col)

    def print_staff_list(self):
        [print(f'{colleague.name()}') for colleague in self.colleagues]

    # method for grouping colleagues by department.
    def group_by_dep(self, dep):
        # a list of colleagues is returned if their department attribute
        # matches the supplied argument.
        return [col for col in self.colleagues if col.department == dep.title()]


class Colleague:
    """Models each individual colleague in the working staff."""

    def __init__(self, last_name, first_name, department, days, hours,
                 prev_wknd=''):
        self.last_name = last_name
        self.first_name = first_name
        self.department = department
        self.days = days
        self.hours = hours
        self.prev_wknd = prev_wknd

    def name(self):
        """Returns the name of the colleague object, last name first."""
        return f'{self.last_name}, {self.first_name}'
