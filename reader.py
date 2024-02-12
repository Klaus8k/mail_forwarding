import json
from redbox import EmailBox


const_dict = json.load(open("const.json", "r"))
SOURCE_ADDR = const_dict["email"]
PSWD = const_dict["pass"]
HOST = "imap.spaceweb.ru"

box = EmailBox(
    host=HOST,
    port=993,
    username=SOURCE_ADDR,
    password=PSWD,
)

print(box)
# Анализ сообщения
# for msg in messages:
#     print(msg.get_content_type())
