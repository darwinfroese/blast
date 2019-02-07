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

def filter_out_data(list):
    if list[0] == '':
        return False
    elif list[0] and list[0] in subs:
        return False
    elif list[1] and list[1] in subs:
        return False
    elif list[2] and list[2] in subs:
        return False

    return True

def check_unassisted(list):
    if list[1] == '':
        return True

    return False

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
    entry.pop(0)

# remove all the entries that aren't goals and all entries
# that involve a sub

cleanedData = [e for e in data if filter_out_data(e)]

players = set()
for cd in cleanedData:
    for player in cd:
        if player not in players and player not in subs and player:
            players.add(player)
players = sorted(players)

# find all the goals that were scored unassisted and remove them from the data
unassistedEntries = [e for e in cleanedData if check_unassisted(e)]
cleanedData = [e for e in cleanedData if not check_unassisted(e)]

unassistedScorers = set()
for entry in unassistedEntries:
    unassistedScorers.add(entry[0])

# find all primary assists
primaryAssistCount = 0
primaryAssists = defaultdict(int)
for entry in cleanedData:
    player = entry[1]
    primaryAssists[player] += 1
    primaryAssistCount += 1

primaryAssists = OrderedDict(sorted(primaryAssists.items(), key=lambda x: x[1], reverse=True))

# find all the line combos that have scored (with subs and without subs)
subCombos = defaultdict(int)
fullRosterCombos = defaultdict(int)

for entry in cleanedData:
    # remove the secondary assist if it's empty
    if entry[2] == '':
        del entry[2]
    # sort since we care about who was involved, not what they did
    entry.sort()
    line = ", ".join(entry)
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
cleanedData.sort(key=len)
count = 0
for entry in cleanedData:
    inserted = False
    line = ", ".join(entry)

    if count == 0:
        smallCombos[line] += 1

    for combo in playerCombos:
        line = ", ".join(combo)
        num_in_line = count_in_line(entry, line)
        if num_in_line >= 2:
            smallCombos[line] += 1
            count += 1
            inserted = True

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

print("\n\nPrimary Assist Totals:")
for key, value in primaryAssists.items():
    percent = (value / primaryAssistCount) * 100
    print("{:<30}\t{}\t({:.2f}%)".format(key,value,percent))

print("\n\nUnassisted Goal Scorers:")
print("\n".join(unassistedScorers))

print("\n\nUnique Rostered Combos:")
for key, value in sortedFullCombos.items():
    print("{:<30}\t{}".format(key, value))

print("\n\nCombos of 2+:")
for key, value in sortedSmallCombos.items():
    print("{:<30}\t{}".format(key, value))

print("\n\nNon-Scoring combinations:")
print("\n".join(nonScoringCombos))