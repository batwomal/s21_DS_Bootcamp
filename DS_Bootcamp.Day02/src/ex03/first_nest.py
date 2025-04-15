
import sys
import os

class Research:
  def init(self):
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
      lines = file.readlines()
      if len(lines) < 2:
        file_path = ""
      header = lines[0].strip().split(',')
      if len(header) != 2:
        file_path = ""
      for line in lines[1:]:
        elements = line.strip().split(',')
        for element in elements:
          if element.strip() not in ["0", "1"]:
            file_path = ""
            break
    return file_path

  def file_reader(self, has_header=True):
    data = []
    with open(self.init(), "r") as file:
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
    def counts(self):
      heads, tails = 0, 0
      data = Research().file_reader(has_header=True)
      for line in data:
        heads += line[0]
        tails += line[1]
      return heads, tails

    def fractions(self):
      heads, tails = self.counts()
      total = heads + tails
      return heads / total, tails / total

def main():
  research = Research()
  print(research.file_reader())
  calculations = research.Calculations()  # Создаем экземпляр Calculations
  heads, tails = calculations.counts()
  fraction_heads, fraction_tails = calculations.fractions()
  print(heads,tails)
  print(fraction_heads, fraction_tails)

if __name__ == "__main__":
  if (len(sys.argv) != 2 or not os.path.exists(sys.argv[1])):
    raise Exception("Wrong usage, try ../../datasets/data.csv")
  research = Research()
  if research.init() == "":
    raise Exception("Invalid file structure or file not found.")
  else:
    main()