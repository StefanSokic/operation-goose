import itertools
import re
from collections import Counter
import subprocess

def get_length(filename):

  result = subprocess.Popen(["ffprobe", filename], stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  info = [x for x in result.stdout.readlines() if "Duration" in x]
  hours = info[0][12:14]
  minutes = info[0][15:17]
  seconds = info[0][18:23]

  total = (float(hours) * 3600) + (float(minutes) * 60) + float(seconds)

  return total

def getText(file, seconds):

    text = []

    with open(file,'r') as f:
        f.readline()
        for line in f:
            text.append(line)

    text = text[42:]

    memory = []

    for i in text:
        words = [word for word in i if word != " "]
        line = "".join(words)
        memory.append(line)

    memory = [i for i in memory if i != "\n"]

    total = 0

    ints = []
    FPScountr = [i for i in memory if i[:3] == 'FPS']
    for i in FPScountr:
        ints.append(float(i[4:]))

    ints_int = [ int(i * 10) for i in ints ]
    for i in ints_int:
        total += i

    n = len(FPScountr)

    avg_intervals = (seconds / ( total / n )) * 10
    ts = seconds / n

    return ts, n, ints, avg_intervals

def createTimeSeries(ts, n, ints, seconds):

    times = [ts] * n

    deltas = []
    for i in ints:
        change = 1 - i
        deltas.append(change)

    for i,j in enumerate(deltas):
        if j > 0 or j < 0:
            times[i] = times[i] - j
        else:
            times[i] = times[i]

    TIMES = []

    t = 0

    for i, j in enumerate(times):
        frame = t + j
        t = frame
        if t < seconds:
            TIMES.append(round(t, 2))
        else:
            TIMES.append(round(seconds, 2))

    return TIMES

def printOutput(filename, times):
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


    def isplit(iterable,splitters, times):

        return [list(g) for k,g in itertools.groupby(iterable,lambda x:x in splitters) if not k]

    # every time the word "Objects:" appears, we know we have a new frame, converts list to list of sublists, where
    # each sublist represents a frame
    frames = (isplit(lines, "Objects:", times))

    # strip confidence intervals bc fuk that

    regex = re.compile('[^a-zA-Z]')
    for frame in frames:
        for index, item in enumerate(frame):
            frame[index] = regex.sub('', item)

    # count how many of each object we have in each frame
    counts = []
    for i in frames:
        counts.append(dict(Counter(i)))

    frame_num = 0
    current_count = counts[frame_num]

    # this gives a count of how many of each object are in the initial frame
    print("Second: {}".format(times[0])) ###: replace
    print("\n")
    for item, count in current_count.items():
        if current_count[item]==1:
            print("    "+str(count) + " " + item + " is in the frame.")
        else:
            print("    "+str(count) + " " + item + "s are in the frame.")
        print("\n")

    for i, next_count in enumerate(counts[1:]):  # for every other frame besides the very first
        print("Second: "+str(times[i+1]))
        print("\n")
        # check for new objects
        for item, count in next_count.items():
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
        for item, count in next_count.items():  # see if anything new appears
            if item not in current_count.keys():
                num = next_count[item]
                if num == 1:
                    print("    "+"A single " + item + " enters the frame.")
                else:
                    print("    "+str(num) + " " + item + "s enter the frame.")
                    # check for objects disappearing - compares keys in current dict
        for item, count in current_count.items():
            if item not in next_count.keys():
                num = current_count[item]
                if num == 1:
                    print("    "+"A single " + item + " exits the frame.")
                else:
                    print("    "+str(num) + " " + item + "s exit the frame")
        print("\n")
        print("    Total object count:")
        for object, count in next_count.items():
            print("    "+object+"s: " + str(count))
        frame_num += 1
        current_count = counts[frame_num]
        print("\n")

def main():
    filename = input("Enter the text file name: ")
    video_file = input("Enter the video file name: ")
    vid_len = get_length(video_file)

    ts, n, ints, seconds = getText(filename, vid_len)
    times = createTimeSeries(ts, n, ints, vid_len)
    printOutput(filename, times)

if __name__ == '__main__':
    main()