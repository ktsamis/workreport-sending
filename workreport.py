#!/usr/bin/env python3
import argparse
import datetime
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


# Open the plain text file whose name is in filename for reading.
def create_email(filename):
    print(filename)
    content = open_file(filename)
    if content is False:
        return False
    # check_contents(content)
    # Create a text/plain message
    msg = EmailMessage()
    msg.set_content(content)
    # me = the sender's email address
    me = "User"
    # you = the recipient's email address
    you = "email@email.com"

    msg['Subject'] = str(today.strftime("Workreport, Week %Y-%W"))
    msg['From'] = me
    msg['To'] = you

    # Send the message via our own SMTP server.
    s = smtplib.SMTP('mailserver.nowhere.org', 25)
    vac = vacation(filename)
    if vac is False:
        return False
    else:
        s.send_message(msg)
    # Make a local copy of what we are going to send.
    with open(msg['Subject'], 'wb') as f:
        f.write(bytes(msg))
        print("Report was saved successfully")
    s.quit()
    return 0


def open_file(filename):
    # This function return two different types.
    # This is bad practice, now the caller has to know this and check for the type that is returned.
    exists = os.path.isfile(filename)
    # Try to load it and handle the exception
    if exists is True:
        with open(filename) as file:
            content = file.read()
            return content
    else:
        print("The filename you gave does not exist")
        return False


def vacation(filename):
    cur_time = time.localtime()
    mod_time = time.localtime(os.path.getmtime(filename))
    print(mod_time)
    print(cur_time)

    dt = datetime.fromtimestamp(mktime(mod_time))
    ct = datetime.fromtimestamp(mktime(cur_time))
    diff = ct - dt
    print(diff)
    if diff > timedelta(days=6):
        print("vacation")
        return False
    else:
        print("still here")
        return True


def main():
    args = parse_args()
    try:
        c = create_email(args.file)
        if c is False:
            return False
        notification()
        return True
    # Never catch Exception if you won't handle it decently
    except Exception as e:
        return False


if __name__ == "__main__":
    # Return code bool - Why?
    if main() is False:
        sys.exit(1)
    else:
        print("Main exited normally")
