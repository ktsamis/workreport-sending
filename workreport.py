#!/usr/bin/env python3
import argparse
import logging
import os
# Import smtplib for the actual sending function
import smtplib
import sys
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
# Import the email modules we'll need
from email.message import EmailMessage
from time import mktime

# For notifications:
from notify import notification

OK = 0
ERR_IO = 1
ERR_MAIL_SERVER = 2
ERR_ELSE = 3

today = date.today()


def parse_args():
    parser = argparse.ArgumentParser(
        description="This script uses a file to send as text. You can give a file with the flag -f or use the default "
                    "which is /home/user/workreport")
    parser.add_argument("-f", "--file", dest="file",
                        help="Filename relative to the path you are running the script from",
                        default="/home/user/workreport", action='store')
    args = parser.parse_args()
    print(args)
    return args


def create_mail(content):
    msg = EmailMessage()
    msg.set_content(content)
    # me = the sender's email address
    me = "User"
    # you = the recipient's email address
    you = "email@email.com"

    msg['Subject'] = str(today.strftime("Workreport, Week %Y-%W"))
    msg['From'] = me
    msg['To'] = you
    return msg


def outdated_report(filename):
    cur_time = time.localtime()
    mod_time = time.localtime(os.path.getmtime(filename))
    print(mod_time)
    print(cur_time)

    dt = datetime.fromtimestamp(mktime(mod_time))
    ct = datetime.fromtimestamp(mktime(cur_time))
    diff = ct - dt
    if diff >= timedelta(days=6):
        return True
    else:
        return False


# Open the plain text file whose name is in filename for reading.
def send_mail(mail):
    # Send the message via our own SMTP server.
    with smtplib.SMTP('mailserver.nowhere.org', 25) as mailserver:
        mailserver.send_message(mail)


def backup_mail(mail):
    # Make a local copy of what was sent.
    with open(mail['Subject'], 'w') as f:
        f.write(mail.as_string())


def send_report(filename):
    if outdated_report(filename):
        return False
    content = get_report(filename)
    mail = create_mail(content)
    send_mail(mail)
    backup_mail(mail)
    return True


def get_report(filename):
    with open(filename) as f:
        return f.read()


def main():
    args = parse_args()
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S',
                        filename='workreport.log',
                        level=logging.DEBUG)

    try:
        c = send_report(args.file)
        if not c:
            logging.error('The report was not sent. Probably on vacation?')
            return ERR_ELSE
        notification()
        return OK
    except smtplib.SMTPException as e:
        logging.error("I could not send report file due to the imap server. %s", e)
        return ERR_MAIL_SERVER
    except IOError as e:
        logging.error("Something went wrong with IO %s", e)
        return ERR_IO


if __name__ == "__main__":
    sys.exit(main())
