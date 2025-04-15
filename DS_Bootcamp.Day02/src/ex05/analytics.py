import sys
from random import randint
import config as co

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
      self.data = Research().file_reader(co.has_header)

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
      for i in range(0,co.num_of_steps):
        head = randint(0,1)
        tail = int(not head)
        result.append([head, tail])
      return result
    
    def predict_last(self):
      return self.data[-1]
    
    def total(self):
      return len(self.data)

    def counts_predicted(self):
      heads, tails = 0, 0
      for line in self.predict_random():
        heads += line[0]
        tails += line[1]
      return heads, tails

    def save_to_file(self, data, name_of_file, extension='txt'):
      if '.' not in name_of_file:
        name_of_file = f'{name_of_file}.{extension}'
      with open(name_of_file, 'w') as file:
        file.write(data)
