# This script takes all the commit messages on the interval given as parameter
# and gets the patter issue#XXX TIME XX:XX to calculate how much
# time was spent on each issue on that period
# You can pass the initial and the final dates, if not the script will generate for the last seven days

import subprocess
import re
from datetime import datetime, timedelta
import sys

now = datetime.now()
final_date = str(now.year) + "/" + str(now.month) + "/" + str(now.day)

start_date = now - timedelta(days=7)

start_date = str(start_date.year) + "/" + str(start_date.month) + "/" + str(start_date.day)

try:
    start_date = sys.argv[1]
except:
    print "using " + start_date + " as starting date"

try:
    final_date = sys.argv[2]
except:
    print "using " + final_date + " as ending date"



commit_log = subprocess.check_output(['git', 'log', '--since=' + start_date, '--until=' + final_date, '--no-merges', '--format=%B'])

regex = re.compile(r'(issue#[0-9]+)\s+TIME\s+([0-9]+):([0-9]+)')
iterator = regex.findall(commit_log)

issues = {}

for match in iterator:
    time_minutes = int(match[2]) * 60
    time_hours = int(match[1]) * 60 * 60
    total_time = time_minutes + time_hours
    try:
        issues[match[0]] += total_time
    except:
        issues[match[0]] = time_minutes + time_hours


for issue in issues:
    minutes, secconds = divmod(issues[issue], 60)
    hours, minutes = divmod(minutes, 60)
    issues[issue] = "%d:%02d:%02d" % (hours, minutes, secconds)

for issue in issues:
    print "A " + issue  + " demorou " + issues[issue]
