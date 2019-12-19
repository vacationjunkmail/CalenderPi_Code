#!/usr/bin/env python3

row_ = ['modisa_4km_day','modisa_9km_day']
dates = ['2019-12-05','2019-12-06']
data = []
d = {}
d['start_date']='2019-12-05'
d['basename']='file 2019-12-05'
d['row_'] = 'modisa_4km_day'
data.append(d)

d = {}
d['start_date']='2019-12-06'
d['basename']='file 2019-12-06'
d['row_'] = 'modisa_4km_day'
data.append(d)

print(data)
for col in row_:
	print(col)
	col_list = []
	for d in dates:
		for row in data:
			if row['start_date'] == d and row['row_'] == col:
				col_list.append(row['basename']+" "+row['start_date'])
	print(col_list)


