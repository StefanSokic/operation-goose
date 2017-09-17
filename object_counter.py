filename = "logs.txt"

text = []

# open text file and read each line to a list
with open(filename,'r') as f:
    f.readline()
    for line in f:
        text.append(line)

# cut out the yolo info from the list
text = text[38:]

# get rid of random white space and FPS counts (left that to Peter)
lines = []
for i in text:
    words = []
    for word in i:
        if word != " ":
            words.append(word)
    line = "".join(words)
    line = line.strip('\n')
    if line != "" and line[:3] != "FPS":
        lines.append(line)

import itertools
def isplit(iterable,splitters):
    return [list(g) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]

# every time the word "Objects:" appears, we know we have a new frame, converts list to list of sublists, where
# each sublist represents a frame
frames = (isplit(lines, "Objects:"))

# strip confidence intervals bc fuk that
import re
regex = re.compile('[^a-zA-Z]')
for frame in frames:
    for index, item in enumerate(frame):
        frame[index] = regex.sub('', item)

# count how many of each object we have in each frame
from collections import Counter
counts = []
for i in frames:
    counts.append(dict(Counter(i)))


frame_num = 0
current_count = counts[frame_num]

# this gives a count of how many of each object are in the initial frame
print("Frame: 0")
print("\n")
for item, count in current_count.iteritems():
    if current_count[item]==1:
        print("    "+str(count) + " " + item + " is in the frame.")
    else:
        print("    "+str(count) + " " + item + "s are in the frame.")
    print("\n")

for next_count in counts[1:]:  # for every other frame besides the very first
    print("Frame: "+str(frame_num+1))
    print("\n")
    # check for new objects
    for item, count in next_count.iteritems():
        if item in current_count.keys() and item in next_count.keys():
            diff = next_count[item] - current_count[item]
            if diff > 0:  # items have entered the frame
                if diff==1:
                    print("    "+"A single" + " " + item + " enters the frame.")
                else:
                    print("    "+str(diff) + " " + item + "s enter the frame.")
            elif diff < 0:  # items have left the frame
                if diff==-1:
                    print("    "+"A single" + " " + item + " exits the frame.")
                else:
                    print("    "+str(abs(diff)) + " " + item + "s exit the frame.")
            #  if diff == 0, nothing has changed
    for item, count in next_count.iteritems():  # see if anything new appears
        if item not in current_count.keys():
            num = next_count[item]
            if num == 1:
                print("    "+"A single " + item + " enters the frame.")
            else:
                print("    "+str(num) + " " + item + "s enter the frame.")
                # check for objects disappearing - compares keys in current dict
    for item, count in current_count.iteritems():
        if item not in next_count.keys():
            num = current_count[item]
            if num == 1:
                print("    "+"A single " + item + " exits the frame.")
            else:
                print("    "+str(num) + " " + item + "s exit the frame")
    print("\n")
    print("    Total object count:")
    for object, count in next_count.iteritems():
        print("    "+object+"s: " + str(count))
    frame_num += 1
    current_count = counts[frame_num]
    print("\n")

print(counts)





