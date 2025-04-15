def main():
  table = []
  with open('../../datasets/ds.csv', 'r') as f:
    for line in f:
      row = []
      current_field = ""
      in_quotes = False

      for char in line.strip():
        if char == '"':
          in_quotes = not in_quotes
        elif char == ',' and not in_quotes and current_field == "":
          continue
        elif char == ',' and not in_quotes:
          row.append(current_field)
          current_field = ""
        else:
          current_field += char
      row.append(current_field)
      table.append(row)

  with open('ds.tsv', 'w') as f:
    for row in table:
      f.write('\t'.join(row) + '\n')

  return 0
  
if __name__ == "__main__":
  main()