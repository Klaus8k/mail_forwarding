import json
from redbox import EmailBox
from redbox.query import UNSEEN, ALL
import imaplib
import email


const_dict = json.load(open("const.json", "r"))
SOURCE_ADDR = const_dict["email"]
PSWD = const_dict["pass"]
HOST = "imap.spaceweb.ru"

# box = EmailBox(
#     host=HOST,
#     port=993,
#     username=SOURCE_ADDR,
#     password=PSWD,
# )

# inbox = box["INBOX"]
# msg_list = []


# for msg in inbox.search(ALL):
#     msg_list.append(msg)


# print(msg_list[0].__dir__())
# Анализ сообщения
# for msg in messages:
#     print(msg.get_content_type())


# Подключение к серверу IMAP
mail = imaplib.IMAP4_SSL(HOST)
mail.login(SOURCE_ADDR, PSWD)
mail.select('Inbox')

# Получение сообщений
typ, data = mail.search(None, 'ALL')
for msg_id in data[0].split():
    typ, data = mail.fetch(msg_id, '(RFC822)')
    msg = email.message_from_string(data[0][1].decode('utf-8'))
    with open('1.txt', 'a') as f:
        f.write(str(type(msg)))
