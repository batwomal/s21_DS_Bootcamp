import sys

def main():

  if (len(sys.argv) != 2):
    print('Wrong usage')
    return 0
  
  table = ['Name\tSurname\tE-mail\n']

  with open (sys.argv[1], 'r') as f:
    if (not f):
      print('Wrong path to file')
      return 0

    for line in f:
      fio = []
      email = line
      line = line.strip().split('@')[0]
      segmets = line.split('.')
      fio.append(segmets[0])
      fio.append(segmets[1])
      fio[0] = fio[0][0].upper() + fio[0][1:]
      fio[1] = fio[1][0].upper() + fio[1][1:]
      table.append(f'{fio[0]}\t{fio[1]}\t{email}')

  with open ('employees.tsv', 'w') as f:
    f.write(''.join(table))

if __name__ == '__main__':
  main()