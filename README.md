# Concordia Schedule Import

Import your concordia schedule to an ics file to be able export to any calendar app.

## Getting Started

Python is a prerequisite to running this script, see https://www.python.org/downloads/ to download.

### Prerequisites

```
$ python -m pip install requirements.txt
```

### Usage

Sign into MyConcordia at https://my.concordia.ca/psp/upprpr9/EMPLOYEE/EMPL/. Navigate to My Student Centre, then click on Weekly Schedule, List View, select the term of choice and click continue. From here, we have to copy the enclosing html table which holds each course. The absolute xpath is /html/body/div[1]/div[3]/div[1]/form/div[5]/div[1]/table/tbody/tr/td/div/table/tbody/tr[5]/td/div/table/tbody, but the easiest way to select what we need is by inputing the keyboard shortcut ctrl+shift+c, placing the cursor just below List View, Weekly Calendar View and View in Class Schedule Builder, such that each class is highlighted blue, and expanding the resulting html in the Elements tab on the right until we reach the required xpath. (Note: If you hover on an element, it will highlight the corresponding html element on the page. Use this in order to reach the correct <tbody> element). Once selected, right click and Copy element, and paste the contents in myconcordia.html. We can then run import.py, and the output calendar.ics can be manually imported into Google Calendar, or any calendar app of your choice.