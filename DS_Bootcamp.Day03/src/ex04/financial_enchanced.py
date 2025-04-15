import sys
import os
from bs4 import BeautifulSoup
import httpx
import cProfile
import io
from contextlib import redirect_stdout
import pstats

def checks():
  if len(sys.argv) != 3:
    raise Exception('Wrong usage, try "MSFT" "Cost of Revenue"')
  if not sys.argv[1] or not sys.argv[2]:
    raise Exception('Wrong usage, try "MSFT" "Cost of Revenue"')
  if 'VIRTUAL_ENV' not in os.environ:
    raise Exception(
        "This script must be run inside a virtual environment.\n"
        "Try: source ../ex02/batwomalv/bin/activate")

def get_response():
  cookies = {
      'GUCS': 'AVR6XKfm',
      'A3': 'd=AQABBP2kj2cCEObOpyyaMTRn3INjhLmd908FEgABCAHwkGe4Z-2Nb2UB9qMAAAcI8aSPZ4C87Q0&S=AQAAAm2MbI5GD2p-BwFUfyN0FVA',
      'GUC': 'AQABCAFnkPBnuEIhPQSr&s=AQAAAJb_fI5b&g=Z4-lBw',
      'A1S': 'd=AQABBP2kj2cCEObOpyyaMTRn3INjhLmd908FEgABCAHwkGe4Z-2Nb2UB9qMAAAcI8aSPZ4C87Q0&S=AQAAAm2MbI5GD2p-BwFUfyN0FVA',
      'A1': 'd=AQABBP2kj2cCEObOpyyaMTRn3INjhLmd908FEgABCAHwkGe4Z-2Nb2UB9qMAAAcI8aSPZ4C87Q0&S=AQAAAm2MbI5GD2p-BwFUfyN0FVA',
      'EuConsent': 'CQLlOMAQLlOMAAOACBNLBZFoAP_gAEPgACiQKptB9G7WTXFneXp2YPskOYUX0VBJ4MAwBgCBAcABzBIUIBwGVmAzJEyIICACGAIAIGBBIABtGAhAQEAAYIAFAABIAEgAIBAAIGAAACAAAABACAAAAAAAAAAQgEAXMBQgmAZEBFoIQUhAggAgAQAAAAAEAIgBCgQAEAAAQAAICAAIACgAAgAAAAAAAAAEAFAIEQAAIAECAotkdQAAAAAAAAAAAAAACAABAAAAAIKpgAkGpUQBFgSEhAIGEECAEQUBABQIAgAACBAAAATBAUIAwAVGAiAEAIAAAAAAAAACABAAABAAhAAEAAQIAAAAAIAAgAIBAAACAAAAAAAAAAAAAAAAAAAAAAAAAGIBQggABABBAAQUAAAAAgAAAAAAAAAIgACAAAAAAAAAAAAAAIgAAAAAAAAAAAAAAAAAAIAAAAIAAAAgBEFgAAAAAAAAAAAAAACAABAAAAAIAAA',
      'PRF': 't%3DMSFT',
      'cmp': 't=1737467134&j=1&u=1---&v=63',
      'axids': 'gam=y-gCZF0qlE2uJ8RBgeFchDWJGuNIqL4ayj~A&dv360=eS1kSWwxY0FaRTJ1RkllRHRfSXFrVVhLb3dlQ0cuZFNYeH5B&ydsp=y-G80CsJBE2uKiTnT1vWo4JSLjfg3beLWT~A&tbla=y-5vDPyXFE2uLWJnUsgSkXGT7cIXh.L_ka~A',
      'tbla_id': '76df6fc8-5dec-431c-a383-d0f43a66208d-tucte892a87',
  }

  headers = {
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
      'cache-control': 'max-age=0',
      # 'cookie': 'GUCS=AVR6XKfm; A3=d=AQABBP2kj2cCEObOpyyaMTRn3INjhLmd908FEgABCAHwkGe4Z-2Nb2UB9qMAAAcI8aSPZ4C87Q0&S=AQAAAm2MbI5GD2p-BwFUfyN0FVA; GUC=AQABCAFnkPBnuEIhPQSr&s=AQAAAJb_fI5b&g=Z4-lBw; A1S=d=AQABBP2kj2cCEObOpyyaMTRn3INjhLmd908FEgABCAHwkGe4Z-2Nb2UB9qMAAAcI8aSPZ4C87Q0&S=AQAAAm2MbI5GD2p-BwFUfyN0FVA; A1=d=AQABBP2kj2cCEObOpyyaMTRn3INjhLmd908FEgABCAHwkGe4Z-2Nb2UB9qMAAAcI8aSPZ4C87Q0&S=AQAAAm2MbI5GD2p-BwFUfyN0FVA; EuConsent=CQLlOMAQLlOMAAOACBNLBZFoAP_gAEPgACiQKptB9G7WTXFneXp2YPskOYUX0VBJ4MAwBgCBAcABzBIUIBwGVmAzJEyIICACGAIAIGBBIABtGAhAQEAAYIAFAABIAEgAIBAAIGAAACAAAABACAAAAAAAAAAQgEAXMBQgmAZEBFoIQUhAggAgAQAAAAAEAIgBCgQAEAAAQAAICAAIACgAAgAAAAAAAAAEAFAIEQAAIAECAotkdQAAAAAAAAAAAAAACAABAAAAAIKpgAkGpUQBFgSEhAIGEECAEQUBABQIAgAACBAAAATBAUIAwAVGAiAEAIAAAAAAAAACABAAABAAhAAEAAQIAAAAAIAAgAIBAAACAAAAAAAAAAAAAAAAAAAAAAAAAGIBQggABABBAAQUAAAAAgAAAAAAAAAIgACAAAAAAAAAAAAAAIgAAAAAAAAAAAAAAAAAAIAAAAIAAAAgBEFgAAAAAAAAAAAAAACAABAAAAAIAAA; PRF=t%3DMSFT; cmp=t=1737467134&j=1&u=1---&v=63; axids=gam=y-gCZF0qlE2uJ8RBgeFchDWJGuNIqL4ayj~A&dv360=eS1kSWwxY0FaRTJ1RkllRHRfSXFrVVhLb3dlQ0cuZFNYeH5B&ydsp=y-G80CsJBE2uKiTnT1vWo4JSLjfg3beLWT~A&tbla=y-5vDPyXFE2uLWJnUsgSkXGT7cIXh.L_ka~A; tbla_id=76df6fc8-5dec-431c-a383-d0f43a66208d-tucte892a87',
      'priority': 'u=0, i',
      'referer': 'https://consent.yahoo.com/',
      'sec-ch-ua': '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0',
  }
  
  response = httpx.get(f'https://finance.yahoo.com/quote/{sys.argv[1].upper()}/financials/', cookies=cookies, headers=headers)
  if response.status_code != 200:
    raise Exception('Wrong URL')
  return response

def parse_data(response):
  soup = BeautifulSoup(response.text, 'html.parser')
  soup = soup.find(title=f'{sys.argv[2]}')
  if not soup:
    raise Exception('Wrong URL')
  soup = soup.find_parent()
  table = (soup.get_text().strip(),)
  soup = soup.find_next_siblings()
  for sibling in soup:
    value = sibling.get_text().strip()
    if value.endswith('.00'):
      value = value[:-3]
    table += (value,)
  return table

def main():
  checks()
  print('Wait for a few seconds')
  # time.sleep(5)
  print(parse_data(get_response())) 
  return 0


if __name__ == '__main__':
  profiler = cProfile.Profile()
  profiler.enable()
  
  main() 
  
  profiler.disable()
  s = io.StringIO()
  with redirect_stdout(s):
    profiler.print_stats(sort='tottime')
    with open('profiling-http.txt', 'w') as f:
      f.write(s.getvalue())

  s = io.StringIO()
  with redirect_stdout(s):
    profiler.print_stats(sort='ncalls') 
    with open('profiling-ncalls.txt', 'w') as f:
      f.write(s.getvalue())

  with open('pstats-cumulative.txt', 'w') as f:
    p = pstats.Stats(profiler, stream=f)
    p.sort_stats('cumulative').print_stats(5)

if __name__ == '__main__':
  main()