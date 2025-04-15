import sys
import logging
from random import randint
import config as co
import requests
import os


class Research:
  def __init__(self):
    logging.info('Initialise Reserch class')
    self.file_path = sys.argv[1]
    with open(self.file_path, 'r') as file:
      lines = file.readlines()
      if len(lines) < 2:
        self.file_path = ""
      header = lines[0].strip().split(',')
      if len(header) != 2:
        self.file_path = ""
      for line in lines[1:]:
        elements = line.strip().split(',')
        for element in elements:
          if element.strip() not in ["0", "1"]:
            self.file_path = ""
            break

  def file_reader(self, has_header=True):
    logging.info('Read file')
    data = []
    with open(self.file_path, "r") as file:
      start = 1 if has_header else 0
      lines = file.readlines()
      for line in lines[start:]:
        string_line = line.strip().split(',')
        dig_line = []
        for dig in string_line:
          dig_line.append(int(dig.strip()))
        data.append(dig_line)

    return data
  
  def send_to_telegram(self, message):
    bot_token = os.environ.get('MY_BOT_TOKEN')
    chat_id = os.environ.get('MY_TG_ID')
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    payload = {
        'chat_id': chat_id,
        'text': message
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Проверка на ошибки
        logging.info('Message sent to personal Telegram chat')
    except requests.exceptions.RequestException as e:
        logging.error(f'Failed to send message: {e}')

  class Calculations:
    def __init__(self):
      logging.info('Initialise Calculations class')
      self.data = Research().file_reader(co.has_header)

    def counts(self):
      logging.info('Calculate counts heads and tails')
      heads, tails = 0, 0
      for line in self.data:
        heads += line[0]
        tails += line[1]
      return heads, tails

    def fractions(self):
      logging.info('Calculate fractions heads and tails')
      heads, tails = self.counts()
      total = heads + tails
      return heads / total, tails / total

  class Analytics(Calculations):
    def predict_random(self):
      logging.info('Calculate predicted list of lists')
      result = []
      for i in range(0,co.num_of_steps):
        head = randint(0,1)
        tail = int(not head)
        result.append([head, tail])
      return result
    
    def predict_last(self):
      logging.info('Calculate last element of data')
      return self.data[-1]
    
    def total(self):
      logging.info('Calculate total count')
      return len(self.data)

    def counts_predicted(self):
      logging.info('Calculate predicted counts heads and tails')
      heads, tails = 0, 0
      for line in self.predict_random():
        heads += line[0]
        tails += line[1]
      return heads, tails

    def save_to_file(self, data, name_of_file, extension='txt', mode='w'):
      logging.info('Saving to file')
      if '.' not in name_of_file:
        name_of_file = f'{name_of_file}.{extension}'
      with open(name_of_file, mode) as file:
        file.write(data)
