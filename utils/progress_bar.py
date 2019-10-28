import time
import random
import sys

def display(res_time, value, endvalue, bar_length=20):
        percent = float(value) / endvalue
        arrow = '-' * int(round(percent * bar_length)-1) + '>'
        spaces = ' ' * (bar_length - len(arrow))

        sys.stdout.write("\rPercent: [{0}] {1}% ({2} seconds)".format(arrow + spaces, int(round(percent * 100)), res_time))
        sys.stdout.flush()

def progress_bar(max_sleep_time = 5):
  res_time = random.randrange(1, max_sleep_time + 1)
  
  for i in range(0, res_time):
    display(res_time, (max_sleep_time/res_time) * (i + 1), max_sleep_time)
    time.sleep(1)

  sys.stdout.write('\n\n\n')
