from sys import argv
from collections import Counter
import json

from visuals import graph


JSON_PATH = 'output/log.json'
LOG_PATH = 'output/log.txt'


def object_change_text(obj_name, diff):
    if diff == 1:
        return "A single " + obj_name + " enters the frame. "
    elif diff == -1:
        return "A single " + obj_name + " leaves the frame. "
    elif diff > 1:
        return str(abs(diff)) + " " + obj_name + "s enter the frame. "
    elif diff < -1:
        return str(abs(diff)) + " " + obj_name + "s leave the frame. "


def timestamp(seconds, log):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    log.write("\n[%d:%02d:%02d] " % (h, m, s))


# get arguments from script
input_path = argv[1]
file_count = argv[2]
framerate = float(argv[3])


# parse json from darkflow output
frame_info = [
    json.loads(open(input_path+'/out/out' + str(i) + '.json').read())
    for i in range(1, int(file_count) + 1)
]

# output raw json into log file
json_log = open(JSON_PATH, 'w')
json_log.write(json.dumps([list(tup) for tup in enumerate(frame_info)],
                          indent=4))
json_log.close()

# store counts of objects in a dictionary for each frame
frame_objs = [[obj['label'] for obj in frame] for frame in frame_info]
frame_dicts = [dict(Counter(frame)) for frame in frame_objs]

# open log file for writing
text_log = open(LOG_PATH, 'w')

previous_frame = {}
for i, frame in enumerate(frame_dicts):
    if frame != previous_frame:
        timestamp(framerate*i, text_log)
        for obj in set(previous_frame.keys()) | set(frame.keys()):
            frame_diff = int(frame.get(obj) or 0) \
                             - int(previous_frame.get(obj) or 0)
            if frame_diff != 0:
                text_log.write(object_change_text(obj, frame_diff))
    previous_frame = frame

text_log.close()


# create graph and csv
graph(frame_dicts)
