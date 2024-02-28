import json
import imaplib
import email
import smtplib

const_dict = json.load(open("const.json", "r"))
SOURCE_ADDR = const_dict["email"]
PSWD = const_dict["pass"]
HOST = "imap.spaceweb.ru"

FORWARD_ADDRESS = 'tipkor@mail.ru'


# Подключение к серверу IMAP
mail = imaplib.IMAP4_SSL(HOST)
mail.login(SOURCE_ADDR, PSWD)
mail.select('Inbox')

# Получение сообщений
status, num = mail.search(None, 'UNSEEN')


def sender_msg(all_msg: list):
    smtp = smtplib.SMTP(host=HOST, port=587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(SOURCE_ADDR, PSWD)

    for msg in all_msg:
        smtp.send_message(msg=msg, from_addr=SOURCE_ADDR,
                          to_addrs=FORWARD_ADDRESS)

    smtp.close()


# перебираем сообщения по номерам
nums = num[0].split()
print(nums)
msg_to_send = []
for _ in nums:
    status, data = mail.fetch(_, '(RFC822)')
    msg_body = data[0][1]
    email_message = email.message_from_bytes(msg_body)

    msg_to_send.append(email_message)
    sender_msg(all_msg=msg_to_send)
