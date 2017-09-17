import subprocess

def get_length(filename):
  result = subprocess.Popen(["ffprobe", filename],
    stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
  info = [x for x in result.stdout.readlines() if "Duration" in x]
  hours = info[0][12:14]
  minutes = info[0][15:17]
  seconds = info[0][18:23]
  total = (float(hours) * 3600) + (float(minutes) * 60) + float(seconds)
  return

