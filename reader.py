from email.policy import default
from email.parser import BytesParser, Parser
import base64
import pprint
import json
import imaplib
import email
from email.message import Message
from typing import List
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import quopri
import smtplib

# https://stackoverflow.com/questions/1463074/how-can-i-get-an-email-messages-text-content-using-python

const_dict = json.load(open("const.json", "r"))
SOURCE_ADDR = const_dict["email"]
PSWD = const_dict["pass"]
HOST = "imap.spaceweb.ru"


# Подключение к серверу IMAP
mail = imaplib.IMAP4_SSL(HOST)
mail.login(SOURCE_ADDR, PSWD)
mail.select('Inbox')

# Получение сообщений
status, num = mail.search(None, 'ALL')
all_messages = []


def write_to_f(data):
    with open('1.txt', 'a', encoding='utf-8') as f:
        f.write(data + '\n')


def bs64_decode(data: str):
    return base64.b64decode(data).decode('utf-8')


def sender_msg(message):
    smtp = smtplib.SMTP(host=HOST, port=587)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(SOURCE_ADDR, PSWD)
    msg = message
    # msg = MIMEMultipart()
    # msg['From'] = SOURCE_ADDR
    # msg['To'] = 'tipkor@mail.ru'
    
    # f_name = '1.pdf'
    
    # msg.attach(MIMEApplication(message['file'], Name=f_name))
    
    # msg['Content-Disposition'] = 'attachment; filename="%s"' % f_name
    smtp.send_message(msg=msg, from_addr=SOURCE_ADDR, to_addrs='tipkor@mail.ru')
    
    smtp.close()


def print_msg(data: List[Message, ]):
    sender_msg(message=data[0])

    for msg in data:

        msg_headers = Parser(policy=default).parsestr(
            msg.as_string()
        )

        message = {}

        for part in msg.walk():
            msg_headers = Parser(policy=default).parsestr(
                part.as_string()
            )

            if not part.is_multipart():

                content_type = msg_headers['Content-Type'].split()[0][:-1]
                content_encoding = msg_headers['Content-Transfer-Encoding']

                # is_quoted-printable
                if content_encoding == 'quoted-printable':
                    if part.get_charset() == 'utf-8':
                        write_to_f('\nis_quoted-printable')
                        write_to_f(quopri.decodestring(
                            part.get_payload()).decode('utf-8'))
                    if part.get_charset() == 'windows-1251':
                        write_to_f('\nis_quoted-printable')
                        write_to_f(quopri.decodestring(
                            part.get_payload()).decode('windows-1251'))

                if content_type == 'text/plain':
                    write_to_f(content_type)
                    write_to_f(content_encoding)
                    if content_encoding == 'base64':
                        write_to_f('\nis_base64')
                        write_to_f(bs64_decode(part.get_payload()))
                    else:
                        write_to_f(part.get_payload())

                elif content_type == 'text/html':
                    write_to_f(content_type)
                    write_to_f(content_encoding)
                    if content_encoding == 'base64':
                        write_to_f('\nis_base64')
                        write_to_f(bs64_decode(part.get_payload()))
                    else:
                        write_to_f(part.get_payload())

                elif part.get_content_disposition() == 'attachment': # Разобраться как сохранить файл.
                    message['file'] = part.as_bytes()
                    print(message['file'])
                    write_to_f(f'attachment -----------> {content_type}')

                else:
                    write_to_f(
                        f'!!!!!!!!!!!!!!! content type Который не обработан: {content_type}')

        write_to_f(' END ' * 10)
        
        # sender_msg(message=message)


# перебираем сообщения по номерам
nums = num[0].split()
for _ in nums[:1]:

    status, data = mail.fetch(_, '(RFC822)')

    msg_body = data[0][1]

    email_message = email.message_from_bytes(msg_body)
    sender_msg(message=email_message)
    # all_messages.append(email_message)

# print_msg(all_messages)
