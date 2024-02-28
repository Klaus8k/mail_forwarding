from email.policy import default
from email.parser import Parser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import quopri
import base64


def write_to_f(data):
    with open('1.txt', 'a', encoding='utf-8') as f:
        f.write(data + '\n')


def bs64_decode(data: str):
    return base64.b64decode(data).decode('utf-8')


def except_message_read(msg):
    message = MIMEMultipart()
    msg_headers = Parser(policy=default).parsestr(
        msg.as_string()
    )

    for part in msg.walk():
        msg_headers = Parser(policy=default).parsestr(
            part.as_string()
        )

        content_type = msg_headers['Content-Type'].split()[0][:-1]
        content_encoding = msg_headers['Content-Transfer-Encoding']

        # is_quoted-printable
        if content_encoding == 'quoted-printable':
            if part.get_charset() == 'utf-8':
                write_to_f('\nis_quoted-printable')

                msg_text = quopri.decodestring(
                    part.get_payload()).decode('utf-8')

                message.attach(MIMEText(msg_text, 'plain'))

            if part.get_charset() == 'windows-1251':
                write_to_f('\nis_quoted-printable')
                msg_text = quopri.decodestring(
                    part.get_payload()).decode('utf-8')

                message.attach(MIMEText(msg_text, 'plain'))

        if content_type == 'text/plain':

            if content_encoding == 'base64':

                msg_text = bs64_decode(part.get_payload())
                write_to_f(msg_text)

                message.attach(MIMEText(msg_text, 'plain'))
            else:
                write_to_f(part.get_payload())

        elif content_type == 'text/html':
            if content_encoding == 'base64':

                msg_text = bs64_decode(part.get_payload())

                message.attach(MIMEText(msg_text, 'plain'))
            else:
                write_to_f(part.get_payload())

        # elif part.get_content_disposition() == 'attachment':
        #     message['file'] = part.as_bytes()
        #     print(message['file'])
        #     write_to_f(f'attachment -----------> {content_type}')

        else:
            write_to_f(
                f'content type Который не обработан: {content_type}')

    return message
