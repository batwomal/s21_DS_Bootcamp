import sys

def ticker_to_company(ticker, COMPANIES):
  company = ''
  for name, symbol in COMPANIES.items():
    if symbol == ticker:
      company = name
      break
  return company

def company_to_cost(company, STOCKS, COMPANIES):
  cost = STOCKS[COMPANIES[company].upper()]
  return cost

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

  COMPANIES_UPPER = {name.upper(): name for name in COMPANIES.keys()}
  if len(sys.argv) != 2:
    return 0

  inputs = [input.strip().upper() for input in sys.argv[1].split(',') if input.strip()]
  out = []

  for input in inputs:
    if (input in COMPANIES_UPPER):
      company = ticker_to_company(input, COMPANIES)
      cost = company_to_cost(COMPANIES_UPPER[input], STOCKS, COMPANIES)
      out.append(f'{company} {input} stock price is {cost:.2f}'.strip())
    elif (input in STOCKS):
      company = ticker_to_company(input, COMPANIES)
      out.append(f'{input} is a ticker symbol for {company}')
    else:
      out.append(f'{input} is an unknown company or an unknown ticker symbol')

  print('\n'.join(out))

  return 0

if __name__ == "__main__":
  main()