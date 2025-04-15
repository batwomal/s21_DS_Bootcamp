import sys
import os
import subprocess

def main():
  required_libraries = ['beautifulsoup4', 'pytest']
  subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + required_libraries)

  installed_packages = subprocess.check_output([sys.executable, '-m', 'pip', 'list']).decode('utf-8')

  formatted_packages = []
  for line in installed_packages.splitlines()[2:]:
    package_info = line.split()
    if len(package_info) >= 2:
      formatted_packages.append(f'{package_info[0]}=={package_info[1]}')

  with open('requirements.txt', 'w') as f:
    for package in formatted_packages:
      f.write(f'{package}\n')
      print(package)

  subprocess.check_call(['zip', '-r', 'batwomalv.zip', 'batwomalv'])

if __name__ == '__main__':
  if 'VIRTUAL_ENV' not in os.environ:
    raise Exception(
        "This script must be run inside a virtual environment.\n"
        "Try: source ../ex02/batwomalv/bin/activate")
  else:
    main()
  
