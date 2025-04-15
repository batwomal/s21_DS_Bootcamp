import sys
from resource import *


def read_from_file(filename):
  try:
    with open(filename, 'r') as f:
      return list(f.readlines())
  except:
    raise FileNotFoundError


def useless_loop(lst):
  for _ in lst:
    pass


def main():
  try:
    filename = sys.argv[1]
  except:
    raise IndexError
  lst = read_from_file(filename)
  useless_loop(lst)

  user_mode_time, system_mode_time, memory_usage = getrusage(RUSAGE_SELF)[:3]

  print(f'Peak Memory Usage = {memory_usage / 2 ** 20:.3f} GB')
  print(
      f'User Mode Time + System Mode Time = {user_mode_time + system_mode_time:.2f}s')


if __name__ == "__main__":
  try:
    main()
  except FileNotFoundError:
    sys.stderr.write("File not found\n")
  except IndexError:
    sys.stderr.write(
        "Wrong usage, try python3 ordinary.py ml-25m/ratings.csv\n")
