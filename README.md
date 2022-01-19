# Concordia Schedule Export

Export your concordia schedule to an ics file for import to any calendar app in a *quick and dirty* way.

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
  - The absolute xpath is `/html/body/div[1]/div[3]/div[1]/form/div[5]/div[1]/table/tbody/tr/td/div/table/tbody/tr[5]/td/div/table`
  - **The easiest way to select what we need is by openning dev tools and searching the page source (`ctrl+F`) for the above path.**
4. Once selected, right click > Copy > Inner HTML (or something similar), and paste the contents into `myconcordia.html`.
5. Run the script via `python export.py`
  - The output calendar.ics can be manually imported into Google Calendar, or any other calendar app of choice.
