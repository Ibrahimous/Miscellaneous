#!/usr/bin/python
# -*-coding:utf-8 -*

#SEE: https://docs.python.org/2/library/email-examples.html

# Import smtplib for the actual sending function
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText

textfile = "gorgeousMail"

# Open a plain text file for reading.  For this example, assume that
# the text file contains only ASCII characters.
fp = open(textfile, 'rb')
# Create a text/plain message
msg = MIMEText(fp.read())
fp.close()

# me == the sender's email address
me = "cibrahim@organisation.fr"
# you == the recipient's email address
msg['Subject'] = 'The contents of %s' % textfile
msg['From'] = me
msg['To'] = me

# Send the message via our own SMTP server, but don't include the
# envelope header.
#s = smtplib.SMTP('smtp.amesys.fr') #not working
s = smtplib.SMTP('localhost') #working...
s.sendmail(me, me, msg.as_string())
s.quit()
