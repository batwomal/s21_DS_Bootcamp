import sys
from resource import *


def read_from_file_generator(filename):
  try:
    with open(filename, 'r') as f:
      for line in f:
        yield line
  except:
    raise FileNotFoundError


def useless_loop(filename):
  for _ in read_from_file_generator(filename):
    pass


def main():
  try:
    filename = sys.argv[1]
  except:
    raise IndexError

  useless_loop(filename)

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
