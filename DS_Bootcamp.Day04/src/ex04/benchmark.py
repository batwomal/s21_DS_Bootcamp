from timeit import timeit
import random
from collections import Counter


def generate_list():
  return [random.randint(0, 100) for _ in range(1000000)]


def list_to_dict_counter(lst):
  return dict(Counter(lst))


def list_to_dict_my(lst):
  counts = {i: 0 for i in range(101)}
  for num in lst:
    counts[num] += 1
  return counts


def counter_top_10(lst):
  return list(dict(Counter(lst).most_common(10)).keys())


def my_top_10(lst):
  counts = list_to_dict_my(lst)
  sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
  return [item[0] for item in sorted_items[:10]]


def main():
  rand_list = generate_list()

  time_counter = timeit(lambda: list_to_dict_counter(rand_list), number=1)
  time_my = timeit(lambda: list_to_dict_my(rand_list), number=1)

  time_counter_top_10 = timeit(lambda: counter_top_10(rand_list), number=1)
  time_my_top_10 = timeit(lambda: my_top_10(rand_list), number=1)

  print(f"my function: {time_my:.6f}\nCounter: {time_counter:.6f}")
  print(f"my top 10: {time_my_top_10:.6f}\nCounter's top 10: {
        time_counter_top_10:.6f}")


if __name__ == "__main__":
  main()
