class Research:
  def file_reader():
    with open ("../../datasets/data.csv", "r") as file:
      text = file.read()
    return text

def main():
  print(Research.file_reader())

if __name__ == "__main__":
  main()