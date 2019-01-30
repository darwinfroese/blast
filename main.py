from collections import defaultdict
from collections import OrderedDict
import csv

with open('hockey-stats_scoring-data.csv', newline='') as csvfile:
    data = list(csv.reader(csvfile))

# remove total and header lines
data.pop(0)
del data[-1]

# data format:
# date, goal scorer, primary assist, secondary assist

for entry in data:
    # strip date
    del entry[0]

# remove all the entries that aren't goals
for idx, entry in enumerate(data):
    if entry[0] == '':
        del data[idx]

cleanedData = data

# find all the goals that were scored unassisted and remove them from the data
unassistedScorers = set()

for idx, entry in enumerate(data):
    if entry[1] == '' and entry[0] not in unassistedScorers:
        unassistedScorers.add(entry[0])
        del data[idx]

# find all the line combos that have scored (with subs and without subs)
subCombos = defaultdict(int)
fullRosterCombos = defaultdict(int)

for entry in data:
    # remove the secondary assist if it's empty
    if entry[2] == '':
        del entry[2]
    # sort since we care about who was involved, not what they did
    entry.sort()
    line = ", ".join(entry)
    if "Davis" in line or "Andy" in line or \
     "Graham" in line or "Jordan L" in line:
        subCombos[line] += 1
    else:
        fullRosterCombos[line] += 1

unassistedScorers = sorted(unassistedScorers)
# sort combos by most goals scored
sortedSubCombos = OrderedDict(sorted(subCombos.items(), key=lambda x: x[1], reverse=True))
sortedFullCombos = OrderedDict(sorted(fullRosterCombos.items(), key=lambda x: x[1], reverse=True))

# grab all 2+ combos of full roster lines
smallCombos = defaultdict(int)
data.sort(key=len)
count = 0
for entry in data:
    line = ", ".join(entry)

    # ignore the sub combinations
    if "Davis" in line or "Andy" in line or \
     "Graham" in line or "Jordan L" in line:
        continue

    if count == 0:
        smallCombos[line] += 1
    for key in list(smallCombos):
        if key in line:
            smallCombos[key] += 1
            count += 1
            break
        else:
            smallCombos[line] += 1
            count += 1
            break

sortedSmallCombos = OrderedDict(sorted(smallCombos.items(), key=lambda x: x[1], reverse=True))

print("\n\nUnassisted Goal Scorers:")
print("\n".join(unassistedScorers))

print("\n\nScoring Roster Combos:")
for key, value in sortedFullCombos.items():
    print("{:<30}\t{}".format(key, value))

print("\n\nCombos of 2+:")
for key, value in sortedSmallCombos.items():
    print("{:<30}\t{}".format(key, value))

print("\n\nSub Roster Combos:")
for key, value in sortedSubCombos.items():
    print("{:<30}\t{}".format(key, value))