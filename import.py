from bs4 import BeautifulSoup
from datetime import datetime, timedelta

# FILE_IN should contain the xpath: /html/body/div[1]/div[3]/div[1]/form/div[5]/div[1]/table/tbody/tr/td/div/table/tbody/tr[5]/td/div/table/tbody
# from the list view of a myconcordia schedule
FILE_IN = 'myconcordia.html'
FILE_OUT = 'calendar.ics'


class Course():
    WEEKDAYS = {'MO': 1, 'TU': 2, 'WE': 3, 'TH': 4, 'FR': 5}
    class Event():
        def __init__(self, course_name, event):
            self.course_name = course_name
            cols = {'Nbr': -1, 'Section': -1, 'Component': -1,
                    'Times': -1, 'Room': -1, 'Instructor': -1, 'Date': -1}
            for i in range(len(event)):
                if cols.get(event[i]):
                    cols[event[i]] = i + 1
            self.nbr = event[cols['Nbr']] if event[cols['Nbr']] != 'Section' else None
            self.section = event[cols['Section']] if event[cols['Section']] != 'Component' else None
            self.component = event[cols['Component']] if event[cols['Component']] != 'Days' else None
            self.weekdays = event[cols['Times']] if event[cols['Times']] != 'Room' else None
            times = ' '.join(event[cols['Times'] + 1:cols['Times'] + 4]) if self.weekdays else None
            if times:
                self.start_time, self.end_time = times.split(' - ')
            else:
                self.start_time, self.end_time = None, None
            self.room = event[cols['Room']]
            self.instructor = ' '.join(event[cols['Instructor']:cols['Date'] - 2])
            self.start = event[cols['Date']]
            self.end = event[cols['Date'] + 2]

        def __repr__(self):
            return 'Course Name: {}\\nSection: {}\\nInstructor: {}'.format(self.course_name, self.section, self.instructor)

    def __init__(self, course):
        self.course_number, self.course_name = course[0].split(' - ')
        header = course[1].split(' Start/End Date ')
        self.start, self.end = header[-1].split(' - ')
        self.events = [self.Event(self.course_name, event.split()) for event in course[9:]]  # 1:9 is redundant data
        for i in range(len(self.events[1:])):
            if not self.events[i].nbr:
                self.events[i].nbr = self.events[i - 1].nbr
            if not self.events[i].section:
                self.events[i].section = self.events[i - 1].section
            if not self.events[i].component:
                self.events[i].component = self.events[i - 1].component

    @staticmethod
    def time_convert(time):
        in_time = datetime.strptime(time, "%I:%M%p")
        return datetime.strftime(in_time, "%H%M%S")

    @staticmethod
    def generate_r_rule(event):
        start_month, start_day, start_year = map(int, event.start.split('/'))
        start_date = datetime(start_year, start_month, start_day)
        end_month, end_day, end_year = event.end.split('/')
        weekdays = [event.weekdays[i:i + 2].upper() for i in range(0, len(event.weekdays), 2)]
        offset = Course.WEEKDAYS[weekdays[0]] - int(start_date.strftime('%w'))
        start_date += timedelta(days=offset)
        start_format = start_date.strftime('%Y%m%d')
        start_time = '{}T{}'.format(start_format, Course.time_convert(event.start_time))
        end_time = '{}T{}'.format(start_format, Course.time_convert(event.end_time))
        end_occurance = '{}{}{}T000000'.format(end_year, end_month, end_day)
        return 'DTSTART;TZID=America/New_York:{}\nDTEND;TZID=America/New_York:{}\nRRULE:FREQ=WEEKLY;UNTIL={};WKST=SU;BYDAY={}\n'.format(start_time, end_time, end_occurance, ','.join(weekdays))

    def ICS_event(self, event, alert=15):
        summary = '{} - {}'.format(self.course_number, event.component)
        description = event.__repr__()
        v_event = 'BEGIN:VEVENT\n{}{}{}END:VEVENT\n'
        content = 'SUMMARY:{}\nLOCATION:{}\nDESCRIPTION:{}\nSTATUS:CONFIRMED\n'.format(summary, event.room, description)
        r_rule = Course.generate_r_rule(event)
        v_alarm = 'BEGIN:VALARM\nTRIGGER:-P{}M\nDESCRIPTION:{}\nACTION:DISPLAY\nEND:VALARM\n'.format(alert, description)
        if alert:
            return v_event.format(content, r_rule, v_alarm)
        return v_event.format(content, r_rule, '')

    def __repr__(self):
        return '{} - {} ({} - {}):\n\t{}'.format(self.course_number, self.course_name, self.start, self.end, '\n\t'.join(map(lambda x: x.__repr__(), self.events)))


def main():
    with open(FILE_IN, 'r') as f:
        soup = BeautifulSoup(f, features='html.parser')
        schedule = soup.find_all('div', {'class': 'ui-body'})
    courses_table = [course.find_all('tr') for course in schedule]
    courses = []
    for course in courses_table:
        events = []
        for event in course:
            events.append(' '.join(event.text.split()))
        courses.append(events)
    courses = list(map(Course, courses))

    with open(FILE_OUT, 'w+') as f:
        CALENDAR_HEADER = 'BEGIN:VCALENDAR\nVERSION:2.0\nCALSCALE:GREGORIAN\n'
        f.write(CALENDAR_HEADER)
        for course in courses:
            for event in course.events:
                if event.start_time:
                    f.write(course.ICS_event(event))
        f.write('END:VCALENDAR')

if __name__ == '__main__':
    main()
