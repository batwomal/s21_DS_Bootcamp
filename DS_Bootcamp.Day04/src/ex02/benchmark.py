from timeit import timeit
import sys


def list_loop_append(emails):
  new_list = []
  for email in emails:
    if '@gmail.com' in email:
      new_list.append(email)
  return new_list


def list_comprehension(emails):
  new_list = [email for email in emails if '@gmail.com' in email]
  return new_list


def list_map(emails):
  gmails = map(lambda email: email if '@gmail' in email else None, emails)
  return gmails


def list_filter(emails):
  gmails = filter(lambda email: '@gmail' in email, emails)
  return gmails


def main():
  if len(sys.argv) != 3:
    raise UnicodeDecodeError
  try:
    number_iterations = int(sys.argv[2])
  except:
    raise ValueError

  funcs = {'loop': list_loop_append,
           'list_comprehension': list_comprehension,
           'map': list_map,
           'filter': list_filter}

  if sys.argv[1] not in funcs:
    raise KeyError

  emails = [
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'
  ]

  print(timeit(lambda: funcs[sys.argv[1]](emails), number=number_iterations))


if __name__ == "__main__":
  try:
    main()
  except UnicodeDecodeError:
    sys.stderr.write(
        "Usage: python3 benchmark.py [function name] [number of iterations]\n")
  except ValueError:
    sys.stderr.write("Second argument must be an integer\n")
  except KeyError:
    sys.stderr.write(
        "First argument must be one of 'loop', 'list_comprehension', 'map', 'filter'\n")
