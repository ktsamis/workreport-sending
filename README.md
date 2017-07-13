The purpose of this python3 script is to automate the workreport sending every
e.g.  week, or whenever you want. This will be determined in a cornjob, or you
can run it manually if you want.

To make the script work:

1. You need to clone the repository
```
git clone https://github.com/ktsamis/workreport-sending.git
```
2. Change the following variables to your emails and mailserver:

```
me = "User"
you = "email@email.com"
'mailserver.nowhere.org'
```
3. Put it in a cronjob to run whenever you want e.g. every Friday at 14:00:

```
0 14 * * 5 python3 workreport.py &> /dev/null
```
The redirection to /dev/null is done to prevent an annoying warning from notify
popping up.
