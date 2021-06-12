#!/usr/bin/env python3
import datetime,time
from pytz import timezone

utc = timezone('utc')
t1 = datetime.datetime.now(utc)
#time.sleep(5)
t2 = datetime.datetime.now(utc)
print(t1)
print(f'{ t2 }\n----------')
print(datetime.datetime.now(utc))
fmt = '%Y-%m-%d %H:%M:%S'
d1 = datetime.datetime.strptime('2010-01-01 16:31:22', fmt)
d2 = datetime.datetime.strptime('2010-01-01 16:36:14', fmt)

diff = d2-d1
diff_minutes = diff.seconds/60
print(diff)
print(f'{int(diff_minutes)} minutes ago')
print(d1)
