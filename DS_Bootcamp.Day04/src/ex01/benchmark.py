from timeit import timeit


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


def main():
  number_iterations = 90000000
  emails = [
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com',
      'john@gmail.com', 'james@gmail.com', 'alice@yahoo.com', 'anna@live.com', 'philipp@gmail.com'
  ]

  time_append = timeit(lambda: list_loop_append(emails),
                       number=number_iterations)
  time_comprehension = timeit(
      lambda: list_comprehension(emails), number=number_iterations)
  time_map = timeit(lambda: list_map(emails), number=number_iterations)

  time_dict = {'loop': time_append,
               'list comprehension': time_comprehension, 'map': time_map}

  time_dict = {key: value for key, value in sorted(
      time_dict.items(), key=lambda item: float(item[1]))}

  best_method = list(time_dict.keys())[0]
  methods_time = [str(value) for value in time_dict.values()]

  print('It is better to use a', best_method)
  print(' vs '.join(methods_time))


if __name__ == "__main__":
  main()
