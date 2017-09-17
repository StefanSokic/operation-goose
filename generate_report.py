from sys import argv
from collections import Counter
import json


def object_change_text(obj_name, diff):
    if diff == 1:
        return "A single " + obj_name + " enters the frame. "
    elif diff == -1:
        return "A single " + obj_name + " leaves the frame. "
    elif diff > 1:
        return str(abs(diff)) + " " + obj_name + "s enter the frame. "
    elif diff < -1:
        return str(abs(diff)) + " " + obj_name + "s leave the frame. "


def timestamp(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print("\n[%d:%02d:%02d] " % (h, m, s), end='')

# get arguments from script
input_path = argv[1]
file_count = argv[2]
framerate = float(argv[3])


# parse json from darkflow output
frame_info = [
    json.loads(open(input_path+'/out/out' + str(i) + '.json').read())
    for i in range(1, int(file_count) + 1)
]

# store counts of objects in a dictionary for each frame
frame_objs = [[obj['label'] for obj in frame] for frame in frame_info]
frame_dicts = [dict(Counter(frame)) for frame in frame_objs]

previous_frame = {}
for i, frame in enumerate(frame_dicts):
    if frame != previous_frame:
        timestamp(framerate*i)
        for obj in set(previous_frame.keys()) | set(frame.keys()):
            frame_diff = int(frame.get(obj) or 0) \
                             - int(previous_frame.get(obj) or 0)
            if frame_diff != 0:
                print(object_change_text(obj, frame_diff), end="")
    previous_frame = frame
