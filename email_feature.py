import ezgmail

newline = "\n"


def email_rota(col, date, work_rota):
    ezgmail.send(col.email_address, f'Rota for {date}',
                 f'Hi {col.first_name},\n\n   Here are your shifts for the '
                 f'week starting {date}:\n\n'
                 f"""{newline.join(f"{day}: {shift}" for day, shift in 
                                   work_rota.colleague_rota(col).items())}"""
                 '\n\nPlease let us know if you have any questions.'
                 '\n\nAll the best,\n\n        Scheduler')
