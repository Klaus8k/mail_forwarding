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
    with open('1.txt', 'w', encoding='utf-8') as f:
        f.write(data + '\n')


def print_msg(data: List[Message, ]):
    """берем список мейл сообщений, по каждому проходим вглубь, определяем тип контента.
    на основе типа контента, надо декодировать инфу.
    Нужно:
    - от кого, кому, тема
    - тело сообщения
    - хтмл если есть
    - аттач, если есть. (попробовать побайтово)
    
    """
    msg_info = {}
    count = 0
    for i in data:
        count += 1
        for part in i.walk():
            if i.get_content_type():
                write_to_f(i.get_content_type())
    # write_to_f(pprint.pformat(msg_info))
    


# Подключение к серверу IMAP
mail = imaplib.IMAP4_SSL(HOST)
mail.login(SOURCE_ADDR, PSWD)
mail.select('Inbox')

# Получение сообщений
status, num = mail.search(None, 'ALL')
all_messages = []
# перебираем сообщения по номерам
for _ in num[0].split():
    status, data = mail.fetch(_, '(RFC822)')
    msg_body = data[0][1].decode('utf-8')
    email_message = email.message_from_string(msg_body)
    all_messages.append(email_message)
    break

print_msg(all_messages)
