#!/usr/bin/env python
#
# makeOneFile.py:  Gather up all the individual files contained in inputDir and combine them
# into a single file, filling in missing carriage returns.
#
# End time is passed as cmd arg, and process ignores records after end-time

import sys
from datetime import datetime
import os

inputDir = 'D:\\TenMinute\\'
end_time = None
time_format = '%Y%m%d%H'
file_time_format = '%Y-%m-%d %H:%M'

# Get the end-time
if len(sys.argv) > 1:
    end_time = datetime.strptime(sys.argv[1], time_format)
else:
    print 'End time required (%s)' % time_format
    exit(1)

# Output filename = end-time
with open(sys.argv[1] + '.twp', 'w') as output:
    # Walk  inputDir
    for root, dirs, files in os.walk(inputDir, topdown=False):
        for file in files:
            try:
                with open(os.path.join(root, file), 'r') as input:
                    for line in input:
                        line = line.strip()
                        if len(line) > 0:
                            time = datetime.strptime(line.split(',')[0], file_time_format)
                            if time >= end_time: continue  # Skip this record
                            output.write(line + '\n')
            except Exception as e:
                print >> sys.stderr, str(e) + " : " + os.path.join(root, file)
                continue

