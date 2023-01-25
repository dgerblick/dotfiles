#!/usr/bin/env python

import time
from datetime import datetime
import json

if __name__ == '__main__':
    while True:
        t = datetime.now()
        print(json.dumps({
            'date': t.strftime('%A, %B %-d'),
            'time': t.strftime('%-I:%M %p'),
            'us': int(t.strftime('%f')),
        }, separators=(',', ':')), flush=True)
        time.sleep(60 - (t.second + t.microsecond / 1000000.))
