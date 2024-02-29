#!/usr/bin/python3
import json
import imaplib
import email
import smtplib
from reader import except_message_read


const_dict = json.load(open("const.json", "r"))
SOURCE_ADDR = const_dict["email"]
PSWD = const_dict["pass"]
HOST = "imap.spaceweb.ru"

FORWARD_ADDRESS = const_dict['FORWARD_ADDRESS']

EXEPT_ADDRESS = const_dict['EXEPT_ADDRESS']

# Подключение к серверу IMAP
mail = imaplib.IMAP4_SSL(HOST)
mail.login(SOURCE_ADDR, PSWD)
mail.select('Inbox')

# Получение сообщений
status, num = mail.search(None, 'UNSEEN')

# Получение сообщений


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
msg_to_send = []
for _ in nums:
    status, data = mail.fetch(_, '(RFC822)')
    msg_body = data[0][1]
    email_message = email.message_from_bytes(msg_body)

    src_message = email_message
    # Удаление отчетов от недоставке
    if 'Mail Delivery' in src_message['From']:
        mail.store(_, '+FLAGS', '\\Deleted')
        continue

    # Ловим из списка адресов исключений
    if src_message['From'] in EXEPT_ADDRESS:
        email_message = except_message_read(
            email_message)  # забираем только text/plain
        email_message['From'] = src_message['From'].split('@')[1]
        email_message['Subject'] = src_message['Subject']

    msg_to_send.append(email_message)
    sender_msg(all_msg=msg_to_send)  # Списком в отправщик сообщений

mail.expunge()
mail.close()
mail.logout()
