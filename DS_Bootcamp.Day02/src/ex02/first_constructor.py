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

  def file_reader(self):
    with open(self.init(), "r") as file:
      text = file.read()
    return text

def main():
  print(Research().file_reader())

if __name__ == "__main__":
  if (len(sys.argv) != 2 or not os.path.exists(sys.argv[1])):
    raise Exception("Wrong usage, try ../../datasets/data.csv")
  research = Research()
  if research.init() == "":
    raise Exception("Invalid file structure or file not found.")
  else:
    main()