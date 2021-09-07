# Concordia Schedule Import

Import your concordia schedule to an ics file for export to any calendar app.

## Getting Started

Python is a prerequisite to running this script, see [the docs](https://www.python.org/downloads/) for download instructions.

## Prerequisites

```bash
$ python -m pip install -r requirements.txt
```

## Usage

1. Sign into [MyConcordia](https://my.concordia.ca/).
2. Navigate to My Student Centre, then click on Class Schedule > List View > select term of choice > Continue.
3. Copy the enclosing html table which holds each course.
  - The absolute xpath is `/html/body/div[1]/div[3]/div[1]/form/div[5]/div[1]/table/tbody/tr/td/div/table/tbody/tr[5]/td/div/table/tbody`
	- The easiest way to select what we need is by inputing the keyboard shortcut `ctrl+shift+c`, placing the cursor just below List View, Weekly Calendar View and View in Class Schedule Builder, such that each class is highlighted blue, and expanding the resulting html in the Elements tab on the right until we reach the required xpath.
    - **Note: If you hover on an element, it will highlight the corresponding html element on the page. Use this in order to reach the correct `<tbody>` element).**
4. Once selected, right click > Copy > Copy element, and paste the contents in myconcordia.html.
5. Run the script via `python import.py`
  - The output calendar.ics can be manually imported into Google Calendar, or any other calendar app of choice.
