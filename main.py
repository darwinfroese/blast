from collections import defaultdict
from collections import OrderedDict
import itertools
import csv

#######################################
# Functions
#######################################
def count_in_line(list, line):
    count = 0
    for l in list:
        if l in line:
            count += 1

    return count

#######################################
# Procedural Logic
#######################################

subs = ["Andy", "Davis", "Graham", "Jordan L"]

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
players = set()
for cd in cleanedData:
    for player in cd:
        if player not in players and player not in subs and player:
            players.add(player)
players = sorted(players)

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
    if subs[0] in line or subs[1] in line or \
     subs[2] in line or subs[3] in line:
        subCombos[line] += 1
    else:
        fullRosterCombos[line] += 1

unassistedScorers = sorted(unassistedScorers)
# sort combos by most goals scored
sortedSubCombos = OrderedDict(sorted(subCombos.items(), key=lambda x: x[1], reverse=True))
sortedFullCombos = OrderedDict(sorted(fullRosterCombos.items(), key=lambda x: x[1], reverse=True))

# generate a list of 2 player tuples
playerCombos = list(itertools.combinations(players, 2))
playerCombosAsStrings = []
for combo in playerCombos:
    playerCombosAsStrings.append(", ".join(combo))

# grab all 2+ combos of full roster lines
smallCombos = defaultdict(int)
data.sort(key=len)
count = 0
for entry in data:
    inserted = False
    line = ", ".join(entry)

    # ignore the sub combinations
    if subs[0] in line or subs[1] in line or \
     subs[2] in line or subs[3] in line:
        continue

    if count == 0:
        smallCombos[line] += 1

    for combo in playerCombos:
        line = ", ".join(combo)
        num_in_line = count_in_line(entry, line)
        if num_in_line >= 2:
            smallCombos[line] += 1
            count += 1
            inserted = True

    # for key in list(smallCombos):
    #     num_in_line = count_in_line(entry, key)
    #     if num_in_line > 1:
    #         smallCombos[key] += 1
    #         count += 1
    #         inserted = True
    #         break

    if not inserted:
        smallCombos[line] += 1

sortedSmallCombos = OrderedDict(sorted(smallCombos.items(), key=lambda x: x[1], reverse=True))

nonScoringCombos = playerCombosAsStrings
for key in list(smallCombos):
    nonScoringCombos.remove(key)

# debug information printing
# print("\n\nPlayers:")
# print("\n".join(players))

# print("\n\nPlayer Combinations:")
# for pc in playerCombos:
#     print(", ".join(pc))

print("\n\nUnassisted Goal Scorers:")
print("\n".join(unassistedScorers))

print("\n\nUnique Rostered Combos:")
for key, value in sortedFullCombos.items():
    print("{:<30}\t{}".format(key, value))

print("\n\nCombos of 2+:")
for key, value in sortedSmallCombos.items():
    print("{:<30}\t{}".format(key, value))

print("\n\nSub Roster Combos:")
for key, value in sortedSubCombos.items():
    print("{:<30}\t{}".format(key, value))

print("\n\nNon-Scoring combinations:")
print("\n".join(nonScoringCombos))