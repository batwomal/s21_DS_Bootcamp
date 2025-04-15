import sys
import os
from random import randint

class Research:
  def __init__(self):
    self.file_path = sys.argv[1]
    with open(self.file_path, 'r') as file:
      lines = file.readlines()
      if len(lines) < 2:
        self.file_path = ""
      header = lines[0].strip().split(',')
      if len(header) != 2:
        self.file_path = ""
      for line in lines[1:]:
        elements = line.strip().split(',')
        for element in elements:
          if element.strip() not in ["0", "1"]:
            self.file_path = ""
            break

  def file_reader(self, has_header=True):
    data = []
    with open(self.file_path, "r") as file:
      start = 1 if has_header else 0
      lines = file.readlines()
      for line in lines[start:]:
        string_line = line.strip().split(',')
        dig_line = []
        for dig in string_line:
          dig_line.append(int(dig.strip()))
        data.append(dig_line)

    return data
  
  class Calculations:
    def __init__(self):
      self.data = Research().file_reader(has_header=True)

    def counts(self):
      heads, tails = 0, 0
      for line in self.data:
        heads += line[0]
        tails += line[1]
      return heads, tails

    def fractions(self):
      heads, tails = self.counts()
      total = heads + tails
      return heads / total, tails / total

  class Analytics(Calculations):
    def predict_random(self):
      result = []
      for i in range(0,3):
        head = randint(0,1)
        tail = int(not head)
        result.append([head, tail])
      return result
    
    def predict_last(self):
      return self.data[-1]


def main():
  research = Research()
  print(research.file_reader())
  calculations = research.Calculations()
  heads, tails = calculations.counts()
  fraction_heads, fraction_tails = calculations.fractions()
  print(heads,tails)
  print(fraction_heads, fraction_tails)
  analytics = research.Analytics()
  print(analytics.predict_random())
  print(analytics.predict_last())


if __name__ == "__main__":
  if (len(sys.argv) != 2 or not os.path.exists(sys.argv[1])):
    raise Exception("Wrong usage, try ../../datasets/data.csv")
  research = Research()
  if research.file_path == "":
    raise Exception("Invalid file structure or file not found.")
  else:
    main()