
class Must_read:
  with open ("../../datasets/data.csv", "r") as file:
    print(file.read())

def main():
  Must_read

if __name__ == "__main__":
  main()