The purpose of this python3 script is to automate the workreport sending every
e.g.  week, or whenever you want. This will be determined in a cronjob, or you
can run it manually if you want.

To make the script work:

1. You need to clone the repository
```
git clone https://github.com/ktsamis/workreport-sending.git
```
2. Change the following variables to your emails and mailserver and path:

```
description="This script uses a file to send as text. You can give a file with the flag -f or use the default "
                    "which is /home/user/workreport")
default="/home/user/workreport"
me = "User"
you = "email@email.com"
'mailserver.nowhere.org'
```
3. Put it in a cronjob to run whenever you want e.g. every Friday at 14:00:

```
0 14 * * 5 python3 workreport.py > /dev/null 2>&1
```
The redirection to /dev/null is done to prevent an annoying warning from notify
popping up.
