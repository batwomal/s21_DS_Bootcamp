import sys

def call_center(clients, recipients):
  not_seen_clients = []
  for client in clients:
    if client not in recipients:
      not_seen_clients.append(client)
  return not_seen_clients

def potential_clients(clients, participants):
  not_clients = []
  for participant in participants:
    if participant not in clients:
      not_clients.append(participant)
  return not_clients

def loyalty_program(clients,participants):
  not_participate_clients = []
  for client in clients:
    if client not in participants:
      not_participate_clients.append(client)
  return not_participate_clients

def main():
  
  clients = ['andrew@gmail.com', 'jessica@gmail.com', 'ted@mosby.com',
    'john@snow.is', 'bill_gates@live.com', 'mark@facebook.com',
    'elon@paypal.com', 'jessica@gmail.com']
  participants = ['walter@heisenberg.com', 'vasily@mail.ru',
    'pinkman@yo.org', 'jessica@gmail.com', 'elon@paypal.com',
    'pinkman@yo.org', 'mr@robot.gov', 'eleven@yahoo.com']
  recipients = ['andrew@gmail.com', 'jessica@gmail.com', 'john@snow.is']

  if (len(sys.argv) != 2):
    print('Wrong usage')
    return 0

  comand = sys.argv[1]

  if comand == 'call_center':
    print(call_center(clients, recipients))
  elif comand == 'potential_clients':
    print(potential_clients(clients, participants))
  elif comand == 'loyalty_program':
    print(loyalty_program(clients, participants))
  else:
    print('Wrong usage')
    return 0

  return 0

if __name__ == '__main__':
  main()