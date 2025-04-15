import sys


def generate_letter(email):
  out = 'Email not found.'
  with open('employees.tsv', 'r') as f:
    for line in f:
      parts = line.strip().split('\t')
      if len(parts) < 2:
        continue
      if (parts[2] == email):
        out = f'Dear {parts[0]}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires.'
  return out


def main():
  if len(sys.argv) != 2:
    print('Usage: python letter_generator.py <email>')
    return 0
  email = sys.argv[1]
  letter = generate_letter(email)
  print(letter)
  return 0


if __name__ == '__main__':
    main()
