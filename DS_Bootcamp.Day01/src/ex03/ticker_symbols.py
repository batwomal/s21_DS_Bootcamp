import sys

def main():

  COMPANIES = {
    'Apple': 'AAPL',
    'Microsoft': 'MSFT',
    'Netflix': 'NFLX',
    'Tesla': 'TSLA',
    'Nokia': 'NOK'
    }

  STOCKS = {
    'AAPL': 287.73,
    'MSFT': 173.79,
    'NFLX': 416.90,
    'TSLA': 724.88,
    'NOK': 3.37
    }

  if len(sys.argv) != 2:
    return 0

  ticker = sys.argv[1].upper()

  if ticker not in STOCKS:
    return 0

  company_name = ''
  for name, symbol in COMPANIES.items():
      if symbol == ticker:
          company_name = name
          break
  print(f'{company_name} {STOCKS[ticker]}')

  return 0


if __name__ == "__main__":
  main()