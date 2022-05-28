import requests, json, os
# free temporary email address
# coded by ./meicookies
api = "https://www.1secmail.com/api/v1/?action="
email = ""
data = {'id': None, 'from': None}
help_msg = """
random: generate email address
message: read the message in your current email
exit: exit this program
help: this fuckin "help" dude
"""
def close():
  input("Press 'ENTER' to close")
def get_random():
  result = requests.get(
    api + "genRandomMailbox&count=1"
  )
  return json.loads(result.text)[0]
def get_message(email):
  data = email.split('@')
  result = requests.get(
    api + f"getMessages&login={data[0]}&domain={data[1]}"
  )
  return json.loads(result.text)
def read_message(email, id):
  data = email.split('@')
  result = requests.get(
    api + f"readMessage&login={data[0]}&domain={data[1]}&id={id}"
  )
  return json.loads(result.text)['body']
def check_message():
  read_msg = read_message(email, data['id'])
  print(f"id: {data['id']}\nfrom: {data['from']}\n")
  option = input("do you want to read this message? (y/n): ")
  with open('read.html', 'w') as file:
    if option == 'y' or option == 'Y':
      file.write(f"{read_msg}\n")
      print("Saved on read.html\n")
      close()
    elif option == 'n' or option == 'N':
      close()
def req_random():
  global email
  email = get_random()
def req_message():
  global data
  read_data = get_message(email)
  if read_data:
    read_data = read_data[0]
    data.update({
      'id': read_data['id'],
      'from': read_data['from']
    })
    check_message()
  else:
    print("no current message\n")
    close()
def helpinfo():
  print(help_msg)
  close()
while True:
  os.system("clear")
  if email:
    print(f"Your email: {email}")
  else:
    print("Type 'help' for more information")
  cmd = input(">> ")
  list_command = {
    'random': req_random,
    'message': req_message,
    'exit': exit,
    'help': helpinfo
  }
  for key, value in list_command.items():
    value() if key == cmd else False
