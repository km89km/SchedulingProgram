Scheduling Program

When working as a team leader for a large chain hardware store, I noticed that it 
was a weekly task for one of the managers to create a schedule for the week. I saw 
this as an opportunity to create a program to automate these schedules to not
only save time and manpower but also to give the colleagues much better advance;
the schedules were made for a single week, usually with only a few days of notice.
With this program, multiple weeks could be made in advance, allowing much better
freedom for the colleagues to make plans etc.

The program is menu based and allows the user to generate a schedule for the desired
week, with the previously generated week kept track of and the user informed. When
a schedule is generated it is outputted as an excel file and can be accessed using
the view available schedules, along with any other previous schedules. There is also
a staff menu, where the user can view the colleagues, add new ones and also edit the
details of and delete existing colleagues.

Another useful feature is that when a schedule is generated, using the ezgmail module,
the colleagues with registered email addresses are automatically emailed their shifts
for the week. This feature came to mind as it was common place for colleagues to
message into the main whatsapp group asking for a photo upload of the rota. This way,
each colleague will be automatically informed.

The staffinit.py file is to be ran first to initialise the staff list and create
a current_staff and a ws_rows file (maps each colleague to a row number in the
'blank_week' excel worksheet that contains only the days and departments) in the
working directory. Afterwards, the menu_feature.py file can be ran and the program
accessed.

Other prospective features that could be incorporated are holidays for the colleagues,
an overtime feature and the automatic input of the schedule to the company's main staffing
software. Realistically to be a viable program, holidays are an important part of a business
and the logic would need to be worked out for incorporating them. During busier times of the
year, the business would have more overtime for colleagues to work beyond their contracted
hours and a feature to input this before schedule generation would be a useful addition. An
excel worksheet is an excellent way to present the weekly schedule but it should be noted that
the company that I worked for used a version of SAP to keep track of schedules. A possible idea
is to use the pyautogui module to control a manager's computer to input the generated shifts into
SAP.