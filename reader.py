import base64
import pprint
import json
import imaplib
import email
from email.message import Message
from typing import List
# https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python

const_dict = json.load(open("const.json", "r"))
SOURCE_ADDR = const_dict["email"]
PSWD = const_dict["pass"]
HOST = "imap.spaceweb.ru"


def write_to_f(data):
    with open('1.txt', 'a', encoding='utf-8') as f:
        f.write(data + '\n')


def print_msg(data: List[Message, ]):
    """берем список сообщений, и в каждом проходим во вложенные.
    определяем тип и забираем.
    типы: текст, штмл, аттач.
    - вложенность, как определить?

    """

    # https://habr.com/ru/articles/17531/
    for i in data:
        for part in i.walk():
            if part.get_content_type():
                content_type = part.get_content_type()
                write_to_f('--------------' + content_type + '--------------')

                if content_type == 'text/plain':
                    write_to_f(part.get_payload())
                elif content_type == 'text/html':
                    write_to_f(part.get_payload())
            break

# Подключение к серверу IMAP
mail = imaplib.IMAP4_SSL(HOST)
mail.login(SOURCE_ADDR, PSWD)
mail.select('Inbox')

# Получение сообщений
status, num = mail.search(None, 'ALL')
all_messages = []
# перебираем сообщения по номерам
nums = num[0].split()
for _ in nums[:3]:
    status, data = mail.fetch(_, '(RFC822)')
    msg_body = data[0][1].decode('utf-8')
    email_message = email.message_from_string(msg_body)
    all_messages.append(email_message)


print_msg(all_messages)
