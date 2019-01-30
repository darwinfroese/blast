import csv

with open('hockey-stats_scoring-data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

data.pop(0)
del data[-1]

for entry in data:
    del entry[0]
    if entry[0] == '':
        del entry

print(data)
