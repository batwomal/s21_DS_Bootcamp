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

  company = sys.argv[1]

  if company not in COMPANIES:
    return 0

  print(STOCKS[COMPANIES[company]])  

  return 0

if __name__ == "__main__":
  main()