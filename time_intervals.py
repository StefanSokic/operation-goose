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

ts, n, ints, seconds = getText('logs.txt', 31)
createTimeSeries(ts, n, ints, seconds)