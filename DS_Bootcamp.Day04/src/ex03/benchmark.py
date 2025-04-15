from timeit import timeit
import sys
from functools import reduce


def loop_square_sum(num):
  sum = 0
  for i in range(1, num + 1):
    sum += i * i

  return sum


def reduce_square_sum(num):
  return reduce(lambda x, y: x + y * y, range(1, num + 1))


def main():
  if len(sys.argv) != 4:
    raise UnicodeDecodeError
  try:
    number_iterations = int(sys.argv[2])
    up_to_number = int(sys.argv[3])
  except:
    raise ValueError

  funcs = {'loop': loop_square_sum,
           'reduce': reduce_square_sum}

  if sys.argv[1] not in funcs:
    raise KeyError

  print(timeit(lambda: funcs[sys.argv[1]](
      up_to_number), number=number_iterations))


if __name__ == "__main__":
  try:
    main()
  except UnicodeDecodeError:
    sys.stderr.write(
        "Usage: python3 benchmark.py [function name] "
        "[number of iterations] [up to number]\n")
  except ValueError:
    sys.stderr.write("Second and third argument must be an integer\n")
  except KeyError:
    sys.stderr.write("First argument must be one of 'loop', 'reduce'\n")
